.. _cpm_lab:

Cyber-Physical Mobility Lab
===========================

The **Cyber-Physical Mobility (CPM) Lab** example in **Ufil** demonstrates one of the framework's most advanced use cases.  
It consists of three packages and is included in the ``ufil_examples`` module.

This scenario illustrates how a complete infrastructure-based localization system, described in the :ref:`Complex Scenario <complex_scenario>`, can be executed on a small-scale testbed like the CPM Lab.

Scenario
----------

The scenario is a three-lane highway segment with an sensitive surface layer (SSL) covering the two right-most lanes near the upstream part of the segment and a roadside lidar outdoor sensor node installed downstream, facing the SSL region; their fields of view partially overlap. Vehicles are equipped with V2I functionality and broadcast CAM messages. 

.. image:: /images/highway_scenario.png
   :width: 400px
   :align: center
   :alt: Illustration of the scenario.


Below is a photo of the setup:

.. image:: /images/cpm_lab_scenario.jpg
   :width: 400px
   :align: center
   :alt: Illustration of the scenario.


Usage
-----

1. **Starting the Example**
   
   The example comes with an integrated launch file that starts all components of the system.

   .. code-block:: bash

      ros2 launch ufil_examples_simple_scenario visualization.launch.py

   The visualization should appear as follows:

   .. image:: /images/cpm_lab_visualization.png
      :width: 400px
      :align: center
      :alt: RViz showing the Ufil visualization

2. **Playing the Dataset**

   In a second terminal, play back the dataset provided. This automatically replays all necessary sensor data to trigger the perception pipeline.  
   Using a higher clock frequency improves timestamp accuracy.

   .. code-block:: bash

      ros2 bag play <path-to-dataset> --clock 300

   The visualization will now display the tracking in action and produce output like this:

   .. image:: /images/cpm_lab_running.png
      :width: 400px
      :align: center
      :alt: RViz showing Ufil tracking the complex scenario in the CPM Lab

Dataset
-------

The dataset used for this example will be made available soon.