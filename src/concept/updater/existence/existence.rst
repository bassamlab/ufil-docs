.. _existence:

Existence
=========

The existence probability :math:`p_e` expresses how certain a component is that a track
corresponds to a real object. Trackers estimate it from their detections (``ExistenceEstimator``,
``ExistenceUpdater``). The central fusion combines the existence probabilities of the individual
sources with a Bayesian estimator based on Dempster-Shafer theory, which takes sensor-specific
trust values, persistence, visibility and the recent association history into account. This keeps
the existence estimate robust against conflicting or uncertain information from different sensors
and controls the publication and deletion of tracks with configurable thresholds.

.. toctree::
   :caption: Contents:
   :maxdepth: 2

   existence_fusion