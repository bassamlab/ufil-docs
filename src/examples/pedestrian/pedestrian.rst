.. _examples_pedestrian:

Pedestrian Simulation
=====================

The pedestrian example needs no simulator, testbed or recorded data. A lightweight scenario
simulator replays pedestrians walking on the sidewalks and crosswalks of a synthetic intersection
and publishes their ground truth and noisy detections; the tracker of an outdoor sensor node
tracks the detections. The scenarios cover typical challenges of multi-object tracking, which
makes the example the quickest way to see Ufil running and a test bench for tracker changes.

Running the Example
-------------------

With Docker Compose (after building the workspace, see :doc:`../../installation/installation`):

.. code-block:: bash

   COMPOSE_PROFILES=pedestrian,foxglove-bridge docker compose up

Select another scenario with ``PEDESTRIAN_SCENARIO``:

.. code-block:: bash

   PEDESTRIAN_SCENARIO=group.yaml COMPOSE_PROFILES=pedestrian,foxglove-bridge docker compose up

In a sourced workspace:

.. code-block:: bash

   ros2 launch ufil_examples_pedestrian pedestrian.launch.xml scenario:=crossing.yaml

The example runs in wall-clock time (``use_sim_time`` defaults to ``false``). Connect Foxglove to
``ws://localhost:8765`` and show the marker topics of the table below. The simulator stops
publishing at the end of the scenario (``runtime``); restart the example to replay it.

.. figure:: ../../images/placeholders/pedestrian_foxglove_20261104.*
    :width: 720px
    :align: center
    :alt: pedestrian example in Foxglove

    *Placeholder* – Screenshot of the 3D panel: the four-way intersection map with ground truth, detections and tracks of the crossing scenario in distinct colors

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Topic
     - Content
   * - ``/ufil_examples_pedestrian/reference_objects``
     - Ground truth: every existing pedestrian
   * - ``/ufil_examples_pedestrian/measured_objects``
     - Detections: ground truth with position noise, missed detections, occlusions and clutter
   * - ``/osn/object_list``
     - Tracks of the pedestrian tracker
   * - ``/ufil_examples_pedestrian/reference_markers``, ``/ufil_examples_pedestrian/measured_markers``,
       ``/osn/object_markers``
     - The three object lists as markers
   * - ``/map``
     - The Lanelet2 intersection as markers

Like the other examples it is split into ``pedestrian_head.launch.xml`` (transforms and
visualization) and ``pedestrian_headless.launch.xml`` (simulator and tracker).

Scenarios
---------

All scenarios use the sidewalks and crosswalks of the example map. They are located in
``ufil_examples_pedestrian_simulator/config``:

.. list-table::
   :header-rows: 1
   :widths: 18 52 30

   * - Scenario
     - Pedestrians
     - Tracker challenge
   * - ``crossing.yaml``
     - 2 enter at the west/east border, walk along the sidewalks, cross the junction diagonally
       (passing 1.2 m apart at its center) and leave along the far sidewalks; 2 more appear later
     - crossing paths, track start/end
   * - ``parallel.yaml``
     - 2 enter side by side at the south border, walk north along the west sidewalk and over the
       west crosswalk and leave at the north border; 2 more appear later
     - closely spaced targets, track start/end
   * - ``passing.yaml``
     - 2 enter at opposite borders, walk towards each other along the east sidewalk, pass on the
       east crosswalk and leave at the opposite border; 2 more appear later
     - opposing targets passing closely, track start/end
   * - ``waiting.yaml``
     - 2 wait at the curb (6 s and 3 s) before crossing; 1 walks past without stopping
     - stop-and-go, zero velocity
   * - ``group.yaml``
     - 4 walk in a tight 2 x 2 formation over the east crosswalk, then split up
     - association ambiguity, track splitting
   * - ``appearing.yaml``
     - 6 enter and leave the scene at different times
     - track initialization and termination
   * - ``occlusion.yaml``
     - 2; one is undetected for 3 s mid-crosswalk, and 15 % of all detections are missed
     - coasting through gaps
   * - ``overtaking.yaml``
     - a jogger (3 m/s) overtakes a slow walker (1 m/s) and merges back in front of it
     - different speeds, lateral manoeuvre
   * - ``clutter.yaml``
     - 2, plus on average 2 false detections per step anywhere on the map
     - false positive rejection
   * - ``crowd.yaml``
     - 8 with staggered starts on all sidewalks and crosswalks, 1 to 2 m/s
     - many targets, opposing flows

Scenario Files
~~~~~~~~~~~~~~

A scenario is a YAML file. The ``waiting`` scenario, shortened to one agent:

.. code-block:: yaml

   name: waiting
   runtime: 37                 # duration of the scenario [s]
   error_covariance: 0.1       # position noise of the detections
   agents:
     - id: 1
       dimension: {width: 1.0, length: 1.0, height: 1.0}
       waypoints:              # position [x, y] in the map frame [m], time [s]
         - {position: [0.5, 12.5], time: 0}
         - {position: [16.5, 12.5], time: 11.43}
         - {position: [16.5, 13.4], time: 12.07}
         - {position: [16.5, 13.4], time: 18.07}   # same position later: stands for 6 s
         - {position: [16.5, 39.5], time: 36.71}

Per agent:

- either a ``starting``/``stopping`` pair or a list of timed ``waypoints``; an agent only exists
  between its first and last waypoint time. Repeating a position with a later time makes it stand
  still.
- ``orientation`` (optional): if omitted, the agent faces its walking direction and keeps that
  heading while standing.
- ``occlusions`` (optional): list of ``start``/``end`` times [s] during which its detections are
  suppressed.

Per scenario (optional):

- ``detection_probability`` (default 1.0) for random missed detections,
- ``clutter``: ``mean_count`` false detections per step, uniformly distributed within
  ``area: [x_min, y_min, x_max, y_max]``,
- ``seed`` for reproducible noise.

The ground truth always contains every existing agent; missed detections and clutter only affect
the detections. Pass an own file with an absolute path:
``ros2 launch ufil_examples_pedestrian pedestrian.launch.xml scenario:=/path/to/my_scenario.yaml``.

Map and Frames
--------------

The head launch file publishes a synthetic four-way Lanelet2 intersection
(``maps/four_way_intersection.osm``) on ``/map`` in the ``map_utm`` frame. The 40 x 40 m square
contains

- a major east-west road (two 3 m lanes per direction) with a zebra crosswalk continuing each
  minor-road sidewalk across it,
- a minor north-south road (one 3 m lane per direction) whose approaches yield to the major road
  at stop lines,
- 2 m sidewalks on both sides of each road and vegetation in the four corners.

Roads have straight connections only and no traffic lights.

The local ``map`` origin is the southwest corner; the intersection and the pedestrian
trajectories are centered at ``(20, 20)``. The TF chain is ``utm_32n → map_utm → map → osn``:
``map_utm`` is translated to UTM32N ``(696303.25, 5328527.39)`` and ``map`` is rotated by 30°
about z relative to ``map_utm``. The OSM coordinates use the same translation and rotation, so
map markers and pedestrian objects align in either frame. The layout is a demo, not a survey of
that location.

Tracker
-------

``ufil_examples_pedestrian_tracker`` is a minimal :ref:`multi-target tracker <tracking_pipeline>`:
random walk motion model, Wasserstein distance with Hungarian association, Kalman filter and
dimension grid map updates, and timed track deletion. Its source is the reference example of the
tracking pipeline. Parameters (``config/pedestrian.yaml``):

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Default
     - Meaning
   * - ``process_noise``
     - 10.0
     - Process noise of the random walk model per axis
   * - ``track_timeout``
     - 1.0
     - Tracks without an associated detection for this long are deleted [s]
   * - ``max_time_gap``
     - 1.0
     - A larger gap between two detection stamps, or a jump back in time, resets the tracker [s]

The simulator publishes every ``timestep`` (default 0.1 s) in ``frame_id`` (default ``map``).

Comparing Trackers
~~~~~~~~~~~~~~~~~~

Because ground truth and tracks are published side by side, the scenarios can be used to compare
tracker configurations, e.g. distance measures and association algorithms. Record the topics,
convert the bag with ``ufil_hdf_converter`` and evaluate it with the scripts in ``evaluation/``
(see :ref:`packages_tools`).
