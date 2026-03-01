.. _intersection_over_union_distance:

================================
Intersection over Union Distance
================================

Overview
--------
The Intersection over Union distance (IoU) is a commonly used metric for measuring the spatial overlap between two objects in n-dimensional space. Unlike Euclidean or Mahalanobis distance, it considers the shape of the objects involved, making it especially useful when object dimensions are significant. It is frequently applied in bounding box regression—for example, in object tracking—to quantify how much a predicted bounding box overlaps with a ground truth measurement. This overlap metric is essential for associating objects and enhances overall tracking accuracy. In the case of Ufil, we scale and invert the value so that lower values indicate stronger matches, which aligns with our association logic. The Intersection over Union is defined as 

.. math::
    d_{IoU} = (1 - \frac{Intersection(A, B)}{Union (A, B)}) \cdot 100,

where :math:`A` and :math:`B` are two n-dimensional bounding boxes.

Compared to other distances like Euclidean or Mahalanobis, the IoU is limited to :math:`d_{IoU} \in [0,100]`, where :math:`100` means no overlap and :math:`0` means complete overlap.

Limitations
-----------
- It does not account for measurement uncertainties or correlations.
- Less computationally efficient than Euclidean distance.

Selection Note
--------------
Use the Intersection over Union distance whenever both state and dimensional data (width, length) are available and covariance matrices can be neglected.

If your application requires uncertainty information use distance measurements like the Malahanobis distance which explicitly incorporates covariance information.

Code Documentation
==================

The IoU distance is implemented in Ufil. It is used to construct a cost matrix for associating measurements with tracks, supporting optimal data association.
The implementation resides in `hypothesizer_functions.hpp`. 

Function Definition
-------------------

.. code-block:: cpp
    
    namespace ufil
    {
    namespace association
    {
    
    template<typename TrackType>
    void intersection_over_union_2D(
    const TrackType & track, const typename TrackType::MeasurementType & measurement,
    ufil::type::Scalar & distance)
    {
    const ufil::type::Scalar x_detection = measurement.x();
    const ufil::type::Scalar y_detection = measurement.y();
    const ufil::type::Scalar length_detection = measurement.dimension().length();
    const ufil::type::Scalar width_detection = measurement.dimension().width();
    if(length_detection <= 0.0f || width_detection <= 0.0f) {
        throw std::runtime_error("IoU: Dimension can't be <= 0");
    }
    const ufil::type::Scalar yaw_detection = measurement.yaw();


    bg::model::polygon<bg::model::d2::point_xy<ufil::type::Scalar>> detection_polygon =
        create_rotated_rectangle(x_detection, y_detection, length_detection,
                                            width_detection, yaw_detection);

    const auto & state = track.currentState();
    const auto & dimension = track.currentDimension();
    const ufil::type::Scalar x_track = state.x();
    const ufil::type::Scalar y_track = state.y();
    const ufil::type::Scalar length_track = dimension.length();
    const ufil::type::Scalar width_track = dimension.width();
    if(length_track <= 0.0f || width_track <= 0.0f) {
        throw std::runtime_error("IoU: Dimension can't be <= 0");
    }
    const ufil::type::Scalar yaw_track = state.yaw();
    bg::model::polygon<bg::model::d2::point_xy<ufil::type::Scalar>> track_polygon =
        create_rotated_rectangle(x_track, y_track, length_track,
                                            width_track, yaw_track);
    std::vector<bg::model::polygon<bg::model::d2::point_xy<ufil::type::Scalar>>> buffer;
    bg::intersection(detection_polygon, track_polygon, buffer);

    if(buffer.size() > 1) {
        throw std::runtime_error("IoU: intersection with more than one polygon is not possible");
    }
    ufil::type::Scalar intersection_area = 0.0f;
    if(!buffer.empty()) {
        intersection_area = bg::area(buffer[0]);
    }


    buffer.clear();
    bg::union_(detection_polygon, track_polygon, buffer);

    ufil::type::Scalar union_area = 0.0f;
    for(const auto & p : buffer) {
        union_area += bg::area(p);
    }

    if(union_area > 0.0f) {
        distance = (1.0f - (intersection_area / union_area)) * 100;  // intersectionOU 1 great, 0 bad
    } else {
        throw std::runtime_error("IoU calculation failed: Union can't be 0.0");
    }
    }

    
    }  // namespace association
    }  // namespace ufil

Helper Functions
----------------

It makes use of additional helper functions that handle geometric operations as creating rotated rectangles and individual points which can be found in `impl/intersection_over_union_functions.hpp`

.. code-block:: cpp
    
    #ifndef UFIL_OBJECT_TRACKING__ASSOCIATION__IMPL__INTERSECTION_OVER_UNION_FUNCTIONS_HPP_
    #define UFIL_OBJECT_TRACKING__ASSOCIATION__IMPL__INTERSECTION_OVER_UNION_FUNCTIONS_HPP_

    #include <vector>
    #include <cmath>
    #include <boost/geometry.hpp>
    #include <boost/geometry/geometries/point_xy.hpp>
    #include <boost/geometry/geometries/polygon.hpp>

    #include "ufil_object_tracking/types/scalar.hpp"

    namespace bg = boost::geometry;


    inline bg::model::d2::point_xy<ufil::type::Scalar> rotate_point(
    const bg::model::d2::point_xy<ufil::type::Scalar> & p,
    const bg::model::d2::point_xy<ufil::type::Scalar> & center, ufil::type::Scalar angle_rad)
    {
    ufil::type::Scalar cos_p = std::cos(angle_rad);
    ufil::type::Scalar sin_p = std::sin(angle_rad);
    ufil::type::Scalar x = bg::get<0>(p) - bg::get<0>(center);
    ufil::type::Scalar y = bg::get<1>(p) - bg::get<1>(center);

    //  rotation matrix
    ufil::type::Scalar x_rot = cos_p * x - sin_p * y + bg::get<0>(center);
    ufil::type::Scalar y_rot = sin_p * x + cos_p * y + bg::get<1>(center);

    return bg::model::d2::point_xy<ufil::type::Scalar>(x_rot, y_rot);
    }

    inline bg::model::polygon<bg::model::d2::point_xy<ufil::type::Scalar>> create_rotated_rectangle(
    ufil::type::Scalar x, ufil::type::Scalar y, ufil::type::Scalar length,
    ufil::type::Scalar width, ufil::type::Scalar angle_rad)
    {
    std::vector<bg::model::d2::point_xy<ufil::type::Scalar>> corners;
    corners.reserve(5);  // reserve space to avoid reallocations
    ufil::type::Scalar half_length = length / 2.0;
    ufil::type::Scalar half_width = width / 2.0;
    // create vector
    std::vector<bg::model::d2::point_xy<ufil::type::Scalar>> position = {
        bg::model::d2::point_xy<ufil::type::Scalar>(x - half_length, y - half_width),  // topLeft
        bg::model::d2::point_xy<ufil::type::Scalar>(x + half_length, y - half_width),  // topRight
        bg::model::d2::point_xy<ufil::type::Scalar>(x + half_length, y + half_width),  // bottomRight
        bg::model::d2::point_xy<ufil::type::Scalar>(x - half_length, y + half_width)  // bottomLeft
    };
    // rotate
    for(const auto & p : position) {
        corners.emplace_back(rotate_point(p, bg::model::d2::point_xy<ufil::type::Scalar>(x, y),
                                        angle_rad));
    }
    corners.emplace_back(corners[0]);  // otherwise polygon would be open.
    bg::model::polygon<bg::model::d2::point_xy<ufil::type::Scalar>> poly;
    bg::assign_points(poly, corners);
    bg::correct(poly);  // Ensure polygon is valid & orientation is correct
    return poly;
    }

    #endif  // UFIL_OBJECT_TRACKING__ASSOCIATION__IMPL__INTERSECTION_OVER_UNION_FUNCTIONS_HPP_


Example Usage
-------------

.. code-block:: cpp

    #include <iostream>
    #include <ufil_object_tracking/ufil_object_tracking.hpp>

    // Get track and measurement

    ufil::type::Scalar distance;
    ufil::association::intersection_over_union_2D(track, measurement, distance);
    std::cout << "Intersection over Union Distance: " << distance << std::endl;

Parameters
----------

- `track`: The track containing the estimated state.
- `measurement`: The measurement to compare against the track's state.
- `distance`: Output parameter storing the computed Intersection over Union distance.
