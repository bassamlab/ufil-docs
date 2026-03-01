.. _euclidean_distance:

==================
Euclidean Distance
==================

Overview
--------
The Euclidean distance is a widely used metric for measuring the straight-line distance between two points in an n-dimensional space and is defined as

.. math::
    d_{euclidean} = \sqrt{(\pmb{p_b} - \pmb{p_a})^T (\pmb{p_b} - \pmb{p_a})},

where :math:`\pmb{p_a}` and :math:`\pmb{p_b}` represent the position vectors of the state and measurement vectors.

Limitations
-----------
- It does not account for measurement uncertainties or correlations.
- It does not consider the orientation of the object or any other dynamic state variable.

Selection Note
--------------
The Euclidean distance is a good choice for applications where covariance matrices are unavailable or unnecessary. It is computationally efficient and works well in normalized spaces. However, for cases where uncertainty information is critical, the Mahalanobis distance is preferred.

Code Documentation
==================

The Euclidean distance is implemented in Ufil. It is used to create a cost matrix that helps in optimal measurement-to-track assignments. The function is located in `hypothesizer_functions.hpp`.

Function Definition
-------------------

.. code-block:: cpp
    
    namespace ufil
    {
    namespace association
    {
    
    template<typename TrackType>
    void euclidean(
    const TrackType & track, const typename TrackType::MeasurementType & measurement,
    ufil::type::Scalar & distance)
    {
    const auto & state = track.currentState();
    const auto position_detection = measurement.position();
    const auto position_object = state.position();
    distance = (position_detection - position_object).norm();
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
    ufil::association::euclidean(track, measurement, distance);
    std::cout << "Euclidean Distance: " << distance << std::endl;

Parameters
----------

- `track`: The track containing the estimated state.
- `measurement`: The measurement to compare against the track's state.
- `distance`: Output parameter storing the computed Euclidean distance.
