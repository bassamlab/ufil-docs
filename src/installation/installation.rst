.. _installation:

Installation
============



Ufil is a ROS 2 workspace. The repository `bassamlab/ufil <https://github.com/bassamlab/ufil>`_
contains all Ufil components and ships a Docker setup, a dev container and a ``Makefile`` for
building.

Ufil targets **ROS 2 Jazzy** on **Ubuntu 24.04** (amd64 and arm64). There are three ways to get a
working installation:

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Option
     - Use it when
     - Requirements
   * - :ref:`Docker Compose <installation_docker>` (recommended)
     - You want to run the examples or deploy Ufil without installing ROS 2 on the host.
     - Docker with Compose v2
   * - :ref:`Dev container <installation_devcontainer>`
     - You develop Ufil in VS Code.
     - Docker, VS Code, Dev Containers extension
   * - :ref:`Native build <installation_native>`
     - You need Ufil directly on the host, e.g. on a sensor node.
     - Ubuntu 24.04 with ROS 2 Jazzy

All three use the same dependencies: the container images are built from
``docker/Dockerfile`` of the workspace, and the native build installs the same packages.

.. note::
   Installation from ``.deb`` packages is not available yet.

Get the Workspace
-----------------



Clone the workspace from GitHub:

.. code-block:: bash

   git clone https://github.com/bassamlab/ufil.git ufil_ws
   cd ufil_ws

To get a specific release, check out one of its tags (``git tag`` lists them), e.g.
``git checkout <version>``.

The workspace has the following layout:

.. code-block:: text

   ufil_ws/
   ├── docker/                 # Dockerfile, pinned Python requirements
   ├── docker-compose.yaml     # build, terminal, bag, router, visualization and example services
   ├── .devcontainer/          # VS Code dev container
   ├── lichtblick/             # optional Lichtblick web visualization stack
   ├── evaluation/             # Python scripts for the evaluation of recorded runs
   ├── Makefile                # colcon shortcuts
   └── src/
       ├── ufil-core/          # tracking library, messages, bridges, visualization
       ├── ufil-osn/           # outdoor sensor node
       ├── ufil-rsu/           # road side unit (central fusion)
       ├── ufil-obu/           # on-board unit
       ├── ufil-ssl/           # sensitive surface layer
       ├── ufil-tools/         # bag and map tools
       └── ufil-examples/      # example deployments (CARLA, CPM Lab, pedestrian, ...)

See :doc:`../concept/packages` for the content of each component.

.. _installation_docker:

Option 1: Docker Compose
------------------------



The runtime image contains ROS 2 Jazzy and every dependency of the workspace.

1. **Build the runtime image** (takes a while, it installs PyTorch and the ROS dependencies):

   .. code-block:: bash

      docker compose build foxglove-bridge

   All services share the same image, so building it for one service is enough.

2. **Build the workspace** inside the image. The source tree is mounted into the container, so
   ``build/``, ``install/`` and ``log/`` end up in the workspace on the host:

   .. code-block:: bash

      docker compose --profile build up

   The ``build`` service runs ``make sequential``, which builds one package at a time to keep
   the memory consumption low.

3. **Run something**, e.g. the pedestrian example with Foxglove:

   .. code-block:: bash

      COMPOSE_PROFILES=pedestrian,foxglove-bridge docker compose up

   Open `Foxglove <https://app.foxglove.dev>`_ and connect to ``ws://localhost:8765``.

:doc:`../usage/usage` explains the profiles, the middleware selection and how to split an example
across machines.

For an interactive shell in the runtime image, use the ``terminal`` profile:

.. code-block:: bash

   docker compose --profile terminal run --rm terminal
   source install/setup.bash

.. _installation_devcontainer:

Option 2: Dev Container
-----------------------

The dev container uses the ``dev`` stage of ``docker/Dockerfile``: the runtime image plus a
non-root user ``ufil``, compilers, ``gdb`` and Git. Development, CI and deployment therefore share
the same dependencies.

1. Create ``.devcontainer/.env`` with the values used by ``.devcontainer/docker-compose.yml``:

   .. code-block:: bash

      ROS_DOMAIN_ID=21
      BAGS_DIR=/absolute/path/to/your/bags   # mounted read-only at /bags



2. Open the workspace in VS Code and run **Dev Containers: Reopen in Container**. The image is
   built locally on the first start.

3. The post-create script runs ``rosdep install`` for all packages. Build with the VS Code task
   ``colcon:build`` or with ``make`` in the integrated terminal (see :ref:`make_targets`).

The workspace is mounted at ``/home/ufil/ws``; port ``8765`` (Foxglove bridge) is forwarded to
the host.

.. _installation_native:

Option 3: Native Build
----------------------

1. **Install ROS 2 Jazzy** following the
   `official guide <https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html>`_ and
   source it:

   .. code-block:: bash

      source /opt/ros/jazzy/setup.bash

2. **Install the dependencies.** ``make dependencies`` resolves all ``package.xml`` dependencies
   with ``rosdep`` (requires ``sudo``):

   .. code-block:: bash

      sudo rosdep init   # only once per machine
      make dependencies

   The YOLO classifier of the outdoor sensor node additionally needs the Python packages in
   ``docker/requirements.txt`` (Ultralytics, PyTorch). Install them with the pinned versions:

   .. code-block:: bash

      make venv && . ./venv/bin/activate
      pip install -c docker/constraints.txt -r docker/requirements.txt

   ``make venv`` creates a virtual environment with access to the system site packages, so the
   ROS 2 Python packages stay visible.

3. **Build** the workspace:

   .. code-block:: bash

      make

4. **Verify** the installation:

   .. code-block:: bash

      source install/setup.bash
      ros2 pkg list | grep ufil

.. tip::
   Add ``source /opt/ros/jazzy/setup.bash`` and ``source ~/ufil_ws/install/setup.bash`` to your
   ``~/.bashrc`` to avoid sourcing them in every new terminal.

.. _make_targets:

Makefile Targets
----------------

All targets call ``colcon build`` with ``--symlink-install`` (Python and launch files can be edited
without rebuilding) in release mode unless stated otherwise.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Target
     - Builds
   * - ``make`` / ``make build``
     - the whole workspace with 4 parallel workers
   * - ``make sequential``
     - the whole workspace one package at a time, without tests (used by the Docker ``build`` service)
   * - ``make debug``
     - the whole workspace in debug mode
   * - ``make core`` / ``osn`` / ``rsu`` / ``obu`` / ``ssl`` / ``tools`` / ``examples``
     - a component and its dependencies (``--packages-up-to ufil_<component>``)
   * - ``make example_cpm_lab`` / ``example_pedestrian`` / ``example_uofa``
     - a single example and its dependencies
   * - ``make clean``
     - removes ``build/``, ``install/`` and ``log/``
   * - ``make dependencies``
     - installs the system dependencies with ``rosdep``
   * - ``make venv``
     - creates the Python virtual environment ``venv/``

.. hint::
   Heavy packages such as ``ufil_osn_tracker`` need a lot of memory to compile. If the compiler
   gets killed, use ``make sequential``.

Container Images
----------------

``docker/Dockerfile`` defines all images:

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Stage
     - Content
   * - ``runtime``
     - ROS 2 Jazzy (without the desktop meta-package) with all workspace dependencies, CPU-only
       PyTorch and the pinned Python packages. Used by CI and ``docker-compose.yaml``.
   * - ``dev``
     - ``runtime`` plus the non-root user ``ufil`` and development tools. Used by the dev
       container.

Dependencies are pinned for reproducible builds:

- **Base image:** ``ros:jazzy`` is pinned by digest (``ROS_IMAGE`` in the Dockerfile).
- **Python packages:** top-level packages go into ``docker/requirements.txt``; the exact versions
  for amd64 and arm64 are in ``docker/constraints.txt``. After changing the requirements, run
  ``docker/update-python-lock.sh`` (needs Docker buildx) and commit both files.
- **ROS packages:** add them to the ``apt-get install`` list in the Dockerfile. The CI job
  ``rosdep-check`` fails if a ``package.xml`` declares a dependency that the runtime image lacks.


Troubleshooting
---------------

**CMake cannot find** ``ament_cmake``

.. code-block:: text

   CMake Error at CMakeLists.txt:15 (find_package):
     By not providing "Findament_cmake.cmake" in CMAKE_MODULE_PATH...

ROS 2 is not sourced in the terminal. Run ``source /opt/ros/jazzy/setup.bash`` and build again.

**The compiler is killed during the build**

The machine ran out of memory. Build with ``make sequential`` or reduce
``--parallel-workers`` in the ``Makefile``.

**Nodes in different containers or on different machines do not see each other**

All participants must use the same ``RMW_IMPLEMENTATION`` and ``ROS_DOMAIN_ID``; with Zenoh they
also need to reach the same router. See :ref:`usage_middleware`.

**General checks**

.. code-block:: bash

   ros2 doctor
   ros2 pkg list | grep ufil
