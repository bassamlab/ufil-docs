.. _bicycle_model:

#######################################
Bicycle Model
#######################################

.. warning::
    This model is currently not implemented in ufil and serves for documentation purposes only.

The **bicycle model** is a widely used kinematic model for vehicles and mobile robots. It captures the motion of wheeled vehicles while accounting for steering dynamics. This model is particularly useful for path planning, state estimation, and control in autonomous driving applications.

Unlike simpler motion models (e.g., the :doc:`constant velocity (CV) <constant_velocity>` or :doc:`constant turn rate and velocity (CTRV) <constant_turn_rate_velocity>` models), the bicycle model considers the effects of steering angle, wheelbase, and vehicle geometry.

Mathematical Formulation
=========================

The **state** of the system is represented as:

.. math::
    \mathbf{x} = \begin{bmatrix} p_x \\ p_y \\ \theta \\ v \\ \delta \end{bmatrix},

where:

- :math:`p_x, p_y` are the Cartesian coordinates of the vehicle,
- :math:`\theta` is the heading angle (orientation),
- :math:`v` is the forward velocity,
- :math:`\delta` is the steering angle.

State Transition Model
=======================

The nonlinear system dynamics evolve as:

.. math::
    \dot{p}_x = v \cos(\theta)

.. math::
    \dot{p}_y = v \sin(\theta)

.. math::
    \dot{\theta} = \frac{v}{L} \tan(\delta)

.. math::
    \dot{v} = a

.. math::
    \dot{\delta} = \omega,

where:

- :math:`L` is the wheelbase of the vehicle,
- :math:`a` is the longitudinal acceleration,
- :math:`\omega` is the rate of change of the steering angle.

Unlike linear models, the **state transition function** is expressed as:

.. math::
    \mathbf{x}_{k+1} = f(\mathbf{x}_k, \mathbf{u}_k) + \mathbf{w}_k,

where :math:`\mathbf{u}_k = [a, \omega]` is the control input and :math:`\mathbf{w}_k` represents process noise.

Process Noise
=============

Since the bicycle model involves nonlinear dynamics, the process noise covariance is estimated using **first-order linearization** techniques such as the **Extended Kalman Filter (EKF)**. The noise covariance :math:`\mathbf{Q}` is approximated as:

.. math::
    \mathbf{Q} \approx \mathbf{G} \mathbf{W} \mathbf{G}^T,

where :math:`\mathbf{G}` is the Jacobian of :math:`f(\mathbf{x}, \mathbf{u})` with respect to the noise terms, and :math:`\mathbf{W}` is the covariance of acceleration and steering rate noise.

Sensitivity to Steering Angle Errors
=====================================

A key limitation of the bicycle model is its **sensitivity to steering angle errors**. Small errors in :math:`\delta` can lead to significant deviations in predicted trajectories, particularly at high speeds. This sensitivity has been analyzed extensively in tracking literature (see [1] for a detailed discussion).

Next Steps
==========

For a simpler approximation of vehicle motion, see the :doc:`constant turn rate and acceleration (CTRA) <constant_turn_rate_acceleration>` model. For a more detailed model incorporating tire forces, refer to dynamic models such as the **full vehicle model**.

References
--------------------------------

R. Rajamani, "Vehicle Dynamics and Control," Springer, 2011
