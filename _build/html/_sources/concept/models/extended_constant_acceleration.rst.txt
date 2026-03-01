.. _extended_constant_acceleration:

##############################################
Extended Constant Acceleration Model
##############################################

The extended constant acceleration (ECV) model extends the standard :doc:`CV <constant_acceleration>` model by introducing a yaw angle :math:`\psi` that evolves based on a constant yaw rate :math:`\omega`. This allows for a more realistic representation of objects that follow curved trajectories rather than strictly linear motion.

This model is particularly useful in applications where the object's heading changes smoothly over time, such as in vehicle tracking, autonomous navigation, and robotic localization.

Mathematical Formulation
========================

The state vector in a two-dimensional space with yaw angle and yaw rate is defined as:

.. math::
    \mathbf{x} = \begin{bmatrix} p_x \\ p_y \\ v_x \\ v_y \\ a_x \\ a_y \\ \psi \\ \omega \end{bmatrix},

where:

- :math:`p_x, p_y` are the Cartesian coordinates of the object's position,
- :math:`v_x, v_y` are the velocity components along the x and y axes, respectively,
- :math:`a_x, a_y` are the acceleration components along the x and y axes, respectivly,
- :math:`\psi` is the yaw angle (orientation),
- :math:`\omega` is the yaw rate (rate of change of yaw angle).

The state transition model over a time step :math:`\Delta t` is given by:

.. math::
    \mathbf{x}_{k+1} = \mathbf{F} \mathbf{x}_k + \mathbf{w}_k,

where:

- :math:`\mathbf{x}_k` is the state at time step :math:`k`,
- :math:`\mathbf{F}` is the state transition matrix,
- :math:`\mathbf{w}_k` is the process noise.

The state transition matrix for a time step :math:`\Delta t` is given by:

.. math::
    \mathbf{F} = \begin{bmatrix} 1 & 0 & \Delta t & 0 & \frac{1}{2} \Delta t^2 & 0 & 0 & 0\\ 0 & 1 & 0 & \Delta t & 0 & \frac{1}{2} \Delta t^2 & 0 & 0\\ 0 & 0 & 1 & 0 & \Delta t & 0 & 0 & 0\\ 0 & 0 & 0 & 1 & 0 & \Delta t & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 &\\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 &\\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & \Delta t \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix}.

This matrix propagates the position based on the previous acceleration while assuming it remains constant.

.. hint::
    The state transition matrix :math:`\mathbf{F}` might be time-variant as the time step :math:`\Delta t` might not be constant.

Process Noise
=============

To model real-world uncertainties, we introduce process noise :math:`\mathbf{w}_k` following:

.. math::
    \mathbf{w}_k \sim \mathcal{N}(0, \mathbf{Q}).

The process noise covariance matrix :math:`\mathbf{Q}` is designed using a **discretized Wiener process model**, accounting for uncertainty in acceleration and yaw rate:

.. math::
    \mathbf{Q} = \mathbf{G} \mathbf{W} \mathbf{G}^T.

where:

.. math::
    \mathbf{G} = \begin{bmatrix} 
        \frac{\Delta t^3}{6} & 0 & 0 \\ 
        0 & \frac{\Delta t^3}{6} & 0 \\ 
        \frac{\Delta t^2}{2} & 0 & 0 \\ 
        0 & \frac{\Delta t^2}{2} & 0 \\
        \Delta t & 0 & 0 \\ 
        0 & \Delta t & 0 \\ 
        0 & 0 & \frac{\Delta t^2}{2} \\ 
        0 & 0 & \Delta t 
    \end{bmatrix},

.. math::
    \mathbf{W} = \text{diag}(\sigma_a^2, \sigma_a^2, \sigma_\omega^2),

where:

- :math:`\sigma_a^2` is the variance of acceleration noise,
- :math:`\sigma_\omega^2` is the variance of yaw rate noise.

This formulation ensures that the uncertainty in yaw rate does not artificially decrease over time when no updates are received.

Code Documentation
==================

The extended constant acceleration model is implemented in ``extended_ca_transition_model.hpp``. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~

.. code:: cpp

    // Define state and control types for model
    using State = ufil::type::state::PoseVelocityAcceleration2D;
    using Control = ufil::type::control::None;
    using TransitionModel = ufil::model::transition::ExtendedConstantAccelerationTransitionModel<State, Control>;
    
    // Create model instance and initialize
    TransitionModel model;
    model.onModelInitialization();

    // Step model in update loop
    model.onEveryTimestep(state, timestamp, duration);
    model.step(state, std::nullopt, timestamp, predicted_state);

Next Steps
==========

For situations where acceleration plays a significant role, consider using the :doc:`constant acceleration model <constant_acceleration>`, which provides a more refined motion model.

References
--------------------------------

R\. Schubert, E. Richter, and G. Wanielik, “Comparison and evaluation of advanced motion models for vehicle tracking,” Interna-
tional Conference on Information Fusion, 2008