.. _existence:

Existence
=========

Ufil comes with an existence estimation system that requires the individual components to provide an existence probability in their object messages. The fusion algorithm combines these existence probabilities from different sources using a Bayesian estimator based on Dempster-Shafer theory, which takes into account sensor-specific trust values, persistence, visibility, detection and clutter likelihoods, and recent association history to compute a fused existence probability for each global track. This allows the system to maintain robust existence estimates even in the presence of conflicting or uncertain information from different sensors, and to control the publication and deletion of tracks based on configurable thresholds.

.. toctree::
   :caption: Contents:
   :maxdepth: 2

   existence_fusion