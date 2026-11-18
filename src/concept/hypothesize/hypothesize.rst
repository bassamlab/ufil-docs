..  _hypothesize:

====================
Hypothesize Measures
====================

The Ufil framework provides several hypothesize methods for measurement-to-track similarity
comparison. Next to well-known measures such as the Euclidean distance, the Mahalanobis distance
and the Intersection over Union (IoU), Ufil also includes more experimental approaches such as a
closed-form Wasserstein distance. A distance measure is combined with an
:doc:`assignment algorithm <../association/association>` in a ``FunctionAssociator`` (see
:ref:`tracking_pipeline`).

.. toctree::
   :caption: Contents
   :maxdepth: 1

   euclidean_distance.rst
   mahalanobis_distance.rst
   wasserstein_distance.rst
   intersection_over_union_distance.rst
