.. _index:

Welcome to the Ufil's documentation!
====================================

.. toctree::
   :titlesonly:
   :maxdepth: 1
   :hidden:

   installation/installation
   concept/concept
   examples/examples
   literature
   style_guide
   about

.. image:: images/ufil_logo.svg
   :width: 200px
   :align: center
   :alt: Ufil Logo

In this documentation, you will find everything about the Unified Framework for Infrastructure Localization (Ufil). This project provides a framework for the localization of traffic participants in a fixed area of interest. Unlike other localization frameworks for automated driving or the ROS NAV2 stack, Ufil focuses on tracking an arbitrary number of targets in a fixed area without the need for an ego vehicle. Additionally, this framework allows for the distributed fusion of many information sources, including CAVs, roadside sensor networks, in-road sensors, and more.

In addition to the framework, this documentation showcases three exemplary implementations of this framework:

1. **Computer Simulations with CARLA**: Demonstrating the framework's capabilities in a simulated environment.
2. **Small-Scale Testbed CPM Lab**: Applying the framework in a controlled, small-scale setting.
3. **Real-World Application at the University of Alberta, Edmonton, Canada**: Implementing the framework in a real-world scenario to highlight its practical utility.

These three applications illustrate how Ufil can abstract and unify single tracking applications across multiple deployments in different domains.

If you use Ufil in your work, please see :doc:`Literature <literature>` to cite Ufil.

Getting started
---------------

* :doc:`Installation <installation/installation>` Set up Ufil with ease! Follow these step-by-step instructions to get your environment up and running for the first time.

* :doc:`Concepts <concept/concept>` Explore high-level explanations of Ufil’s core principles. This section complements the guides by giving you a deeper understanding of the framework’s foundational concepts.

* :doc:`Examples <examples/examples>` Discover real-world applications of Ufil in large-scale projects. This section showcases how Ufil has been implemented across various industries, highlighting successful use cases and demonstrating its versatility and effectiveness.


Acknowledgement
---------------

We acknowledge the financial support for this project by the `Collaborative Research Center / Transregio 339 <https://www.sfbtrr339.de/de/>`_ of the German Research Foundation (DFG).

This framework is developed by the Cyber-Physical Mobility Group at the University of the Bundeswehr Munich, Germany and the RWTH Aachen University, Germany. For more information about the group and our research, please visit our website:

- `Cyber-Physical Mobility Group in Aachen <https://www.embedded.rwth-aachen.de/cms/embedded/Forschung/~bflcvi/Cyber-Physical-Mobility/lidx/1/>`_ 
- `Cyber-Physical Mobility Group in Munich <https://www.unibw.de/cas>`_.