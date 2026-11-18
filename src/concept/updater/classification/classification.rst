.. _classification:

Classification
==============

The classification vector :math:`\mathbf{c}` holds the probability of each object class (see
:ref:`object_definition`). Trackers derive it from their sensor, e.g. the OSN tracker from the
estimated dimensions (:doc:`look-up of class-conditioned dimension distributions
<classification_estimation_via_look_up>`) and the OSN classifier from camera images.

The central fusion requires every source to provide a classification vector in its object
messages. It constructs a set of superclasses (e.g. vehicle, VRU, stationary) and fine-grained
classes (e.g. car, pedestrian, bicycle) and uses Dempster-Shafer theory to combine the
classification vectors of the different sources into a single posterior distribution over the
classes. This keeps the classification stable over time and provides a principled way to handle
conflicting or uncertain classification information.

.. toctree::
   :caption: Contents:
   :maxdepth: 2

   classification_fusion
   classification_estimation_via_look_up