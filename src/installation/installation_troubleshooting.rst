.. _installation_troubleshooting:

Installation Troubleshooting
================================

This page provides a collection of troubleshooting tips and solutions for common issues encountered while building or using Ufil.

The topics are loosely grouped by category to help you quickly identify and resolve known problems.

Common Issues
---------------

Missing ``ament_cmake`` Package
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

Additional Notes
----------------

- **Working with Python Files**

  If you are working with Python files in Ufil, add the ``--symlink-install`` flag to the ``COLCON_ARGS`` in the Makefile for easier development. Modify the line as follows:

  .. code-block:: make

     COLCON_ARGS := --merge-install --symlink-install --parallel-workers 2 --cmake-force-configure

- **General Tip**

  Consider adding ``source /opt/ros/jazzu/setup.bash`` and ``source ~/ufil_ws/install/setup.bash`` to your shell's startup script (e.g., ``~/.bashrc``) to avoid manually sourcing them every time you open a new terminal.
