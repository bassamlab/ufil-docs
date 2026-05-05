.. _constant_acceleration:

#######################################
Constant Acceleration Model
#######################################

The constant acceleration (CA) model extends the :doc:`constant velocity (CV) <constant_velocity>` model by including acceleration as a part of the system state. This model is useful in scenarios where objects undergo smooth acceleration, making it more realistic for tracking and estimation compared to the constant velocity model.

This model is frequently used in applications such as autonomous vehicles, robotics, and radar tracking systems.

Mathematical Formulation
=========================

In a two-dimensional space, the state of an object is represented by its position, velocity, and acceleration components:

.. math::
    \mathbf{x} = \begin{bmatrix} p_x \\ p_y \\ v_x \\ v_y \\ a_x \\ a_y \end{bmatrix},

where:

- :math:`p_x, p_y` are the Cartesian coordinates of the object's position,
- :math:`v_x, v_y` are the velocity components along the x and y axes,
- :math:`a_x, a_y` are the acceleration components along the x and y axes.

The state transition model follows:

.. math::
    \mathbf{x}_{k+1} = \mathbf{F} \mathbf{x}_k + \mathbf{w}_k,

where:

- :math:`\mathbf{x}_k` is the state at time step :math:`k`,
- :math:`\mathbf{F}` is the state transition matrix,
- :math:`\mathbf{w}_k` is the process noise, modeling uncertainties in acceleration.

For a time step :math:`\Delta t`, the state transition matrix is:

.. math::
    \mathbf{F} = \begin{bmatrix} 1 & 0 & \Delta t & 0 & \frac{1}{2}\Delta t^2 & 0 \\
    0 & 1 & 0 & \Delta t & 0 & \frac{1}{2}\Delta t^2 \\
    0 & 0 & 1 & 0 & \Delta t & 0 \\
    0 & 0 & 0 & 1 & 0 & \Delta t \\
    0 & 0 & 0 & 0 & 1 & 0 \\
    0 & 0 & 0 & 0 & 0 & 1 \end{bmatrix}.

This matrix models how position and velocity evolve under constant acceleration.

Process Noise
=============

The process noise accounts for real-world uncertainties using the **discretized Wiener process jerk model**, where jerk (rate of change of acceleration) is treated as Gaussian noise with variance :math:`\sigma_j^2`. The noise follows:

.. math::
    \mathbf{w}_k \sim \mathcal{N}(0, \mathbf{Q}),

where :math:`\mathbf{Q}` is the process noise covariance matrix, computed as:

.. math::
    \mathbf{B} = \begin{bmatrix} \frac{1}{6}\Delta t^3 & 0 \\
    0 & \frac{1}{6}\Delta t^3 \\
    \frac{1}{2}\Delta t^2 & 0 \\
    0 & \frac{1}{2}\Delta t^2 \\
    \Delta t & 0 \\
    0 & \Delta t \end{bmatrix},

.. math::
    \mathbf{W} = \begin{bmatrix} \sigma_j^2 & 0 \\
    0 & \sigma_j^2 \end{bmatrix},

and the process noise covariance is given by:

.. math::
    \mathbf{Q} = \mathbf{B} \mathbf{W} \mathbf{B}^T.

This formulation is derived from the **discretized Wiener process jerk model**, commonly used in Kalman filtering applications (see [1] for reference).

Code Documentation
==================

The constant acceleration model is implemented in ``ca_transition_model.hpp``. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~

.. code:: cpp

    // Define state and control types for model
    using State = ufil::type::state::PositionVelocityAcceleration2D;
    using Control = ufil::type::control::None;
    using TransitionModel = ufil::model::transition::ConstantAccelerationTransitionModel<State, Control>;
    
    // Create model instance and initialize
    TransitionModel model;
    model.onModelInitialization();

    // Step model in update loop
    model.onEveryTimestep(state, timestamp, duration);
    model.step(state, std::nullopt, timestamp, predicted_state);

Next Steps
==========

For scenarios involving turning motions, the :doc:`constant turn rate and acceleration (CTRA) <constant_turn_rate_acceleration>` extends this approach further but is a non-linear model.

References
==========

R\. Schubert, E. Richter, and G. Wanielik, “Comparison and evaluation of advanced motion models for vehicle tracking,” Interna-
tional Conference on Information Fusion, 2008

Y\. Bar-Shalom, X. R. Li, and T. Kirubarajan, "Estimation with Applications to Tracking and Navigation," John Wiley & Sons, 2001
