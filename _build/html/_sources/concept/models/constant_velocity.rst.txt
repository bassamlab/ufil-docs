.. _constant_velocity:

################################
Constant Velocity Model
################################

The constant velocity (CV) model is a simple yet widely used motion model in tracking and estimation. In contrast to the :doc:`random walk (RW) <random_walk>` model, it assumes that an object moves in a straight line with a fixed velocity, meaning that no acceleration or external forces affect its motion.

Algorithms commonly use this model in scenarios where the object's motion is smooth and free from abrupt changes or if the system inputs, for example, a change in heading angle or acceleration, can not be estimated.

Mathematical Formulation
========================

In a two-dimensional space, the state of an object is represented by its position and velocity components:

.. math::
    \mathbf{x} = \begin{bmatrix} p_x \\ p_y \\ v_x \\ v_y \end{bmatrix},

where:

- :math:`p_x, p_y` are the Cartesian coordinates of the object's position,
- :math:`v_x, v_y` are the velocity components along the x and y axes, respectively.

The following state transition model governs the evolution of the state over time:

.. math::
    \mathbf{x}_{k+1} = \mathbf{F} \mathbf{x}_k + \mathbf{w}_k,

where:

- :math:`\mathbf{x}_k` is the state at time step :math:`k`,
- :math:`\mathbf{F}` is the state transition matrix,
- :math:`\mathbf{w}_k` is the process noise, modeling uncertainties in the motion.

The state transition matrix for a time step :math:`\Delta t` is given by:

.. math::
    \mathbf{F} = \begin{bmatrix} 1 & 0 & \Delta t & 0 \\ 0 & 1 & 0 & \Delta t \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}.

This matrix propagates the position based on the previous velocity while assuming it remains constant.

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
    \mathbf{G} = \begin{bmatrix} \frac{\Delta t^2}{2} & 0 \\ 0 & \frac{\Delta t^2}{2} \\ \Delta t & 0 \\ 0 & \Delta t \end{bmatrix},

.. math::
    \mathbf{W} = \begin{bmatrix} \sigma_a^2 & 0 \\ 0 & \sigma_a^2 \end{bmatrix},

where :math:`\sigma_a^2` represents the variance of the acceleration noise. 

This formulation is derived from the **discretized Wiener process acceleration model**, which is widely used in Kalman filtering applications.

Code Documentation
==================

The constant velocity model is implemented in ``cv_transition_model.hpp``. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~

.. code:: cpp

    // Define state and control types for model
    using State = ufil::type::state::PositionVelocity2D;
    using Control = ufil::type::control::None;
    using TransitionModel = ufil::model::transition::ConstantVelocityTransitionModel<State, Control>;
    
    // Create model instance and initialize
    TransitionModel model;
    model.onModelInitialization();

    // Step model in update loop
    model.onEveryTimestep(state, timestamp, duration);
    model.step(state, std::nullopt, timestamp, predicted_state);

Next Steps
==========

For scenarios where acceleration plays a significant role, the :doc:`constant acceleration (CA) <constant_acceleration>` model provides a more refined approach to motion prediction. Additionally the :doc:`constant turn rate and velocity (CTRV) <constant_turn_rate_velocity>` model allows for limiting the object's turn rate but is a non-linear model.

References
--------------------------------

R\. Schubert, E. Richter, and G. Wanielik, “Comparison and evaluation of advanced motion models for vehicle tracking,” Interna-
tional Conference on Information Fusion, 2008

Y\. Bar-Shalom, X. R. Li, and T. Kirubarajan, "Estimation with Applications to Tracking and Navigation," John Wiley & Sons, 2001
