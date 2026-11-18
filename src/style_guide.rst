.. _style_guide:

Style Guide
================

This project uses the ROS2 style guide as a base. The following section describes alterations to said style guide.

The ROS2 style guide can be found at: https://docs.ros.org/en/jazzy/The-ROS2-Project/Contributing/Code-Style-Language-Versions.html

Directory Naming Conventions
----------------------------

The following naming conventation only hold true for directories in the `src` directory.

- Use `snake_case` for packages.
- Use `kebab-case` for directories.
- Use `ufil` prefix for directories containing packages.
- Do not use the `ufil` prefix for directories not containing packages, like the `launch` directory inside of a package.

File Naming Conventions
----------------------------

- Use `snake_case` for file names.
- Use the `<package-name>` as a prefix and `node` as a suffix for files containing a ROS 2 node, e.g. a node in the `ufil_osn` package should be named `ufil_osn_<name-of-node>_node.cpp`. The name of the executable should be the same as the file name without the `.cpp` suffix.

Package Layout
--------------

All packages follow the same structure, so that algorithms stay testable without ROS 2 and every
node can be started and configured the same way:

.. code-block:: text

   <package>/
   ├── include/<package>/   # ROS-independent core library (public headers)
   ├── src/                 # ROS-independent core library (implementation)
   ├── component/           # ROS 2 layer: parameters, message conversion, rclcpp component
   ├── config/default.yaml  # default parameters of every node of the package
   ├── launch/              # default.launch.xml and further launch files
   ├── test/                # unit tests of the core library and the component
   ├── CHANGELOG.rst
   ├── CMakeLists.txt
   └── package.xml

- Nodes are ``rclcpp`` components registered with ``rclcpp_components_register_node``; the
  plugin is ``<package>::<Name>Node`` and the generated executable ``<name>_node``.
- The core library has no ROS 2 dependency. Use ``ufil_ros`` for conversions between
  ``ufil_object_tracking`` types and messages.
- Parameters are declared in the component, read-only unless they are meant to change at runtime,
  and validated at start-up; invalid values are logged as fatal and the construction fails.
- Every node publishes diagnostics on ``/diagnostics`` with ``diagnostic_updater`` (parameters
  ``diagnostic_updater.period`` and ``diagnostic_updater.use_fqn``).
- ``launch/default.launch.xml`` starts the package with ``config/default.yaml``; further parameter
  files are loaded on top, so they only contain the values that differ.
- Changes are documented in ``CHANGELOG.rst`` (ROS 2 changelog format).
- The C++ standard is C++20.

VSCode Helper Tasks
----------------------------
The workspace contains a `.vscode` directory with helper tasks to make development easier. The
check and lint tasks mirror the jobs executed by the CI pipelines of the component repositories.

Usage
+++++++++++++++++++++++++++++
These tasks can be executed from the command palette in VSCode by searching for "Tasks: Run Task" and selecting the desired task.

They will be executed in the context of the component of the file that is currently open in the editor. If no file is open, the tasks will be executed in the context of the workspace.

Tasks
++++++++++++++++++++++++++++

The tasks can be found in the `tasks.json` file and are the following:

- `colcon:build`: Builds the workspace.
- `test:all`: Runs the tests of all packages.
- `test:current`: Runs the tests of the package of the currently open file.
- `lint:xml`: Lints XML files using `ament_xmllint`.
- `lint:cmake`: Lints CMake files using `ament_lint_cmake`.
- `lint:cpp`: Lints C++ files using `ament_cpplint`.
- `check:copyright`: Checks copyright headers in source files for compliance with the project's copyright policy.
- `check:uncrustify`: Checks C++ files for formatting using `ament_uncrustify`.
- `check:cpp`: Checks C++ files for style issues using `ament_cpplint`.

In addition, some tasks are provided to perform some of the formatting tasks automatically:

- `format:copyright`: Adds copyright headers to source files.
- `format:uncrustify`: Formats C++ files inplace using `ament_uncrustify`.

To ease execution of these tasks, they can be executed in groups with the following commands:

- `format:all`: Runs all formatting tasks.
- `check:all`: Runs all check tasks.

