.. _usage:

Running Ufil
============

This page explains how to start Ufil with Docker Compose, how the ROS 2 middleware is selected,
how an example is split across machines and how to look at the results. It assumes the runtime
image is available and the workspace is built (see :doc:`../installation/installation`).

Compose Profiles
----------------

``docker-compose.yaml`` at the root of the workspace defines one service per task. Every service
uses the runtime image and mounts the workspace at ``/workspace``. Services are grouped into
profiles, and a run is composed by selecting profiles:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Profile
     - Starts
   * - ``build``
     - ``make sequential`` in the container; the build output lands in the workspace on the host.
   * - ``terminal``
     - An interactive shell with access to ``/dev``, ``/media`` and the X11 display.
   * - ``bag``
     - ``ros2 bag play /bag --clock`` for the bag directory given in ``BAG``.
   * - ``router``
     - The Zenoh router ``rmw_zenohd`` on port ``7447`` (started automatically by every ROS profile).
   * - ``foxglove-bridge``
     - The Foxglove WebSocket bridge on ``ws://localhost:8765``.
   * - ``rviz``
     - RViz 2 on the host display (X11).
   * - ``carla-highway``, ``carla-highway-head``, ``carla-highway-headless``
     - The :doc:`CARLA highway example <../examples/carla/carla>` on one machine, or its head or
       headless part.
   * - ``cpm-lab``, ``cpm-lab-head``, ``cpm-lab-headless``
     - The :doc:`CPM Lab example <../examples/cpm_lab/cpm_lab>` on one machine, or its head or
       headless part.
   * - ``pedestrian``
     - The :doc:`pedestrian example <../examples/pedestrian/pedestrian>`; the scenario is selected
       with ``PEDESTRIAN_SCENARIO`` (default ``crossing.yaml``).

Profiles compose freely, so any example can run with Foxglove, RViz, both or neither:

.. code-block:: bash

   COMPOSE_PROFILES=carla-highway,foxglove-bridge docker compose up
   COMPOSE_PROFILES=cpm-lab,rviz docker compose up
   PEDESTRIAN_SCENARIO=group.yaml COMPOSE_PROFILES=pedestrian,foxglove-bridge docker compose up

The example services launch with ``use_sim_time:=false``. When you replay a bag, the ``bag``
service publishes ``/clock``; launch the example yourself from a ``terminal`` with
``use_sim_time:=true`` if the nodes have to follow the bag time.

Replaying a Bag
~~~~~~~~~~~~~~~

Point the ``bag`` profile at a bag directory on the host. It is mounted read-only at ``/bag``:

.. code-block:: bash

   BAG=/absolute/path/to/my_bag COMPOSE_PROFILES=cpm-lab-headless,bag,foxglove-bridge docker compose up

``BAG`` is only required when the ``bag`` profile is active; without it the service exits with an
error.

.. _usage_middleware:

Middleware
----------

All ROS services share one middleware, selected with two environment variables:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Variable
     - Default
     - Values
   * - ``RMW_IMPLEMENTATION``
     - ``rmw_zenoh_cpp``
     - ``rmw_zenoh_cpp``, ``rmw_fastrtps_cpp``, ``rmw_cyclonedds_cpp``
   * - ``ROS_DOMAIN_ID``
     - ``21``
     - any valid domain id

.. code-block:: bash

   RMW_IMPLEMENTATION=rmw_cyclonedds_cpp COMPOSE_PROFILES=pedestrian,foxglove-bridge docker compose up

With Zenoh (the default), every ROS profile also starts the ``router`` service and all nodes
connect to it at ``tcp/router:7447``. With another RMW the router exits right away and the nodes
use DDS discovery. ``COMPOSE_PROFILES=router`` starts the router alone.

.. _usage_distributed:

Distributed Setup: Head and Headless
------------------------------------

The deployments of Ufil are distributed: on-board units and the visualization run on one
machine, the infrastructure (outdoor sensor node, sensitive surface layer and road side unit) on
another. Every example therefore has the same launch file structure:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Launch file
     - Content
   * - ``<example>_head.launch.xml``
     - **Head machine**: adapters of the vehicles (on-board units), CAM transmission via UDP and the
       visualization nodes.
   * - ``<example>_headless.launch.xml``
     - **Headless machine**: outdoor sensor node, sensitive surface layer and the road side unit with
       CAM reception and central fusion.
   * - ``<example>.launch.xml``
     - Head and headless on a single machine. Loads ``config/<example>_local.yaml`` on top, which
       e.g. sends the CAMs to ``127.0.0.1`` instead of the RSU address.

.. mermaid::
   :caption: Distributed setup of an example with the default Zenoh middleware
   :alt: Head machine with on-board units, visualization and Zenoh router; headless machine with OSN, SSL and RSU; CAMs over UDP and ROS topics over Zenoh
   :align: center

   flowchart LR
      subgraph HEAD["Head machine (-head profile)"]
         OBU["On-board units<br/>adapters, CAM senders"]
         VIZ["Visualization<br/>markers, Foxglove / RViz"]
         ROUTER["Zenoh router<br/>tcp/7447"]
      end
      subgraph HEADLESS["Headless machine (-headless profile)"]
         OSN["Outdoor sensor node"]
         SSL["Sensitive surface layer"]
         RSU["Road side unit<br/>CAM reception, central fusion"]
         OSN --> RSU
         SSL --> RSU
      end
      OBU -. "CAM over UDP<br/>(target_address:5000)" .-> RSU
      HEADLESS <-->|"ROS 2 topics<br/>(ZENOH_CONFIG_OVERRIDE)"| ROUTER
      ROUTER <--> VIZ

To split an example across two machines, run the ``-head`` profile on one machine and the
``-headless`` profile on the other. The headless machine connects to the router of the head
machine instead of starting its own:

.. code-block:: bash

   # Head machine
   COMPOSE_PROFILES=cpm-lab-head,foxglove-bridge docker compose up

   # Headless machine
   ZENOH_ROUTER=false \
   ZENOH_CONFIG_OVERRIDE='connect/endpoints=["tcp/<head-ip>:7447"];listen/endpoints=["tcp/0.0.0.0:0"]' \
   COMPOSE_PROFILES=cpm-lab-headless docker compose up

The CAMs of the on-board units are not sent over ROS but as ETSI ITS messages over UDP, like a
real V2X radio would. The target address of the ``udp_sender`` nodes is set in the
example's parameter file (``192.168.1.41:5000`` in the distributed setups); adapt it to the IP of
your headless machine.

.. _usage_configuration:

Configuration
-------------

Every node loads its parameters in three layers:

1. ``config/default.yaml`` of its own package (the package defaults),
2. ``params_file``: the parameter file of the example, e.g.
   ``ufil_examples_cpm_lab/config/cpm-lab.yaml``, with one section per node,
3. ``local_params_file``: machine-specific overrides (defaults to ``params_file``).

Later layers only need the values that differ. The example parameter files are loaded with launch
substitutions (``allow_substs``), so they may reference installed files with
``$(find-pkg-share <package>)``. All launch files accept ``use_sim_time``, ``params_file`` and
``local_params_file``:

.. code-block:: bash

   ros2 launch ufil_examples_cpm_lab cpm-lab_headless.launch.xml \
     use_sim_time:=false local_params_file:=/path/to/my_overrides.yaml

Most parameters are read-only and validated when the node starts; an invalid value is logged as
fatal and the node does not start.

Diagnostics
~~~~~~~~~~~

The Ufil nodes publish their status on ``/diagnostics`` (received, published and dropped
messages, transform errors, timing). With ``diagnostic_updater.use_fqn: true`` (the default) the
entries are prefixed with the node namespace, so several sensor nodes or vehicles can be told
apart. Inspect them with ``ros2 topic echo /diagnostics`` or the diagnostics panel of Foxglove.

.. _usage_visualization:

Visualization
-------------

Ufil does not ship custom RViz plugins. Instead, ``ufil_visualization`` converts object lists and
Lanelet2 maps into standard ``visualization_msgs/MarkerArray`` messages, which every frontend can
display (see :ref:`packages_core`). In all examples the head machine publishes:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Topic
     - Content
   * - ``/map``
     - Lanelet2 map of the example (lanes, crosswalks, areas)
   * - ``/obu/object_markers``
     - Objects of the on-board units (ground truth of the vehicles)
   * - ``/osn/object_markers``
     - Tracks of the outdoor sensor node
   * - ``/ssl/object_markers``
     - Vehicles detected by the sensitive surface layer
   * - ``/rsu/cam/object_markers``
     - Objects decoded from the received CAMs
   * - ``/rsu/object_markers``
     - Fused object list of the road side unit

Each object is drawn as a box with its body axes, a velocity arrow, the two-sigma position
ellipse, an orientation uncertainty ellipse and a label ``<id> | <class> | <existence>``.

.. figure:: ../images/placeholders/object_markers_20261104.*
    :width: 720px
    :align: center
    :alt: object markers

    *Placeholder* – Close-up of one object as drawn by ufil_visualization, with box, axes, velocity arrow, covariance ellipses and label annotated

Foxglove
   Start the ``foxglove-bridge`` profile (or ``ros2 launch ufil_viz_helpers foxglove-bridge.launch.xml``)
   and connect Foxglove to ``ws://localhost:8765``. Add a 3D panel and enable the marker topics.

RViz
   Start the ``rviz`` profile (or ``ros2 launch ufil_viz_helpers rviz.launch.xml``). Allow the
   container to use your X server first, e.g. ``xhost +local:``. Set the fixed frame to ``map``
   and add a *MarkerArray* display per topic.

Lichtblick
   The ``lichtblick/`` directory of the workspace contains a standalone Docker Compose setup of the
   `Lichtblick <https://github.com/lichtblick-suite/lichtblick>`_ web visualization with a Ufil
   layout and an extension that converts Ufil object lists:

   .. code-block:: bash

      cd lichtblick
      cp .env.example .env
      docker compose up --build

   The web UI is served at ``http://localhost:8080`` and connects to the Foxglove bridge at
   ``ws://localhost:8765``.

Coordinate Frames
-----------------

The examples publish their static frames with ``robot_state_publisher`` from the URDF files in
the ``urdf/`` directory of each example package. Three kinds of frames appear in every example:

``utm_<zone>``
   The UTM frame of the deployment (``utm_32n`` for CARLA, the CPM Lab and the pedestrian example,
   ``utm_12n`` for Edmonton). The on-board units transform their objects into this frame to
   compute the WGS84 position of the CAM.
``map``
   The local metric frame of the deployment. Trackers, the central fusion, the area filters and
   the RSU output work in this frame. It may be rotated against UTM (e.g. 30° in the pedestrian
   example, -1.19 rad in the CPM Lab).
``map_utm``
   The local origin, axis-aligned with UTM. The Lanelet2 maps are drawn in this frame.

Sensor frames (``sensor_node_base``, ``sensor_node``, ``lidar``, ``osn``, ``ssl_frame_<id>``, ...) hang
below ``map``. For the pedestrian example the chain is
``utm_32n → map_utm → map → osn``; check the URDF of an example for its exact tree.
