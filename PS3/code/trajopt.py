# trajopt.py
# This program runs the main algorithms built on top of your util functions
# (Do not modify, but please read)
#
# Brian Plancher - Spring 2023
# Adapted from code written by Rus Tedrake and Scott Kuindersma

import sys, math, pygame, copy
from pygame.locals import *
from time import sleep
import numpy as np
import scipy as sp
from util import Util
np.set_printoptions(precision=3) # so things print nicer

class Trajopt:
    def __init__(self, robot_object, start_node, goal_node, N, XMAX_MIN, YMAX_MIN, \
                       MAX_ITER = 100, EXIT_TOL = 1e-3, ALPHA_FACTOR = 0.5, ALPHA_MIN = 1e-4, MU = 5):
        self.robot_object = robot_object # the robot_object with physics and cost functions
        self.MAX_ITER = MAX_ITER         # total ddp loops to try
        self.EXIT_TOL = EXIT_TOL         # This is the convergence criterion. We will declare success when the trajectory
                                         # is updated by a norm of less that 1e-4. DO NOT MODIFY.
        self.N = N                       # Number of nodes in a trajectory
        self.start_node = start_node
        self.goal_node = goal_node
        self.util = Util(self.robot_object)
        self.XMAX_MIN = XMAX_MIN         # max for drawing locically
        self.YMAX_MIN = YMAX_MIN         # max for drawing locically
        self.canvas_max = 640            # max for drawing pixels
        # set global line search parameters
        self.alpha_factor = ALPHA_FACTOR # how much to reduce alpha by each deeper search
        self.alpha_min = ALPHA_MIN       # minimum alpha to try
        self.mu = MU                     # merit function weighting        

    def draw_circle(self, node, size, color):
        percent_x = (node[0] + self.XMAX_MIN) / 2 / self.XMAX_MIN
        percent_y = (node[1] + self.YMAX_MIN) / 2 / self.YMAX_MIN
    
        scaled_x = int(self.canvas_max*percent_x)
        scaled_y = int(self.canvas_max*percent_y)    

        pygame.draw.circle(self.screen, color, (scaled_x, scaled_y), size)

    def draw_line(self, node1, node2, color):
        percent_x1 = (node1[0] + self.XMAX_MIN) / 2 / self.XMAX_MIN
        percent_y1 = (node1[1] + self.YMAX_MIN) / 2 / self.YMAX_MIN
        percent_x2 = (node2[0] + self.XMAX_MIN) / 2 / self.XMAX_MIN
        percent_y2 = (node2[1] + self.YMAX_MIN) / 2 / self.YMAX_MIN
    
        scaled_x1 = int(self.canvas_max*percent_x1)
        scaled_y1 = int(self.canvas_max*percent_y1)
        scaled_x2 = int(self.canvas_max*percent_x2)
        scaled_y2 = int(self.canvas_max*percent_y2)

        # check if angle wrapping (and don't draw lines across the screen)
        if node1[0] - node2[0] > math.pi:
            pass
        elif node1[0] - node2[0] < -math.pi:
            pass
        else:
            pygame.draw.line(self.screen, color, (scaled_x2, scaled_y2), (scaled_x1, scaled_y1))

    def init_screen(self):
        # initialize and prepare screen
        pygame.init()
        self.screen = pygame.display.set_mode((self.canvas_max,self.canvas_max))
        pygame.display.set_caption('PS3 - RRT')
        black = 20, 20, 40
        blue = 0, 0, 255
        green = 0, 255, 0
        self.screen.fill(black)
        self.draw_circle(self.start_node, 5, blue)
        self.draw_circle(self.goal_node, 5, green)
        pygame.display.update()

    def draw_trajectory(self, x):
        white = 255, 240, 200
        red = 255, 0, 0
        self.draw_circle(x[:,0], 2, white)
        for k in range(1,self.N):
            self.draw_circle(x[:,k], 2, white)
            self.draw_line(x[:,k-1], x[:,k], red)
        pygame.display.update()
        sleep(0.4)

    def wait_to_exit(self, x, u, DISPLAY_MODE = True):
        # if in test mode return the path
        if not DISPLAY_MODE:
            return x, u, K
        # Else wait for the user to see the solution to exit
        else:
            while(1):
                for e in pygame.event.get():
                    if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                        sys.exit("Leaving because you requested it.")


    def solve(self, x, u, N, DISPLAY_MODE = False, MAIN_SOLVER = '-iLQR', INNER_SOLVER = '-CG'):
        # start up the graphics
        self.init_screen()

        # get constants
        nx = self.robot_object.get_state_size()
        nu = self.robot_object.get_control_size()

        # solve
        error = False
        if MAIN_SOLVER == '-iLQR':
            self.iLQR(x, u, nx, nu, N, DISPLAY_MODE)
        elif MAIN_SOLVER == '-SQP':
            if INNER_SOLVER == '-CG':
                self.SQP(x, u, nx, nu, N, DISPLAY_MODE, 1)
            elif INNER_SOLVER == '-INV':
                self.SQP(x, u, nx, nu, N, DISPLAY_MODE, 0)
            else:
                print("[!] ERROR: Invalid Inner Solver: ", INNER_SOLVER)
                error = True
        else:
            print("[!] ERROR: Invalid Solver: ", MAIN_SOLVER)
            error = True
        return error


    def SQP(self, x, u, nx, nu, N, DISPLAY_MODE = False, INNER_SOLVER = 0):
        # compute initial merit function value
        xs = copy.deepcopy(x[:,0])
        J, const, merit = self.util.compute_merit_value(x, u, xs, self.mu, nx, nu, N)
        J_prev = J
        if DISPLAY_MODE:
            print("Initial Cost: ", J)
            print("Initial Constraint Violation: ", const)
            print("Initial Merit Function: ", merit)

        # start the main loop
        iteration = 0
        failed = False
        while 1:

            # construct the KKT system blocks
            G, C, g, c = self.util.construct_KKT_system_blocks(x, u, xs, nx, nu, N)

            # assemble into full KKT system
            KKTMatrix, KKTVector = self.util.assemble_KTT_system(G, C, g, c, nx, nu, N)

            # solve the KKT system
            if INNER_SOLVER == 0: # backslash (standard matrix inverse / factorization)
                dxul_new = np.linalg.solve(KKTMatrix,KKTVector)[:,0]
            else: # conjugate gradient
                dxul_new = sp.sparse.linalg.cg(KKTMatrix,KKTVector)[0]

            # do line search to accept (or reject) the update
            alpha = 1
            while 1:
                # unravel the update
                x_new = copy.deepcopy(x)
                u_new = copy.deepcopy(u)
                for k in range(N-1):
                    x_new[:,k] += alpha*dxul_new[(nx+nu)*k:(nx+nu)*k + nx]
                    u_new[:,k] += alpha*dxul_new[(nx+nu)*k + nx:(nx+nu)*(k+1)]
                x_new[:,N-1] += alpha*dxul_new[(nx+nu)*(N-1):(nx+nu)*(N-1) + nx]

                # compute the cost, constraint violation, and merit function
                J_new, const_new, merit_new = self.util.compute_merit_value(x_new, u_new, xs, self.mu, nx, nu, N)

                # compute the line search criteria
                flag = self.util.sqp_line_search_criteria(x_new, u_new, J_new, const_new, merit_new, x, u, J, const, merit, nx, nu, N)

                if flag:
                    J_prev = J
                    x = x_new
                    u = u_new
                    J = J_new
                    const = const_new
                    merit = merit_new
                    if DISPLAY_MODE:
                        print("Iter[", iteration, "] Cost[", np.round(J,4), "], Constraint Violation[", np.round(const,4), "], ", \
                                                     "mu [", self.mu, "], Merit Function[", np.round(merit,4), "] and x final:")
                        print(x[:,N-1])
                        self.draw_trajectory(x)
                    break

                # failed try to continue the line search
                elif alpha > self.alpha_min:
                    alpha *= self.alpha_factor
                    if DISPLAY_MODE:
                        print("Deepening the line search")
                
                # failed line search
                else:
                    if DISPLAY_MODE:
                        print("Line search failed")
                    failed = True
                    break

            # Check for exit (or error)
            if failed: # need double break to get out of both loops here if line search fails
                break

            delta_J = J_prev - J
            if delta_J < self.EXIT_TOL:
                if DISPLAY_MODE:
                    print("Exiting for exit_tolerance")
                break
            
            if iteration == self.MAX_ITER - 1:
                if DISPLAY_MODE:
                    print("Exiting for max_iter")
                break
            else:
                iteration += 1

        if DISPLAY_MODE:
            print("Final Trajectory")
            print(x)
            print(u)

        self.wait_to_exit(x, u, DISPLAY_MODE)

    def iLQR(self, x, u, nx, nu, N, DISPLAY_MODE = False):
        
        # allocate memory for things we will compute
        kappa = np.zeros([nu,N-1])     # control updates
        K = np.zeros((nu,nx,N-1))   # feedback gains

        # compute initial cost
        J = self.util.compute_total_cost(x, u, nx, nu, N)
        J_prev = J
        if DISPLAY_MODE:
            print("Initial Cost: ", J)

        # start the main loop
        iteration = 0
        failed = False
        while 1:

            # Do backwards pass to compute new control update and feedback gains: kappa and K
            # start by initializing the cost to go
            Vxx, Vx = self.util.initialize_CTG(x[:,N-1], nx, N) 
            for k in range(N-2,-1,-1):
                # then compute the quadratic approximation at that point
                A, B, H, g = self.util.compute_approximation(x[:,k], u[:,k], nx, nu, k)

                # then compute the control update and new CTG estimates
                kappak, Kk, Vxx, Vx = self.util.backward_pass_iterate(A, B, H, g, Vxx, Vx, nx, nu, k)

                # save kappa and K for forward pass
                kappa[:,k] = kappak.tolist()
                K[:,:,k] = Kk.tolist()

            # Do forwards pass to compute new x, u, J (with line search)
            alpha = 1
            while 1:
                # rollout new trajectory
                x_new, u_new = self.util.rollout_trajectory(x, u, K, kappa, alpha, nx, nu, N)

                # compute new cost
                J_new = self.util.compute_total_cost(x_new, u_new, nx, nu, N)
                    
                # simple line search criteria
                flag = self.util.ilqr_line_search_criteria(x_new, u_new, J_new, x, u, J, nx, nu, N)

                if flag:
                    J_prev = J
                    x = x_new
                    u = u_new
                    J = J_new
                    if DISPLAY_MODE:
                        print("Iteration[", iteration, "] with cost[", round(J,4), "] and x final:")
                        print(x[:,N-1])
                        self.draw_trajectory(x)
                    break

                # failed try to continue the line search
                elif alpha > self.alpha_min:
                    alpha *= self.alpha_factor
                    if DISPLAY_MODE:
                        print("Deepening the line search")
                
                # failed line search
                else:
                    if DISPLAY_MODE:
                        print("Line search failed")
                    failed = True
                    break

            # Check for exit (or error)
            if failed: # need double break to get out of both loops here if line search fails
                break

            delta_J = J_prev - J
            if delta_J < self.EXIT_TOL:
                if DISPLAY_MODE:
                    print("Exiting for exit_tolerance")
                break
            
            if iteration == self.MAX_ITER - 1:
                if DISPLAY_MODE:
                    print("Exiting for max_iter")
                break
            else:
                iteration += 1

        if DISPLAY_MODE:
            print("Final Trajectory")
            print(x)
            print(u)

        self.wait_to_exit(x, u, DISPLAY_MODE)