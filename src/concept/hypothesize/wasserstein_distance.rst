.. _wasserstein_distance:

====================
Wasserstein Distance
====================

Overview
--------
The Wasserstein distance is a statistical metric that measures the distance
between two probability distributions. It originates from optimal transport
theory and is also known as the Earth Mover’s Distance.

In the general case, computing the Wasserstein distance requires solving an
optimal transport optimization problem. However, when both distributions are
Gaussian, the 2-Wasserstein distance admits a closed-form analytical solution.
Ufil implements this closed-form solution for Gaussian state and measurement
distributions.

For two Gaussian distributions
:math:`\mathcal{N}(\pmb{\mu}_1, \pmb{C}_1)` and
:math:`\mathcal{N}(\pmb{\mu}_2, \pmb{C}_2)`,
the closed-form 2-Wasserstein distance is:

.. math::

    d_{W} =
    \sqrt{
        \|\pmb{\mu}_1 - \pmb{\mu}_2\|^2
        +
        \operatorname{tr}
        \left(
            \pmb{C}_1 + \pmb{C}_2
            -
            2 \left(
                \pmb{C}_1^{1/2}
                \pmb{C}_2
                \pmb{C}_1^{1/2}
            \right)^{1/2}
        \right)
    }

where:

- :math:`\pmb{\mu}_1`, :math:`\pmb{\mu}_2` are the mean vectors
- :math:`\pmb{C}_1`, :math:`\pmb{C}_2` are the covariance matrices
- :math:`\operatorname{tr}(\cdot)` denotes the matrix trace
- :math:`(\cdot)^{1/2}` is the symmetric matrix square root

Interpretation
--------------
The Wasserstein distance consists of two components:

1. **Mean term** — squared Euclidean distance between the means.
2. **Covariance term** — geometric difference between uncertainty ellipsoids.

Unlike the Mahalanobis distance, which evaluates compatibility under a shared
covariance assumption, the Wasserstein distance symmetrically compares two
full Gaussian distributions. Differences in uncertainty shape directly
influence the result.

.. warning::
   The computation requires matrix square roots of positive semi-definite
   matrices. Numerical instability may occur if covariance matrices are
   ill-conditioned. Matrix square root operations are computationally more
   expensive than matrix inversion.

Limitations
-----------
- Requires positive semi-definite covariance matrices.
- Computationally heavier than Mahalanobis distance.
- Matrix square root operations dominate runtime.
- Numerical stability depends on the implementation of ``matrix_sqrt``.

Selection Note
--------------
The Wasserstein distance is a good choice when:

- A symmetric distribution-to-distribution metric is required.
- Differences in uncertainty shape should influence association.
- A geometrically meaningful metric is preferred over likelihood-based measures.

For high-rate real-time systems, the additional computational load should be
evaluated carefully.

Code Documentation
==================

The Wasserstein distance is implemented in Ufil as part of its association
process. It is used to create a cost matrix that helps in optimal
measurement-to-track assignments.

The function is located in ``hypothesizer_functions.hpp``.

Function Definition
-------------------

.. code-block:: cpp

    namespace ufil
    {
    namespace association
    {

    template<typename TrackType>
    void wasserstein(
      const TrackType & track,
      const typename TrackType::MeasurementType & measurement,
      ufil::type::Scalar & distance)
    {
      const typename TrackType::StateType & state = track.currentState();

      // Compute difference term (handles periodic variables internally)
      const ufil::type::Vector<TrackType::MeasurementType::Size> difference =
        ufil::difference<typename TrackType::MeasurementType,
          typename TrackType::StateType>(measurement, state);

      ufil::type::Scalar diff_term = difference.squaredNorm();

      const auto H =
        ufil::generateMeasurmentMatrix<typename TrackType::MeasurementType,
          typename TrackType::StateType>();

      // Project state covariance into measurement space
      const ufil::type::SquareMatrix<TrackType::MeasurementType::Size> C1 =
        H * state.covariance() * H.transpose();

      const ufil::type::SquareMatrix<TrackType::MeasurementType::Size> C2 =
        measurement.covariance();

      // Compute matrix square roots
      const ufil::type::DynamicMatrix sqrt_C1 = ufil::matrix_sqrt(C1);
      const ufil::type::SquareMatrix<TrackType::MeasurementType::Size> M =
        sqrt_C1 * C2 * sqrt_C1;

      const ufil::type::DynamicMatrix sqrt_M = ufil::matrix_sqrt(M);

      // Compute trace term
      const ufil::type::Scalar trace_term =
        (C1 + C2 - 2.0f * sqrt_M).trace();

      // Final Wasserstein distance
      distance = std::sqrt(trace_term + diff_term);
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
    ufil::association::wasserstein(track, measurement, distance);

    std::cout << "Wasserstein Distance: "
              << distance << std::endl;

Parameters
----------

- `track`: The track containing the estimated state.
- `measurement`: The measurement to compare against the track's state.
- `distance`: Output parameter storing the computed Mahalanobis distance.