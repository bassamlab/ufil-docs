.. _install_from_source_via_docker:

Installation from Source with Docker (Containerized ROS 2)
===========================================================

This guide explains how to install **Ufil** using Docker with a
containerized ROS 2 environment. This approach avoids modifying your
host ROS installation and keeps all dependencies isolated.

Prerequisites
-------------

Before installing Ufil, ensure Docker is installed on your system.

Follow the official installation guide for your platform:

- `Docker Installation Guide <https://docs.docker.com/engine/install/>`_

After installation, verify Docker is working:

.. code-block:: bash

   docker --version


Building Ufil from Source
--------------------------

1. Clone the Ufil Workspace
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone the Ufil workspace repository:

.. code-block:: bash

   git clone <link-to-ufil-workspace-git> ufil_ws
   cd ufil_ws


2. Build the Docker Image
~~~~~~~~~~~~~~~~~~~~~~~~~~

The repository provides a development Docker image.

You can either use the VS Code Dev Container integration
or build the image manually:

.. code-block:: bash

   ./docker/create_image.bash


3. Build the Ufil Workspace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build the workspace inside the container:

.. code-block:: bash

   ./docker/build_workspace.bash


4. Verify the Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start a container shell and verify that the Ufil packages are available:

.. code-block:: bash

   ./docker/run_terminal.bash
   source install/setup.bash
   ros2 pkg list | grep ufil


If Ufil packages are listed, the installation was successful.


You're Done
-----------

Your containerized development environment is now ready.

You can start developing new features, running simulations,
or contributing to the Ufil ecosystem.

If you encounter issues, refer to the
:ref:`Troubleshooting Guide <installation_troubleshooting>`.


Helpful Commands
-----------------

Debug Build
~~~~~~~~~~~

To build Ufil in debug mode (useful for development or troubleshooting),
clean the workspace first:

.. code-block:: bash

   make clean
   make debug


Build Specific Components
~~~~~~~~~~~~~~~~~~~~~~~~~

You can build specific parts of Ufil:

- **Core functionality**

  .. code-block:: bash

     make core

- **Inroad sensing**

  .. code-block:: bash

     make ssl


Clean the Workspace
~~~~~~~~~~~~~~~~~~~

To remove build artifacts:

.. code-block:: bash

   make clean