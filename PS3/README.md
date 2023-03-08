# COMS BC 3159 - S23
# PS3: Trajectory Optimization
* Due: 11:59pm, Friday March 10th

# Written Assignment (14 points)

Please go to the PDF in the written folder for the written instructions.

# Coding Assignment (26 points)
**You must submit to gradescope to get credit for the assignment --- make sure you submit the required files before the deadline!**

**NOTE: You need to install some python pacakges `pip install -r requirements.txt`**

**NOTE2: You can do this in Colab but you'll lose the visualizations and I think it'll be easier to work on seperate files locally.**

**Files in this assignment:**
`pendulum.py`   Defines a series of (very useful) helper functions related to the robot (the pendulum) we are working with.
                You will need to finish some of the implementation here (and thus submit to Gradescope for Autograding).

`util.py`       The main file you will edit and implement helper functions (and thus submit to Gradescope for Autograding).

`trajopt.py`    Defines the high level trajectory optimzation functions that call the helper functions in `util` and `pendulum` in order to solve trajopt problems. You DO NOT need to submit this file.

`runPend.py`    Sets up some constants and calls the trajopt functions to run and graphically display the solve. You DO NOT need to submit this file.
                
                Usage is: -MAIN_SOLVER (-INNER_SOLVER) where
                    * MAIN_SOLVER  = [iLQR, SQP]
                    * INNER_SOLVER = [CG, INV]

## Taylor Approximations of Dynamics and Cost Functions (7 Points)

For this part of the problem we'll be working in the `pendulum.py` file and we'll be implementing a few dynamics and cost helper functions that we'll use in the rest of the assignemnt.

Functions to update and their points:
* `next_state` 2 points
* `next_state_gradient` 2 points
* `cost_value` 1 point
* `cost_gradient` 1 point
* `cost_hessian` 1 point

We'll begin by converting the pendulum physics functions which compute acceleration (`dynamics`) and its gradient (`dynamics_gradient`) into `next_state` and `next_state_gradient` functions through the use of Euler integration. Recall from class that Euler integation adds a small amount of acceleration and velocity to the original position and velocity:
```
`[q', qd'] = [q, qd] + dt * [qd, qdd]`
```
Also recall that the dynamics derivative matricies are:
```
             A = [[dq'/dq, dq'/dqd],    and B = [[dq/du],
                  [dqd'/dq, dqd'/dqd]]           [dqd/du]]
```

Next we'll move onto the cost functions. Here we need to implement the cost value, gradient, and hessian. For this problem we are going to use the "standard simple quadratic cost":
```
0.5(x-xg)^TQ(x-xg) + 0.5u^TRu
```
As that outputs a scalar value the cost gradient and hessian therefore are of the form:
```
g = [dcost/dq, dcost/dqd, dcost/du]
H = [[d^2cost/dq^2,   d^2cost/dq dqd, d^2cost/dq du], 
     [d^2cost/dqd dq, dcost/dqd^2,    d^2cost/dqd du],
     [d^2cost/du dq,  dcost/du dqd,   d^2cost/du^2]]
```

Note that most things are of type [`np.array`](https://numpy.org/doc/stable/user/quickstart.html) which hopefully should simplify your linear algebra and there are a few more hints left in the code comments! Also, make sure to take into account both the states and the controls!

## Constructing and Solving KKT Systems (10 Points)

Now that we have built a full pendulum object with integrators and cost functions we can use that to build up and solve KKT systems using sucessive quadratic programming! All functions for this section (and the next DDP section) can be found in `util.py` and will be helper functions called by the functions in `trajopt.py`.

Functions to update and their points:
* `compute_total_cost` 1 point
* `compute_total_constraint_violation` 2 point
* `construct_KKT_system_blocks` 4 points
* `assemble_KTT_system` 1 point
*  `compute_merit_value` 1 point
* `sqp_line_search_criteria` 1 point

### Part 1: Helpers

We'll start by setting up some real helper functions that build directly off of the previous section.
* `compute_total_cost`: simply sums the cost across each timestep along the trajectory leveraging the cost functions your wrote in the previous section.
* `compute_total_constraint_violation`: similarly sums up the constraint error. In our case this is simply the dynamics constraints along the trajecotory as well as the initial state constraint (`x0 = xs`). Please use the [L1 norm](https://montjoile.medium.com/l0-norm-l1-norm-l2-norm-l-infinity-norm-7a7d18a4f40c) here (aka absolute sum).

### Part 2: Setting up the KKT System

`construct_KKT_system_blocks`: Now that we have those helper functions in place lets set up the KKT system. This is the big part of this section. Here we want to walk through the states and controls along the trajectory and build the full `G, g, C, c` matricies. Note that in this case `G` is the cost Hessian for the whole trajectory, `g` is the cost gradient, `C` is the constraint gradient, and `c` is the constraint value. Also note that we assume the state/control/lambda ordering discussed in class. That is:
```
[x_0, u_0, x_1, u_1 ... u_{N-1}, x_N, \lambda_0, \lamnbda_1 ... \lamnbda_N]^T
```
*Hint: what is the sparsity pattern you expect in those matricies?*

`assemble_KTT_system`: Now that we have set up the KKT system blocks we need to form it into the full KKT system!
```
[[G, C^T],  *  [[xu],       =  [[-g],   <--->   KKT * xul = kkt
 [C, 0  ]]      [\lambda]]      [c]]
```

### Part 3: Solving the KKT System

Now that we have the problem steup we need to use sequential quadratic programming to continously solve QPs. But, we need to be careful and apply a line search to make sure we are taking good steps toward the goal! Since this is a constrained optimization problem we need to balance primal optimiality (finding the minimum of the cost function) and dual feasibility (finding a solution that doens't violate the constraints).

`compute_merit_value`: we are going to go about doing this by forming what is called a "merit function." This function will be the function we line search over and it will be our guide of how to balance the optimality and feasibility of our solution. We will use the standard L1 merit function (Nocedal and Wright 15.4) where:
```
merit = cost_value + \mu * |constaint_value|
```

`sqp_line_search_criteria`: Finally, we'll evaluate the new trajectory as compared to the old trajectory and make sure we are improving in terms of making a sufficient decrease in both cost and constraint according to our merit function. 

*Hint: this one is simpler than you may think.*

### Part 4 - Explore
Now that you have a working SQP implementation run 
```
python3 runPend.py -SQP
```
What happens? Does the trajectory go all the way to the goal? Does the trajectory always look dynamically feasible? Check the terminal output to see the cost function and constraint violations at each iteration. If you change the parameters for the cost function by adjusting `Q` and `R` in that file what happens? Play around with it a little bit. Hopefully it will give you a little better intuition for what the math is doing! You can also switch between using the standard matrix inverse solution of the KKT system to using a conjugate gradient verison. Simply pass in `-CG` or `-INV` at the end of the line above and you will switch between using the two. Can you tell a difference?

## DDP Algorithm (9 points)

In this section, you'll be implementing the DDP algorithm (in particular the iLQR variant). Your goal will be to implement several functions in `util.py` to successfully optimize paths under a cost function. We'll be leveraging all of the work we have done before to help setup the problem and again the main loop code is in `trajopt.py`.

Functions that should be filled in for full credit in the `util.py` file are:
* `initialize_CTG`            - 1 point
* `backpropogate_CTG`         - 2 points
* `compute_du_K`              - 1 point
* `compute_new_CTG`           - 1 point
* `backward_pass_iterate`     - 1 points
* `compute_control_update`    - 1 point
* `rollout_trajectory`        - 1 point
* `ilqr_line_search_criteria` - 1 point

### Part 1 - The Backward Pass
We first compute the feedback control update along the backward pass using the math from the lecture slides (again this is not something you should memorize but it is helpful to understand how its working). Be careful with the sizes of various items and note that you will likely need to slice into items to get the subparts you are looking for.

`initialize_CTG`: We start by setting up the initial quadratic approximation of the cost-to-go (aka negative reward / value function) at the final state. Hint: what is the possible best cost you can have when you are at the last state? What is a quadratic approximation of that?

`backpropogate_CTG`: We now need to compute the CTG update at the previous state using our linear approximation of the dynamics and our quadratic approximation of the cost at that state and of the cost-to-go at the next state. To do this we will use the iLQR version of the math from the lecture slides. Also note that most things are numpy arrays and so the [np.matmul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html) function will make your life a lot easier!

```
Qxx = lxx + fx^T V'xx fx
Quu = luu + fu^T V'xx fu
Qxu = lxu + fx^T V'xx fu
Qx = lx + fx^T V'x
Qu = lu + fu^T V'x
```

`compute_du_K`and `compute_new_CTG` Following that you'll need to use those outputs to construct K, du, and the new estimate of the cost-to-go Vxx, Vx again using the math from the lecture slides (see image below) and again most things are numpy arrays!

```
\delta u = = -Quu^{-1} (Qux \delta x + Qu) = K \delta x + du
Vx = Qx - Qxu du
Vxx = Qxx - Qxu K
```

* `backward_pass_iterate` Finally we'll put that all together and solve a full backwards pass iterate. That is, given `A, B, H, g` -- the cost and dynaics gradients and the cost Hessian --  as well as `Vxx_kp1, Vx_kp1` -- the next states CTG gradient and Hessian -- how can we output `duk, Kk, Vxx, Vx` -- the feedforward and feedback update to the controls and the currrent gradient and Hessian of the CTG.

*Hint: you mostly just need to call the previous few functions!*

### Part 3 - The Forward Pass
Finally, you'll want to compute the control updates in the forward pass based on the feedback controller you computed in the backward pass!

`compute_control_update`: Here we want to compute the change in a single control we want to apply at a single state. Remember that we have both a feedforward (du) term and a feedback (K) term. You'll also want to implement the line search version of the control update!

`rollout_trajectory`: Now you'll want to use that function to rollout a full new trajectory for a given line search iterate.

`ilqr_line_search_criteria`: Finally, you'll want to return a flag indicating whether that newly rolled out trajectory should be accepted or rejected. Remember in iLQR the constraints are implicit in the rollout, so we only need to worry about making sure we have improved in terms of optimality (cost).

*Hint: this one is simpler than you may think.*

### Part 4 - Explore
Now that you have a working DDP implementation run the `runPend.py` file. What happens? How does this work as compared to the SQP algorithm? Is it better? Worse? Slower? Faster? Does the trajectory go all the way to the goal? If you change the parameters for the cost function by adjusting `Q` and `R` in that file what happens? Play around with it a little bit. Hopefully it will give you a little better intuition for what the math is doing!
