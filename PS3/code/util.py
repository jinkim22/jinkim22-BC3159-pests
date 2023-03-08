import numpy as np
import copy

class Util:
    def __init__(self, robot_object):
        self.robot_object = robot_object

    #####################################################
    #                                                   #
    #  Helper functions you need to fill out start here #
    #                                                   #
    #####################################################

    #####################################################
    #                                                   #
    #    Initialization and Taylor Expansion Helpers    #
    #                                                   #
    #####################################################

    # Compute the total cost along the trajectory
    def compute_total_cost(self, x, u, nx, nu, N):
        #
        # TODO
        #
        # Hint: You may want to use the helper functions in the robot_object!
        #
        J = 0
        return J

    # compute the total constraint error
    def compute_total_constraint_violation(self, x, u, xs, nx, nu, N):
        # I'll start us off with th initial state constraint
        x_err = x[:,0] - xs
        const = np.linalg.norm(x_err, ord=1)
        # then we need to find all of the dynamics errors
        #
        # TODO
        #
        #
        return const

    # compute the dynamics and cost gradient and hessians
    def compute_approximation(self, xk, uk, nx, nu, k):
        Hk, gk = self.robot_object.cost_gradient_hessian(xk, uk)
        Ak, Bk = self.robot_object.next_state_gradient(xk, uk)
        return Ak, Bk, Hk, gk

    #####################################################
    #                                                   #
    #              KKT System Helpers                   #
    #                                                   #
    #####################################################
    
    # form the blocks of the KKT system matrix and vector
    def construct_KKT_system_blocks(self, x, u, xs, nx, nu, N):
        total_states = nx*N
        total_controls = nu*(N-1)
        total_states_controls = total_states + total_controls

        # placeholders of the right size for the blocks you need to compute
        G = np.zeros((total_states_controls, total_states_controls))
        g = np.zeros((total_states_controls, 1))
        C = np.zeros((total_states, total_states_controls)) # note for our setup constraints are equal to states
        c = np.zeros((total_states, 1))

        n = nx + nu

        # filling in the initial constraint gradient and value for you!
        C[0:nx, 0:nx] = np.eye(nx)
        c[0:nx, 0] = x[:,0] - xs

        # now compute all the cost gradients and hessians and the rest of the constraint gradients
        #
        # TODO
        #
        # Hint: Don't forget about the final cost gradient / hessian!
        #

        return G, g, C, c

    # form the main KKT system matrix and vector from its blocks
    def assemble_KTT_system(self, G, g, C, c, nx, nu, N):
        #
        # TODO
        #
        # Hint: h and v stack things up!
        #
        KKTMatrix = None
        KKTVector = None
        return KKTMatrix, KKTVector

    # compute the merit function value along a trajectory
    def compute_merit_value(self, x, u, xs, mu, nx, nu, N):
        #
        # TODO
        #
        # Hint: how are we balancing optimality and feasability?
        #  
        J = 0
        const = 0
        merit = 0
        return J, const, merit

    # line search flag for the SQP algorithm
    def sqp_line_search_criteria(self, x_new, u_new, J_new, const_new, merit_new, x, u, J, const, merit, nx, nu, N):
        #
        # TODO
        #
        # Hint: did things get better?
        #  
        return False

    #####################################################
    #                                                   #
    #            iLQR Backward Pass Helpers             #
    #                                                   #
    #####################################################

    # what is the quadratic approximation of the optimal solution
    # from the perspective of the last state?
    def initialize_CTG(self, x, nx, k):
        #
        # TODO
        #
        # Hint: You may want to use the helper functions in the robot_object!
        #
        Vxx = None
        Vx = None
        return Vxx, Vx

    # compute the quadratic estimate one state back along the trajectory
    def backpropogate_CTG(self, A, B, H, g, Vxx, Vx, nx, nu, k):
        #
        # TODO
        #
        # Hint: A = fx, B = fu, H = Jww, g = Jw where w is x or u!
        # Hint2: Everything is a np.array and np.matmul may be helpful!
        #
        Hxx = None
        Huu = None
        Hux = None
        gx = None
        gu = None
        return Hxx, Hux, Huu, gx, gu

    # given the above computation what is the feedback and feedforward update?
    def compute_kappa_K(self, Hxx, Hux, Huu, gx, gu, HuuInv, nx, nu, N):
        #
        # TODO
        #
        # Hint: Everything is a np.array and np.matmul may be helpful!
        #
        K = None
        kappa = None
        return kappa, K

    # given all that above what is the new CTG estimate at this state?
    def compute_new_CTG(self, Hxx, Hux, Huu, gx, gu, HuuInv, kappa, K, nx, nu, N):
        #
        # TODO
        #
        # Hint: Everything is a np.array and np.matmul may be helpful!
        #
        Vxx = None
        Vx = None
        return Vxx, Vx

    # put most of the above backward pass functions together and get from
    # the inputs to return the current kappa, K, Vxx, Vx
    def backward_pass_iterate(self, A, B, H, g, Vxx_kp1, Vx_kp1, nx, nu, k):
        #
        # TODO
        #
        # Hint: you mostly just need to call the helper functions defined above!
        #       and np.linalg.inv may be helpful!
        #
        kappak = None
        Kk = None
        Vxx = None
        Vx = None
        return kappak, Kk, Vxx, Vx

    #####################################################
    #                                                   #
    #           iLQR Forward Pass Helpers               #
    #                                                   #
    #####################################################

    # return u_new based on the current x_new, k, kappa, alpha, and original x
    def compute_control_update(self, x, x_new, K, kappa, alpha, nx, nu, N):
        #
        # TODO
        #
        # Hint: You may want to use the helper functions in the robot_object!
        # Hint2: Everything is a np.array and np.matmul may be helpful!
        # Hint3: We are computing the UPDATE to the controls
        #
        delta = self.robot_object.state_delta(x_new, x)
        return 0

    # rollout the full trajectory to produce x_new, u_new based on
    # x, u (the original trajectory), as well as K, kappa, alpha (the updates)
    def rollout_trajectory(self, x, u, K, kappa, alpha, nx, nu, N):
        x_new = copy.deepcopy(x)
        u_new = copy.deepcopy(u)
        #
        # TODO
        #
        # Hint: You may want to use the helper functions in the robot_object and in util!
        #        
        return x_new, u_new

    # make sure things got better
    def ilqr_line_search_criteria(self, x_new, u_new, J_new, x, u, J, nx, nu, N):
        #
        # TODO
        #
        # Hint: did things get better?
        #  
        return False