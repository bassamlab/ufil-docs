.. _classification:

Classification
==============

Ufil comes with a classification fusion system that requires the individual components to provide a classification vector in their object messages. The fusion algorithem constructs a set of superclasses (e.g. vehicle, VRU, stationary) and fine-grained classes (e.g. car, pedestrian, bicycle) and uses Dempster-Shafer theory to combine the classification vectors from different sources into a single posterior distribution over the classes. This algorithem keeps classifciation resutls stable over time and provides a principled way to handle conflicting or uncertain classification information from different sources.

.. toctree::
   :caption: Contents:
   :maxdepth: 2

   classification_estimation_via_look_up
   classification_fusion