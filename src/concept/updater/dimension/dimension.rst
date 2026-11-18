.. _dimension:

Dimension
=========

Ufil comes with a dimension estimation that is designed to estimate the dimensions of traffic participants based on the measurements from the sensors. The dimension estimation requires the sensor to contain the detected dimensions of the traffic participants. The included estimation uses one grid map per dimension (length, width, height) and estimates the extent covered by all detections of an object. The same approach is used for dimension estimation in a tracker and for dimension fusion in the central fusion, as both are essentially a fusion of the dimensions of all detections.

.. toctree::
   :caption: Contents:
   :maxdepth: 1

   dimension_fusion