..  _mahalanobis_distance:

====================
Mahalanobis Distance
====================

Overview
--------
The Mahalanobis distance is a statistical metric that measures the distance between a measurement and an object track while considering their uncertainties. Unlike Euclidean distance, it accounts for scaling, correlations, and variances of different dimensions, making it well-suited for probabilistic tracking and association tasks.

It is computed as:

.. math::
    d_{mahalanobis} = \sqrt{(\pmb{x_b} - \pmb{x_a})^T \cdot \pmb{P}_{ab}^{-1} \cdot (\pmb{x_b} - \pmb{x_a})}

where :math:`\pmb{x_a}` and :math:`\pmb{x_b}` are two states (e.g., a track position and a measurement), and :math:`\pmb{P}_{ab}` is the combined covariance matrix:

.. math::
    \pmb{P}_{ab} = \pmb{P}_a + \pmb{P}_b - \pmb{P}_{a,b}

where :math:`\pmb{P}_a` and :math:`\pmb{P}_b` are the individual covariances, and :math:`\pmb{P}_{a,b}` is the cross-covariance.


.. warning::
    The function assumes :math:`\pmb{P}_{ab}` is invertible. If numerical instability occurs, a pseudo-inverse or regularization may be used. This can lead to higher and sometimes inconsistent computation times.

Limitations
-----------
- Requires an invertible covariance matrix.
- Computational heavy.

Selection Note
--------------
The Mahalanobis distance is a good choice for applications where uncertainty and correlations matter, and slower computation is acceptable. This distance calculation requires heavy matrix computation, including regularization for stability, and may not produce a result if the covariance matrices are badly conditioned.

Code Documentation
==================
The Mahalanobis distance is implemented in Ufil as part of its association process. It is used to create a cost matrix that helps in optimal measurement-to-track assignments. The function is located in `hypothesizer_functions.hpp`.

Function Definition
-------------------

.. code-block:: cpp
    
    namespace ufil
    {
    namespace association
    {

    template<typename TrackType>
    void mahalanobis(
    const TrackType & track, const typename TrackType::MeasurementType & measurement,
    ufil::type::Scalar & distance)
    {
    const auto & state = track.currentState();
    const auto H = ufil::generateMeasurmentMatrix<typename TrackType::MeasurementType,
        typename TrackType::StateType>();

    // Compute the average covariance
    const ufil::type::SquareMatrix<TrackType::MeasurementType::Size> covariance =
        0.5 * (H * state.covariance() * H.transpose() + measurement.covariance());

    // Check if the covariance matrix is invertible using a small threshold
    if (covariance.determinant() < 1e-6) {
        distance = ufil::scalar::ScalarMax;  // use a max distance value to indicate a problem
        return;
    }

    // Compute the difference vector
    const auto difference =
        ufil::difference<typename TrackType::MeasurementType,
        typename TrackType::StateType>(measurement, state);

    // Compute Mahalanobis distance
    // Invert covariance using Eigenvalue decomposition for better stability
    Eigen::SelfAdjointEigenSolver<ufil::type::DynamicMatrix> solver(covariance);
    if (solver.info() != Eigen::Success) {
        // If decomposition fails, return a max distance
        distance = ufil::scalar::ScalarMax;
        return;
    }

    // Calculate the Mahalanobis distance: sqrt(difference^T * inv(covariance) * difference)
    const ufil::type::DynamicMatrix inv_covariance =
        solver.eigenvectors() * solver.eigenvalues().cwiseInverse().asDiagonal() *
        solver.eigenvectors().transpose();
    distance = std::sqrt(difference.transpose() * inv_covariance * difference);
    }

    }  // namespace association
    }  // namespace ufil

Example Usage
-------------

.. code-block:: cpp

    #include <iostream>
    #include <ufil_object_tracking/ufil_object_tracking.hpp>

    // Get track and measurement
    
    ufil::type::Scalar distance;
    ufil::association::mahalanobis(track, measurement, distance);
    std::cout << "Mahalanobis Distance: " << distance << std::endl;

Parameters
----------

- `track`: The track containing the estimated state.
- `measurement`: The measurement to compare against the track's state.
- `distance`: Output parameter storing the computed Mahalanobis distance.
