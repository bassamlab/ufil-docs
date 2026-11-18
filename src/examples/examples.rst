.. _examples:

Examples
========

The examples are complete deployments of Ufil. Each one combines adapters for its data source,
the Ufil components and the visualization, and can be run end to end. They live in the
``ufil-examples`` component; the meta package ``ufil_examples`` installs all of them.

.. list-table::
   :header-rows: 1
   :widths: 15 35 35 15

   * - Example
     - Data source
     - Ufil components
     - Compose profile
   * - :doc:`CARLA <carla/carla>`
     - CARLA simulator (live) or recorded bags; highway and intersection scenario
     - OBU (7 vehicles), OSN, SSL (simulated mat), RSU
     - ``carla-highway``
   * - :doc:`CPM Lab <cpm_lab/cpm_lab>`
     - Cyber-Physical Mobility Lab (live) or recorded bags
     - OBU (6 vehicles), OSN, SSL (2 mats), RSU
     - ``cpm-lab``
   * - :doc:`Pedestrian <pedestrian/pedestrian>`
     - Built-in pedestrian scenario simulator, no external data
     - OSN tracker
     - ``pedestrian``

The CARLA and CPM Lab examples implement the same :doc:`complex scenario <complex_scenario>`, a
full infrastructure-based perception system with all Ufil components.

If you just want to see Ufil running, start with the :doc:`pedestrian example
<pedestrian/pedestrian>`: it needs no simulator, testbed or recorded data.

Structure
---------

Every example consists of a *bringup* package ``ufil_examples_<name>`` with

- ``launch/``: ``<name>_head.launch.xml``, ``<name>_headless.launch.xml`` and the single-machine
  ``<name>.launch.xml`` (see :ref:`usage_distributed`),
- ``config/<name>.yaml``: the parameters of all nodes, one section per node, and
  ``config/<name>_local.yaml`` with the single-machine overrides,
- ``urdf/``: the static frames of the deployment (sensor poses, UTM origin),
- ``maps/``: the Lanelet2 map shown in the visualization,

plus adapter packages that convert the data of the source into Ufil object lists (e.g.
``ufil_examples_carla_adapter``).

Workflow
--------

1. Build the workspace (see :doc:`../installation/installation`).
2. Start the example, either with Docker Compose

   .. code-block:: bash

      COMPOSE_PROFILES=<profile>,foxglove-bridge docker compose up

   or in a sourced workspace

   .. code-block:: bash

      source install/setup.bash
      ros2 launch ufil_examples_<name> <name>.launch.xml

3. Provide the data: start the simulator or testbed, or replay a bag
   (``ros2 bag play <bag> --clock``, or the ``bag`` compose profile).
4. Inspect the results in Foxglove, RViz or Lichtblick (see :ref:`usage_visualization`).

.. note::
   The launch files default to ``use_sim_time:=true`` (except the pedestrian example), because
   they are mostly used with the simulator or with recorded bags that publish ``/clock``. For live
   data from a testbed, pass ``use_sim_time:=false``.

.. toctree::
   :caption: Contents:
   :maxdepth: 1

   Complex Scenario: Full System <complex_scenario>
   CARLA <carla/carla>
   Cyber-Physical Mobility Lab <cpm_lab/cpm_lab>
   Pedestrian Simulation <pedestrian/pedestrian>

