.. _models:

================
Motion Models
================

This section presents different motion models used in tracking and state estimation, categorized into linear and nonlinear models based on their mathematical properties. Most of the equiations and descriptions in this section are based on the work of Schubert et al. [1] and Schramm et al. [2]. Some model formulations and process noise descriptions are inspired by Bar-Shalom et al. [3].

Linear Models
================

These models assume a linear state transition function, making them suitable for applications where motion is well-approximated by linear equations.

Random Walk Model
----------------------
The random walk (RW) model assumes that an object's position changes over time in an unpredictable manner, with no specific direction or velocity. It is useful for modeling erratic motion or when little prior information is available.

:ref:`Read more about the Random Walk model <random_walk>`

Constant Velocity Model
-----------------------------
The constant velocity (CV) model assumes an object moves in a straight line with a fixed velocity, with no acceleration or external forces. It is useful for tracking objects with smooth, predictable motion.

:ref:`Read more about the Constant Velocity model <constant_velocity>`

Extended Constant Velocity Model
--------------------------------------
The extended constant velocity (ECV) model assumes an object moves along curved trajectories, with no acceleration or external forces. It is useful for tracking objects with smooth, predictable motion and little restriction on turning.

:ref:`Read more about the Extended Constant Velocity model <extended_constant_velocity>`

Constant Acceleration Model
--------------------------------
The constant acceleration (CA) model extends the constant velocity model by incorporating acceleration as part of the system state, making it suitable for applications involving objects that undergo smooth acceleration.

:ref:`Read more about the Constant Acceleration model <constant_acceleration>`

Extended Constant Acceleration Model
-------------------------------------------
The extended constant velocity (ECA) model assumes an object moves along curved trajectories, with no jerk or external forces. It is useful for tracking objects with smooth, predictable motion and little restriction on turning.

:ref:`Read more about the Extended Constant Acceleration model <extended_constant_acceleration>`

Nonlinear Models
===================

These models account for nonlinearity in motion, making them better suited for objects undergoing turning motions or more complex dynamics.

Constant Turn Rate and Velocity Model
-------------------------------------------
The constant turn rate and velocity (CTRV) model extends the constant velocity model by incorporating a turn rate, allowing for curved trajectories. However, it requires a reliable heading angle estimation, as errors in heading propagate significantly to position.

:ref:`Read more about the Constant Turn Rate and Velocity model <constant_turn_rate_velocity>`

Constant Turn Rate and Acceleration Model
----------------------------------------------
The constant turn rate and acceleration (CTRA) model extends the constant acceleration model by incorporating a turn rate. This allows for more realistic modeling of objects undergoing both acceleration and turning.

:ref:`Read more about the Constant Turn Rate and Acceleration model <constant_turn_rate_acceleration>`

Bicycle Model
-----------------
The bicycle model provides a more physically realistic representation of vehicle motion, accounting for front-wheel steering and slip angles. It is widely used in autonomous driving and robotics applications.

:ref:`Read more about the Bicycle model <bicycle_model>`

.. toctree::
   :caption: Contents
   :maxdepth: 1

   random_walk.rst
   constant_velocity.rst
   extended_constant_velocity.rst
   constant_acceleration.rst
   extended_constant_acceleration.rst
   constant_turn_rate_velocity.rst
   constant_turn_rate_acceleration.rst
   bicycle_model.rst


[1] R. Schubert, E. Richter, and G. Wanielik, "Comparison and evaluation of advanced motion models for vehicle tracking," International Conference on Information Fusion, Cologne, Germany, 2008
[2] D. Schramm, M. Hiller, R. Bardini, "Vehicle Dynamics 2nd Edition", Springer, Berlin, 2018
[3] Y. Bar-Shalom, X. R. Li, and T. Kirubarajan, "Estimation with Applications to Tracking and Navigation," John Wiley & Sons, 2001