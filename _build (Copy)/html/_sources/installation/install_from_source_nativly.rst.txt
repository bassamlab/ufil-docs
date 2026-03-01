.. _install_from_source_natively:

Installation from Source with Native ROS 2
==========================================

This guide explains how to install **Ufil** natively on your system
using a locally installed ROS 2 environment.

Unlike the Docker-based setup, this method installs dependencies
directly on your host system. It is recommended for advanced users
who require full system integration.

.. warning::

   On Ubuntu 24.04 and newer, this installation method may interfere
   with other system dependencies due to limitations in the ``rosdep``
   pip installation process.

   Carefully review your Python and ROS dependency setup before proceeding.


Prerequisites
-------------

Before installing Ufil, ensure the following requirements are met.


1. Install ROS 2
~~~~~~~~~~~~~~~~

Ufil requires **ROS 2 Jazzy or newer**.

Follow the official installation guide for your distribution:

- `ROS 2 Jazzy Installation Guide <https://docs.ros.org/en/jazzy/Installation.html>`_

After installation, verify your ROS 2 setup:

.. code-block:: bash

   ros2 --version


2. Source ROS 2
~~~~~~~~~~~~~~~

After installing ROS 2, source the environment:

.. code-block:: bash

   source /opt/ros/<ros2-distro>/setup.bash

Replace ``<ros2-distro>`` with your installed distribution
(e.g., ``jazzy``).

.. note::

   If you are using a different shell, adapt the command accordingly:

   - Zsh: ``source /opt/ros/<ros2-distro>/setup.zsh``
   - Fish: ``source /opt/ros/<ros2-distro>/setup.fish``


Building Ufil from Source
--------------------------

1. Clone the Ufil Workspace
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone the workspace repository:

.. code-block:: bash

   git clone <link-to-ufil-workspace-git> ufil_ws
   cd ufil_ws


2. Create and Activate a Python Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ufil currently relies on Python dependencies that may conflict with
system-installed packages. To avoid conflicts, use a virtual environment.

.. code-block:: bash

   # Create environment
   python3 -m venv venv --system-site-packages --symlinks

   # Activate environment
   source venv/bin/activate

.. note::

   The virtual environment requirement is temporary and may be removed
   in future releases.


3. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

Install all required ROS 2 and system dependencies:

.. code-block:: bash

   make dependencies


4. Build Ufil
~~~~~~~~~~~~~

Build the workspace:

.. code-block:: bash

   make


5. Verify the Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~

After building, source the workspace and verify the packages:

.. code-block:: bash

   source install/setup.bash
   ros2 pkg list | grep ufil

If Ufil packages are listed, the installation was successful.


You're Done
-----------

Your native development environment is now ready.

You can begin developing new features, running simulations,
or contributing to the Ufil ecosystem.

If you encounter issues, refer to the
:ref:`Troubleshooting Guide <installation_troubleshooting>`.


Helpful Commands
-----------------

Debug Build
~~~~~~~~~~~

To build Ufil in debug mode:

.. code-block:: bash

   make clean
   make debug


Build Specific Components
~~~~~~~~~~~~~~~~~~~~~~~~~

You can build individual components:

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