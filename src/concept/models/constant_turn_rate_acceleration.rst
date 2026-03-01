.. _constant_turn_rate_acceleration:

################################################
Constant Turn Rate and Acceleration Model
################################################

.. warning::
    This model is currently not implemented in ufil and serves for documentation purposes only.

The constant turn rate and acceleration (CTRA) model extends the :doc:`constant turn rate and velocity (CTRV) <constant_turn_rate_velocity>` model by incorporating acceleration. This model is suitable for scenarios where objects follow curved trajectories with changing speeds, such as vehicles in urban traffic.

This model is frequently used in autonomous driving, robotics, and radar-based tracking.

Mathematical Formulation
=========================

The state of an object in two-dimensional space is represented as:

.. math::
    \mathbf{x} = \begin{bmatrix} p_x \\ p_y \\ v \\ \theta \\ \omega \\ a \end{bmatrix},

where:

- :math:`p_x, p_y` are the Cartesian coordinates of the object's position,
- :math:`v` is the speed (scalar velocity),
- :math:`\theta` is the heading angle,
- :math:`\omega` is the turn rate (yaw rate),
- :math:`a` is the acceleration.

Since the motion follows a curved trajectory, the state transition function is **nonlinear** and follows:

.. math::
    \mathbf{x}_{k+1} = f(\mathbf{x}_k) + \mathbf{w}_k,

where :math:`f(\mathbf{x}_k)` is the nonlinear motion function, and :math:`\mathbf{w}_k` represents process noise.

For a time step :math:`\Delta t`, the transition function is:

.. math::
    p_x' = p_x + \frac{v}{\omega} (\sin(\theta + \omega \Delta t) - \sin(\theta)) + \frac{a}{\omega^2} (\sin(\theta + \omega \Delta t) - \sin(\theta) - \omega \Delta t \cos(\theta))

.. math::
    p_y' = p_y + \frac{v}{\omega} (-\cos(\theta + \omega \Delta t) + \cos(\theta)) + \frac{a}{\omega^2} (-\cos(\theta + \omega \Delta t) + \cos(\theta) + \omega \Delta t \sin(\theta))

.. math::
    v' = v + a \Delta t

.. math::
    \theta' = \theta + \omega \Delta t

.. math::
    \omega' = \omega

.. math::
    a' = a

This model assumes constant acceleration and turn rate over :math:`\Delta t`.

Sensitivity to Heading Angle Errors
====================================

The CTRA model strongly depends on accurate heading angle estimation. Even small errors in :math:`\theta` can lead to large position errors due to the nonlinear dependency in the state transition function. This issue is particularly critical for longer prediction horizons or high turn rates.

A detailed sensitivity analysis and error propagation study can be found in Bar-Shalom et al. (2001) [1].

Process Noise
=============

The process noise is modeled using the **discretized Wiener process jerk model**, treating acceleration and turn rate variations as Gaussian noise. The noise follows:

.. math::
    \mathbf{w}_k \sim \mathcal{N}(0, \mathbf{Q}),

where :math:`\mathbf{Q}` is computed using:

.. math::
    \mathbf{B} = \begin{bmatrix} \frac{1}{2}\Delta t^2 & 0 & 0 \\
    \frac{1}{2}\Delta t^2 & 0 & 0 \\
    \Delta t & 0 & 0 \\
    0 & \Delta t & 0 \\
    0 & 0 & \Delta t \\
    0 & 0 & \Delta t \end{bmatrix},

.. math::
    \mathbf{W} = \begin{bmatrix} \sigma_a^2 & 0 & 0 \\
    0 & \sigma_\omega^2 & 0 \\
    0 & 0 & \sigma_j^2 \end{bmatrix},

.. math::
    \mathbf{Q} = \mathbf{B} \mathbf{W} \mathbf{B}^T.

Next Steps
==========

For a simpler model, refer to the :doc:`constant turn rate and velocity (CTRV) <constant_turn_rate_acceleration>` model, which does not consider acceleration.

References
--------------------------------

R\. Schubert, E. Richter, and G. Wanielik, “Comparison and evaluation of advanced motion models for vehicle tracking,” Interna-
tional Conference on Information Fusion, 2008

Y\. Bar-Shalom, X. R. Li, and T. Kirubarajan, "Estimation with Applications to Tracking and Navigation," John Wiley & Sons, 2001
