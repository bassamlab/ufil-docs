.. _installation:

Installation 
==================

Ufil is a collection of ROS2 packages designed to facilitate infrastructure-based localization and state estimation. It provides a pre-configured workspace and a Makefile to simplify building, cleaning, and dependency management.

**Installation Options**

1. Building from source using the provided workspace (recommended for developing Ufil).
2. Installing from .deb files (recommended for using Ufil in your own project).

.. warning:: 
   While Ufil will support .deb file installation, this is currently a work in progress. For now, we recommend building from source using the provided workspace.

Prerequisites
-------------

Before installing Ufil, ensure the following steps are completed:

1. **Install ROS2**
   
   Ufil requires ROS2 Jazzy or newer. Follow the official installation guide for your version:
   
   - `ROS2 Jazzy Installation Guide <https://docs.ros.org/en/jazzy/Installation.html>`_

2. **Source ROS2**

   After installing ROS2, source its setup file:
   
   .. code-block:: bash

      source /opt/ros/<ros2-distro>/setup.bash

   Replace ``<ros2-distro>`` with your distribution based on your installation.

   .. note::
      If you're using a shell other than Bash, adapt the command accordingly (e.g., ``source /opt/ros/<ros2-distro>/setup.zsh``).



Building Ufil from Source
--------------------------

1. **Clone the Ufil Workspace**

   Clone the Ufil workspace to your system. This workspace contains all the necessary files and a Makefile for simplified setup:

   .. code-block:: bash

      git clone --recurse-submodules <link to ufil workspace git> ufil_ws
      cd ufil_ws

   
   .. hint::
      If you forgot to use ``--recurse-submodules``, run the following command to initialize and update submodules:
      
      .. code-block:: bash

         git submodule update --init --recursive

   .. hint::
      When you check out the submodule, it will initially point to a specific commit rather than a branch. 
      To develop using ufil, you'll need to manually check out the appropriate branches.

      .. code-block:: bash

         git checkout main

2. **Create Virtual Environment**

   We are using a virtual python environment to manage our dependencies. We plan to remove all python dependencies in the future but for now, this is required to avoid conflicts with the  packages. Create and activate the virtual environment using the following commands:

   .. code-block:: bash

      # Create environment
      python3 -m venv venv --system-site-packages --symlinks

      # Use environment
      . ./venv/bin/activate

   

3. **Install Dependencies**

   Use the Makefile to install all required ROS2 dependencies:

   .. code-block:: bash

      make dependencies

   .. hint::
      This step may require ``sudo`` permissions to install system dependencies.

4. **Build Ufil**

   Use the Makefile to build Ufil:

   .. code-block:: bash

      make

   .. hint::
      If you encounter issues or warnings during the build, make sure all dependencies are installed and ROS2 is correctly sourced.

5. **Optional: Debug Build**

   To build Ufil in debug mode (useful for development or troubleshooting), first clean the workspace:

   .. code-block:: bash

      make clean
      make debug

6. **Optional: Build Specific Packages**

   You can also build specific components of Ufil:

   - **Core functionality** (essential Ufil features):

     .. code-block:: bash

        make core

   - **Inroad sensing**:

     .. code-block:: bash

        make ssl

   - ...

7. **Clean the Workspace**

   If needed, clean the workspace using:

   .. code-block:: bash

      make clean

8. **Verify Installation**

   After building, verify that the Ufil packages are correctly installed:

   .. code-block:: bash

      source install/setup.bash
      ros2 pkg list | grep ufil


Additional Notes
----------------

- **Working with Python Files**

  If you are working with Python files in Ufil, add the ``--symlink-install`` flag to the ``COLCON_ARGS`` in the Makefile for easier development. Modify the line as follows:

  .. code-block:: make

     COLCON_ARGS := --merge-install --symlink-install --parallel-workers 2 --cmake-force-configure

- **General Tip**

  Consider adding ``source /opt/ros/jazzu/setup.bash`` and ``source ~/ufil_ws/install/setup.bash`` to your shell's startup script (e.g., ``~/.bashrc``) to avoid manually sourcing them every time you open a new terminal.


Troubleshooting
---------------

Common Issue: Missing ``ament_cmake`` Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Error Message**:

  .. code-block:: text

     CMake Error at CMakeLists.txt:15 (find_package):
       By not providing "Findament_cmake.cmake" in CMAKE_MODULE_PATH...

- **Cause**:

  This occurs when ROS2 is not sourced in the terminal before running the command.

- **Solution**:

  Ensure you source ROS2 by running:

  .. code-block:: bash

     source /opt/ros/<ros2-distro>/setup.bash

  Always run this command in every new terminal session or add it to your shell’s startup script (e.g., ``~/.bashrc``).

Other Suggestions
~~~~~~~~~~~~~~~~~

- Ensure all system dependencies for ROS2 are installed. The installation guide linked above provides instructions for setting up your environment.
- Verify your ROS2 installation by running:

  .. code-block:: bash

     ros2 doctor
