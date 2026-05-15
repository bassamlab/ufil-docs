.. _ekf:

=========================
Extended Kalman Filter
=========================

The extended Kalman filter (EKF) is a nonlinear variant of the standard Kalman
filter. It applies to **nonlinear** dynamical systems where the state transition
and/or measurement models are given by nonlinear functions rather than linear
matrices.  The EKF operates by linearizing these functions around the current
estimate using first-order Taylor expansions (Jacobian matrices), then applying
the standard Kalman filter mechanics to the linearized system.

The following notation is used throughout this document (see
:ref:`notation` for a complete reference):

- :math:`\mathbf{x}_k` is the state vector at time step :math:`k`.


- :math:`f(\cdot)` and :math:`h(\cdot)` are the **nonlinear state transition
  and measurement functions**, respectively.



Mathematical Formulation
========================

The nonlinear system is described by

.. math::
    \mathbf{x}_{k} = f(\mathbf{x}_{k-1}, \mathbf{u}_{k-1}) + \mathbf{w}_{k-1},

.. math::
    \mathbf{z}_{k} = h(\mathbf{x}_{k}) + \mathbf{v}_{k},

where

- :math:`f(\cdot)` is the **nonlinear state transition function** that
  propagates the state forward in time,
- :math:`h(\cdot)` is the **nonlinear measurement function**,
- :math:`\mathbf{u}` is the control vector (if present),
- :math:`\mathbf{w}` and :math:`\mathbf{v}` are zero‑mean Gaussian noises
  with covariances :math:`\mathbf{Q}` and :math:`\mathbf{R}`,

  .. math::
      \mathbf{w}_{k} \sim \mathcal{N}(0,\mathbf{Q}_{k}),\qquad
      \mathbf{v}_{k} \sim \mathcal{N}(0,\mathbf{R}_{k}),

where

- :math:`\mathbf{P}` denotes the state covariance matrix, :math:`\mathbf{Q}`
  the process noise covariance and :math:`\mathbf{R}` the measurement noise
  covariance.

The EKF linearizes these functions at the current operating point using
first-order Taylor expansions. The Jacobian matrices are computed as

.. math::
    \mathbf{F}_{k-1} = \left. \frac{\partial f}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}^+_{k-1}, \mathbf{u}_{k-1}},

.. math::
    \mathbf{H}_{k} = \left. \frac{\partial h}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}^-_{k}}.,

where

- :math:`\mathbf{F}` and :math:`\mathbf{H}` are the **Jacobian matrices** of
  :math:`f` and :math:`h` evaluated at the current estimate.

These Jacobians replace the constant linear matrices of the standard Kalman
filter, allowing the algorithm to approximate nonlinear dynamics.

Prediction Step
----------------

The prior (predicted) state and covariance are computed as

.. math::
    \hat{\mathbf{x}}^-_{k} = f(\hat{\mathbf{x}}^+_{k-1}, \mathbf{u}_{k-1}),

.. math::
    \mathbf{P}^-_{k} = \mathbf{F}_{k-1} \, \mathbf{P}^+_{k-1}
        \, \mathbf{F}^T_{k-1} + \mathbf{Q}_{k-1}.

Note that the nonlinear function :math:`f` is applied to obtain the predicted
state, while the Jacobian :math:`\mathbf{F}` is used for the covariance
propagation (linearized dynamics).

Correction Step
----------------

After receiving a measurement :math:`\tilde{\mathbf{z}}_{k}`, the filter
computes the innovation (residual) using the nonlinear measurement function

.. math::
    \tilde{\mathbf{y}}_{k} = \tilde{\mathbf{z}}_{k} -
        h(\hat{\mathbf{x}}^-_{k}),

and the Kalman gain

.. math::
    \mathbf{K}_{k} = \mathbf{P}^-_{k} \mathbf{H}^T_{k}
        (\mathbf{H}_{k} \mathbf{P}^-_{k} \mathbf{H}^T_{k} +
        \mathbf{R}_{k})^{-1}.

The posterior estimate and covariance are then updated by

.. math::
    \hat{\mathbf{x}}^+_{k} = \hat{\mathbf{x}}^-_{k} +
        \mathbf{K}_{k} \tilde{\mathbf{y}}_{k},

.. math::
    \mathbf{P}^+_{k} = (\mathbf{I} - \mathbf{K}_{k} \mathbf{H}_{k})
        \mathbf{P}^-_{k}.

As in the linear filter, the posterior covariance reflects the reduction in
uncertainty provided by the measurement.

Linearization and Approximation Error
=====================================

The EKF replaces nonlinear functions with their first-order Taylor
approximations. This linearization incurs approximation error that grows with
the magnitude of nonlinearity and the size of the covariance (uncertainty
region).  For highly nonlinear systems or when nonlinearity matters
significantly, higher-order filters (e.g., unscented Kalman filter,
particle filters) may be required.

Motion Models and Process Noise
===============================

Many of the motion models described in :ref:`models` are nonlinear, such as
the :doc:`constant turn rate and velocity (CTRV) <../../models/constant_turn_rate_velocity>`
model. The EKF is the standard approach for estimating states under these
models. Process and measurement noise covariances are designed using the same
principles as for linear filters; see :ref:`models` for details on
:math:`\mathbf{Q}` design.

Code Documentation
==================

The extended Kalman filter is seperated in prediction and correction step. The prediction step is implemented in the ``model_state_predictor.hpp`` using a model which inherits from ``non_linear_kalman_transition_model.hpp``. The correction step is implemented in the ``model_state_updater.hpp`` usning a measurement model which inherits from ``non_linear_kalman_measurement_model.hpp``.

Example Usage
-------------

.. code:: cpp
    using State = ufil::type::state::PoseVelocity2D;
    using Control = ufil::type::control::None;                                                                                                                 
    using Measurement = ufil::type::measurement::Pose2DWithDimension3D;                                                                                      
    using TransitionModel = ufil::model::transition::ExtendedConstantVelocityTransitionModel<State, Control>;                                                  
    using MeasurementModel = ufil::model::LinearKalmanMeasurementModel<State, Measurement>;
    
    // Prediction step                                                                                                                                       
    TransitionModel transition_model;                                                                                                                          
    transition_model.onModelInitialization();                                                                                                                
    transition_model.onEveryTimestep(state, timestamp, duration);
    transition_model.step(state, std::nullopt, timestamp, predicted_state);
    
    // Correction step
    MeasurementModel measurement_model;                                                                                                                        
    measurement_model.step(predicted_state, measurement, timestamp, corrected_state); 

References
--------------------------------

R\. E\. Kalman, “A new approach to linear filtering and prediction problems,” Journal of Basic Engineering, 1960

Y\. Kim and H. Bang, "Introduction to Kalman filter and its applications," Introduction and implementations of the Kalman filter, IntechOpen, 2018

H\. A\. P\. Blom and Y\. Bar-Shalom, "The interacting multiple model algorithm for systems with Markovian switching coefficients," in IEEE Transactions on Automatic Control, vol. 33, no. 8, pp. 780-783, 1988