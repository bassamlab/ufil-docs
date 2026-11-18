.. _updater:

Updater
=======

The sections below describe the updaters of Ufil and the mathematical approaches behind them.
An updater corrects one part of a track with an associated measurement (see the update step of
the :ref:`tracking pipeline <tracking_pipeline>`). The updaters are grouped into four categories,
matching the parts of an :ref:`object <object_definition>`: state, dimension, classification and
existence. In the central fusion the same categories are used to fuse the object lists of several
sensors.

.. toctree::
   :caption: Contents:
   :maxdepth: 2

   state/state
   dimension/dimension
   classification/classification
   existence/existence
