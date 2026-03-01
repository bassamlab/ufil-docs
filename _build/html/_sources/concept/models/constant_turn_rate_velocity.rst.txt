.. _constant_turn_rate_velocity:

##############################################
Constant Turn Rate and Velocity Model
##############################################

.. warning::
    This model is currently not implemented in ufil and serves for documentation purposes only.

The constant turn rate and velocity (CTRV) model extends the :doc:`constant velocity (CV) <constant_velocity>` model by incorporating a turn rate, allowing for curved motion. This model is particularly useful in tracking applications where objects follow smooth, turning trajectories, such as vehicles making turns or aircraft following curved flight paths.

This model assumes that the object moves with constant velocity and a fixed turn rate over the prediction step. **It is highly sensitive to errors in heading angle estimation**, as even small errors can lead to large deviations in the predicted position.

Mathematical Formulation
=========================

In a two-dimensional space, the state of an object is represented by:

.. math::
    \mathbf{x} = \begin{bmatrix} p_x \\ p_y \\ v \\ \theta \\ \omega \end{bmatrix},

where:

- :math:`p_x, p_y` are the Cartesian coordinates of the object's position,
- :math:`v` is the velocity magnitude (or speed),
- :math:`\theta` is the heading angle,
- :math:`\omega` is the turn rate (angular velocity).

The nonlinear state transition function is given by:

.. math::
    \mathbf{x}_{k+1} = f(\mathbf{x}_k) + \mathbf{w}_k,

where :math:`f(\mathbf{x}_k)` represents the nonlinear evolution of the state. Assuming a small time step :math:`\Delta t`, the motion model is:

.. math::
    p_x^{k+1} = p_x^k + \frac{v^k}{\omega^k} \left( \sin(\theta^k + \omega^k \Delta t) - \sin(\theta^k) \right),

.. math::
    p_y^{k+1} = p_y^k + \frac{v^k}{\omega^k} \left( -\cos(\theta^k + \omega^k \Delta t) + \cos(\theta^k) \right),

.. math::
    v^{k+1} = v^k,

.. math::
    \theta^{k+1} = \theta^k + \omega^k \Delta t,

.. math::
    \omega^{k+1} = \omega^k.

If the turn rate :math:`\omega` is very small (close to zero), the equations reduce to a linear motion update similar to the :doc:`constant velocity (CV) <constant_velocity>` model.

Process Noise
=============

The process noise accounts for real-world uncertainties using a **discretized Wiener process acceleration model**, where acceleration noise :math:`\sigma_a^2` and turn rate noise :math:`\sigma_\omega^2` are considered. The noise follows:

.. math::
    \mathbf{w}_k \sim \mathcal{N}(0, \mathbf{Q}),

where the process noise covariance matrix :math:`\mathbf{Q}` is computed using:

.. math::
    \mathbf{B} = \begin{bmatrix} \frac{1}{2} \Delta t^2 & 0 \\
    0 & \frac{1}{2} \Delta t^2 \\
    \Delta t & 0 \\
    0 & \Delta t \\
    0 & \Delta t \end{bmatrix},

.. math::
    \mathbf{W} = \begin{bmatrix} \sigma_a^2 & 0 \\
    0 & \sigma_\omega^2 \end{bmatrix},

and the process noise covariance is:

.. math::
    \mathbf{Q} = \mathbf{B} \mathbf{W} \mathbf{B}^T.

Sensitivity to Heading Angle Errors
====================================

This model is highly dependent on the **accuracy of heading angle estimation**. Errors in :math:`\theta` can propagate significantly into :math:`p_x` and :math:`p_y`, especially at higher velocities. This sensitivity can be analyzed by computing the Jacobian of :math:`f(\mathbf{x})` with respect to :math:`\theta` and observing its influence on position error growth.

A detailed discussion on error propagation in nonlinear motion models, including the CTRV model, can be found in **Bar-Shalom et al. (2001)** [1].

Next Steps
==========

For cases where acceleration also plays a role in turn maneuvers, see the :doc:`constant turn rate and acceleration (CTRA) <constant_turn_rate_acceleration>`.

References
--------------------------------

R\. Schubert, E. Richter, and G. Wanielik, “Comparison and evaluation of advanced motion models for vehicle tracking,” Interna-
tional Conference on Information Fusion, 2008

Y\. Bar-Shalom, X. R. Li, and T. Kirubarajan, "Estimation with Applications to Tracking and Navigation," John Wiley & Sons, 2001

