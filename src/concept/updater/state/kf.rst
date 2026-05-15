.. _kf:

================
Kalman Filter
================

The Kalman filter is the canonical algorithm for recursive estimation of the
state of a **linear** dynamical system from noisy measurements.  It assumes
that both the process (motion) and measurement models are linear and that all
uncertainties are Gaussian.  When either model is nonlinear the **extended
Kalman filter** should be used; see :doc:`/concept/updater/state/ekf` for that
case.

The following notation is used throughout this document (see
:ref:`notation` for a complete reference):




Mathematical Formulation
========================

The underlying linear system is expressed as

.. math::
    \mathbf{x}_{k} = \mathbf{F}_{k-1} \mathbf{x}_{k-1} +
        \mathbf{B}_{k-1} \mathbf{u}_{k-1} + \mathbf{w}_{k-1},

.. math::
    \mathbf{z}_{k} = \mathbf{H}_{k} \mathbf{x}_{k} + \mathbf{v}_{k},

where

- :math:`\mathbf{x}_k` is the state vector at time step :math:`k`.
- :math:`\mathbf{F}` is the **state transition matrix** that propagates the
  previous state forward in time,
- :math:`\mathbf{B}` is the **control input matrix** and
  :math:`\mathbf{u}` the control vector (if present),
- :math:`\mathbf{w}` and :math:`\mathbf{v}` are zero‑mean Gaussian noises
  with covariances :math:`\mathbf{Q}` and :math:`\mathbf{R}`,

  .. math::
      \mathbf{w}_{k} \sim \mathcal{N}(0,\mathbf{Q}_{k}),\qquad
      \mathbf{v}_{k} \sim \mathcal{N}(0,\mathbf{R}_{k}).

The filter maintains an estimate :math:`\hat{\mathbf{x}}^+_{k}` and its
covariance :math:`\mathbf{P}^+_{k}` at each time step.  Starting from an
initial guess (often with a large covariance to express uncertainty), the
algorithm proceeds in two phases: prediction and correction.

Prediction Step
----------------

The prior (predicted) state and covariance are computed as

.. math::
    \hat{\mathbf{x}}^-_{k} = \mathbf{F}_{k-1} \hat{\mathbf{x}}^+_{k-1} +
        \mathbf{B}_{k-1} \mathbf{u}_{k-1},

.. math::
    \mathbf{P}^-_{k} = \mathbf{F}_{k-1} \, \mathbf{P}^+_{k-1}
        \, \mathbf{F}^T_{k-1} + \mathbf{Q}_{k-1},

where

- :math:`\mathbf{P}` denotes the state covariance matrix, :math:`\mathbf{Q}`
  the process noise covariance and :math:`\mathbf{R}` the measurement noise
  covariance.

This step propagates the estimate forward and increases uncertainty by adding
process noise.

Correction Step
----------------

After receiving a measurement :math:`\tilde{\mathbf{z}}_{k}`, the filter
computes the innovation (residual)

.. math::
    \tilde{\mathbf{y}}_{k} = \tilde{\mathbf{z}}_{k} -
        \mathbf{H}_{k} \hat{\mathbf{x}}^-_{k},

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

Note that the posterior covariance is always less than or equal to the prior
covariance in the positive semidefinite sense, reflecting the information
added by the measurement.

Process and Measurement Noise
=============================

Both noise covariances :math:`\mathbf{Q}` and :math:`\mathbf{R}` play a
critical role in filter performance.  Typical design strategies mirror those
used for the motion models in :ref:`models`, e.g. using a discretized Wiener
process for :math:`\mathbf{Q}` when the underlying dynamics include
(acceleration) uncertainty.

Code Documentation
==================

The linear Kalman filter is seperated in prediction and correction step. The prediction step is implemented in the ``model_state_predictor.hpp`` using a model which inherits from ``linear_kalman_transition_model.hpp``. The correction step is implemented in the ``model_state_updater.hpp`` usning a measurement model which inherits from ``linear_kalman_measurement_model.hpp``.

Example Usage
-------------

.. code:: cpp
    
    using State = ufil::type::state::PositionVelocity2D;                                                                                                       
    using Control = ufil::type::control::None;                                                                                                                 
    using Measurement = ufil::type::measurement::Pose2D;                                                                                                     
    using TransitionModel = ufil::model::transition::ConstantVelocityTransitionModel<State, Control>;                                                          
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

R\. E\. Kalman, “A new approach to linear filtering and prediction problems,”
Journal of Basic Engineering, 1960

Y\. Kim and H. Bang, "Introduction to Kalman filter and its applications," Introduction and implementations of the Kalman filter, IntechOpen, 2018
