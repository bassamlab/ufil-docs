.. _state:

State
=====

Ufil comes with a model based state estimation system using the Kalman Filter (KF) and Extended Kalman Filter (EKF) algorithms. The state estimation system is designed to estimate the state of traffic participants based on the measurements from the sensors. The state of a traffic participant is defined as a vector that contains the dynamic parameters of the participant, such as position, velocity, acceleration, orientation, and dimensions. The state estimation system uses a motion model to predict the state of the participant at the next time step and a measurement model to update the predicted state based on the measurements from the sensors.

The models used in the state estimation system are defined in the :ref:`models <models>` section.
 
.. toctree::
   :caption: Contents:
   :maxdepth: 2

   kf
   ekf
