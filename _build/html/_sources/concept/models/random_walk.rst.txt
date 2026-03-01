.. _random_walk:

##################################
Random Walk Model
##################################

The random walk (RW) model is a probabilistic motion model often used in tracking and state estimation when the object's motion is uncertain and exhibits random fluctuations. It assumes that the object's position changes randomly over time, with no specific direction or velocity. 

This model is useful in scenarios where the object's motion is erratic or where there is little information about its future state, such as in applications involving random disturbances or noise.

Mathematical Formulation
========================

In a two-dimensional space, the state of an object is represented by its position components:

.. math::
    \mathbf{x} = \begin{bmatrix} p_x \\ p_y \end{bmatrix},

where:

- :math:`p_x, p_y` are the Cartesian coordinates of the object's position.

The evolution of the state over time is governed by the following state transition model:

.. math::
    \mathbf{x}_{k+1} = \mathbf{x}_k + \mathbf{w}_k,

where:

- :math:`\mathbf{x}_k` is the state at time step :math:`k`,
- :math:`\mathbf{w}_k` is the process noise, representing the random fluctuations in the position.

Process Noise
=============

To account for the random fluctuations in the object's motion, a process noise term is added:

.. math::
    \mathbf{w}_k \sim \mathcal{N}(0, \mathbf{Q}),

where :math:`\mathbf{Q}` is the process noise covariance matrix, which models the variance of the random walk.

In the case of a random walk with independent and identically distributed noise in both x and y directions, the process noise covariance is given by:

.. math::
    \mathbf{Q} = \begin{bmatrix} \sigma_x^2 & 0 \\ 0 & \sigma_y^2 \end{bmatrix},

where :math:`\sigma_x^2` and :math:`\sigma_y^2` are the variances of the noise in the x and y directions, respectively.

Applications
============

The random walk model is commonly used in:

- **Tracking** (e.g., in environments with little prior information about the motion)
- **Sensor fusion** (e.g., when integrating noisy sensor data with unknown dynamics)
- **Simulations** (e.g., modeling random movements in stochastic environments)

This model serves as a useful baseline in situations where more complex motion models like constant velocity or acceleration may not be applicable due to the randomness or lack of motion predictability.

Code Documentation
==================

The random walk model is implemented in ``random_walk_transition_model.hpp``. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~

.. code:: cpp

    // Define state and control types for model
    using State = ufil::type::state::PositionVelocity2D;
    using Control = ufil::type::control::None;
    using TransitionModel = ufil::model::transition::RandomWalkTransitionModel<State, Control>;
    
    // Create model instance and initialize
    TransitionModel model;
    model.onModelInitialization();

    // Step model in update loop
    model.onEveryTimestep(state, timestamp, duration);
    model.step(state, std::nullopt, timestamp, predicted_state);

Next Steps
==========

For scenarios where the object's motion is more structured, the :doc:`constant velocity model <constant_velocity>` or the :doc:`constant acceleration model <constant_acceleration>` might provide better performance in motion prediction.

References
--------------------------------

R\. Schubert, E. Richter, and G. Wanielik, “Comparison and evaluation of advanced motion models for vehicle tracking,” Interna-
tional Conference on Information Fusion, 2008