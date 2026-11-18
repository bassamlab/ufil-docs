.. _index:

Welcome to Ufil's documentation!
================================

.. toctree::
   :titlesonly:
   :maxdepth: 1
   :hidden:

   installation/installation
   usage/usage
   concept/concept
   examples/examples
   literature
   style_guide
   about

.. image:: images/ufil_logo_20240718.svg
   :width: 200px
   :align: center
   :alt: Ufil Logo

This is the documentation of the Unified Framework for Infrastructure Localization (Ufil). Ufil
localizes and tracks an arbitrary number of traffic participants in a fixed area of interest,
such as an intersection or a parking lot. Unlike localization stacks for automated vehicles or
the ROS 2 Nav2 stack, Ufil needs no ego vehicle: it fuses the information of distributed sources,
such as connected vehicles (on-board units), roadside sensor nodes and in-road sensors, at a road
side unit into one global object list.

Ufil is a set of ROS 2 Jazzy packages around a ROS-independent C++ tracking library. Four example
deployments show how the same components are used in different domains:

1. **CARLA**: computer simulations of a highway and an intersection scenario.
2. **CPM Lab**: a small-scale demonstrator in the Cyber-Physical Mobility Lab.
3. **University of Alberta**: a real-world deployment on a parking lot in Edmonton, Canada.
4. **Pedestrian simulation**: a self-contained scenario simulator to try Ufil and test trackers.

If you use Ufil in your work, please cite the ITSC 2026 paper *Ufil: A Unified Framework for Infrastructure-based
Localization*; see :doc:`Literature <literature>` for all references.

Getting Started
---------------

* :doc:`Installation <installation/installation>`: run Ufil with Docker Compose, in the dev
  container or build it natively.
* :doc:`Running Ufil <usage/usage>`: Compose profiles, middleware, distributed setups,
  configuration and visualization.
* :doc:`Concept <concept/concept>`: architecture, packages, object definition, tracking pipeline
  and the algorithms behind it.
* :doc:`Examples <examples/examples>`: the CARLA, CPM Lab, UofA and pedestrian deployments.

The quickest way to see Ufil in action is the :doc:`pedestrian example <examples/pedestrian/pedestrian>`:

.. code-block:: bash

   docker compose --profile build up                         # build the workspace once
   COMPOSE_PROFILES=pedestrian,foxglove-bridge docker compose up

Acknowledgement
---------------

We acknowledge the financial support for this project by the `Collaborative Research Center / Transregio 339 <https://www.sfbtrr339.de/de/>`_ of the German Research Foundation (DFG).

This framework is developed by the Cyber-Physical Mobility Group at the University of the Bundeswehr Munich, Germany and the RWTH Aachen University, Germany. For more information about the group and our research, please visit our website:

- `Cyber-Physical Mobility Group in Aachen <https://www.embedded.rwth-aachen.de/cms/embedded/Forschung/~bflcvi/Cyber-Physical-Mobility/lidx/1/>`_
- `Cyber-Physical Mobility Group in Munich <https://www.unibw.de/cas>`_
