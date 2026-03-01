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

They will be executed in the context of the component of the file that is currently open in the editor. If no file is open, the tasks will be executed in the context of the workspace.

Tasks
++++++++++++++++++++++++++++

The tasks can be found in the `tasks.json` file and are the following:

- `lint:xml`: Lints XML files using `ament_xmllint`.
- `lint:cmake`: Lints CMake files using `ament_cmake_lint_cmake`.
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

