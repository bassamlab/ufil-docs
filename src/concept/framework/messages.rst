.. _messages:

Messages
========

``ufil_msgs`` defines the ROS 2 interface of Ufil. The messages map the
:ref:`object definition <object_definition>` one to one; ``ufil_ros`` converts them to and from
the types of ``ufil_object_tracking``.

Object Lists
------------

.. code-block:: text

   ufil_msgs/ObjectList
   ├── std_msgs/Header header             # frame and stamp of all objects
   └── Object[] objects
       ├── uint32 id
       ├── StateWithCovariance state
       │   ├── State state                # x, y, v_x, v_y, a_x, a_y, yaw, yaw_rate (float64)
       │   └── float64[64] covariance     # 8 x 8 matrix
       ├── DimensionWithCovariance dimension
       │   ├── Dimension dimension        # length, width, height (float64)
       │   └── float64[9] covariance      # 3 x 3 matrix
       ├── float64 existence_probability
       ├── Classification classification  # float32[7], indexed by the class constants
       ├── Features features              # bool fl, fr, bl, br, f, b, l, r, c
       └── Axle[] axles                   # axle topology, may be empty

``ObjectStamped`` carries a single object with a header, e.g. the own vehicle of an on-board unit.

The class indices of ``Classification`` (also used by ``Detection``) are:

.. list-table::
   :header-rows: 1
   :widths: 10 20 10 20

   * - Index
     - Class
     - Index
     - Class
   * - 0
     - ``CAR``
     - 4
     - ``PEDESTRIAN``
   * - 1
     - ``TRUCK``
     - 5
     - ``STATIONARY``
   * - 2
     - ``MOTORCYCLE``
     - 6
     - ``OTHER``
   * - 3
     - ``BICYCLE``
     -
     -

An ``Axle`` describes one axle of the axle topology:

.. code-block:: text

   bool single_track                 # one wheel track (e.g. motorcycle) instead of two
   float32 track_width               # [m]
   float32 track_width_variance      # [m^2]
   float32 center_to_axle            # distance from the object center [m]
   float32 center_to_axle_variance   # [m^2]
   bool[] wheel_detected             # left to right in driving direction

Components that do not estimate a part of the object set the corresponding covariance entries to
``-1`` (see :ref:`object_definition`).

Detections
----------

``Detection`` (with ``DetectionList`` and ``DetectionStamped``) is a lightweight measurement
without covariances: ``id``, ``state``, ``dimension`` and a ``classification`` vector.

Sensor Field of View
--------------------

``SensorFOV`` describes the field of view of a sensor in spherical coordinates around
``origin``: range ``r_min``/``r_max``, azimuth ``phi_min``/``phi_max`` and elevation
``theta_min``/``theta_max``, with a 6 x 6 ``covariance``. The point cloud preprocessor of the
outdoor sensor node estimates it continuously, and the central fusion uses it to compute the
persistence probability of the existence fusion (see :ref:`existence`).

Occlusion grids are published as standard ``nav_msgs/OccupancyGrid`` messages.

Maps
----

``LaneletMapOsm`` carries a Lanelet2 map as raw OSM XML (``data``) with a header.

External Messages
-----------------

Besides ``ufil_msgs``, Ufil uses standard and third-party interfaces at its boundaries:

- ``etsi_its_cam_msgs/CAM`` (`etsi_its_messages <https://github.com/ika-rwth-aachen/etsi_its_messages>`_)
  for Cooperative Awareness Messages and ``udp_msgs/UdpPacket`` for the UDP bridge,
- ``sensor_msgs/PointCloud2`` for lidar data, ``nav_msgs/OccupancyGrid`` for SSL pressure grids and
  occlusion grids,
- ``visualization_msgs/MarkerArray`` for the visualization,
- ``derived_object_msgs/ObjectArray`` and ``carla_msgs`` (CARLA), ``cpm_lab_lab_msgs`` (CPM Lab)
  and ``sbg_driver`` (UofA test vehicle) in the example adapters.
