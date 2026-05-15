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
- Use the `<package-name>` as a prefix and `node` as a suffix for files containing a ROS2 nodem e.g. a node in the `ufil_osn` package should be named `ufil_osn_<name-of-node>_node.cpp`. The name of the executable should be the same as the file name without the `.cpp` suffix.

VSCode Helper Tasks
----------------------------
The project contains a `.vscode` directory with helper tasks to make development easier. They mirror the tasks
executed by the CI pipeline.

Usage
+++++++++++++++++++++++++++++
These tasks can be executed from the command palette in VSCode by searching for "Tasks: Run Task" and selecting the desired task.

They will be executed in the context of the component of the file that is currently focused in the editor. If no file is open, the tasks will be executed in the context of the workspace.

Tasks
+++++

The tasks can be found in the ``tasks.json`` file. They are divided into four types:

- **Lint**: static analysis of files.
- **Check**: validation of style, formatting, or copyright compliance.
- **Format**: automatic in-place correction of files (e.g., adding copyright headers, reformatting C++ code).
- **Group**: batch tasks that run multiple other tasks.

.. list-table:: Tasks Reference
   :widths: 20 12 40
   :header-rows: 1

   * - Task
     - Type
     - Description
   * - ``lint:xml``
     - Lint
     - Lints XML files using ``ament_xmllint``.
   * - ``lint:cmake``
     - Lint
     - Lints CMake files using ``ament_cmake_lint_cmake``.
   * - ``lint:cpp``
     - Lint
     - Lints C++ files using ``ament_cpplint``.
   * - ``check:copyright``
     - Check
     - Checks copyright headers with ``ament_copyright``.
   * - ``check:uncrustify``
     - Check
     - Checks C++ formatting using ``ament_uncrustify``.
   * - ``check:cpp``
     - Check
     - Static analysis of C++ using ``ament_cppcheck``.
   * - ``format:copyright``
     - Format
     - Adds missing copyright headers (MIT license).
   * - ``format:uncrustify``
     - Format
     - Reformats C++ files in place with ``ament_uncrustify --reformat``.
   * - ``format:all``
     - Group
     - Runs ``format:copyright`` and ``format:uncrustify`` in sequence.
   * - ``check:all``
     - Group
     - Runs all lint and check tasks (same as CI pipeline).