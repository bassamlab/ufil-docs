.. _classification_estimation_via_look_up:

Classification Estimation via Look-Up
=====================================

A simple approach to classification estimation is a look-up that maps the estimated dimensions of
an object to class probabilities. Usually, such a look-up is constructed from a training dataset
and some features extracted from the objects. Ufil uses the estimated **length and width** as
features and fits a class-conditioned normal distribution per feature and class to the training
data. Bayes' rule then gives the posterior probability of each class for the current dimension
estimate.

Formulation
-----------

For every class :math:`C_i` the lengths and widths of the training objects are modelled as
independent normal distributions :math:`\mathcal{N}(\mu_{l,i}, \sigma_{l,i}^2)` and
:math:`\mathcal{N}(\mu_{w,i}, \sigma_{w,i}^2)`. With the estimated length :math:`l` and width
:math:`w` of a track (ordered so that :math:`l \geq w`), the likelihood of a class is the
probability mass within a radius :math:`r` around the estimate:

.. math::
    p(l, w \mid C_i) = \left[ F_{l,i}(l + r) - F_{l,i}(l - r) \right]
                       \left[ F_{w,i}(w + r) - F_{w,i}(w - r) \right],

where :math:`F` is the cumulative distribution function of the respective normal distribution.
With a uniform prior, normalizing the likelihoods over all classes yields the classification
vector:

.. math::
    c_i = \frac{p(l, w \mid C_i)}{\sum_j p(l, w \mid C_j)}.

The default models in ``ufil_object_tracking`` are:

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 20 20

   * - Class
     - :math:`\mu_l` [m]
     - :math:`\sigma_l` [m]
     - :math:`\mu_w` [m]
     - :math:`\sigma_w` [m]
   * - Car
     - 4.78
     - 0.74
     - 2.07
     - 0.17
   * - Truck
     - 14.94
     - 4.40
     - 3.34
     - 0.34
   * - Pedestrian
     - 0.67
     - 0.09
     - 0.67
     - 0.09
   * - Bicycle
     - 1.66
     - 0.16
     - 0.87
     - 0.09
   * - Motorcycle
     - 2.04
     - 0.26
     - 0.89
     - 0.11

Properties
----------

This approach results in a single-shot estimation of the classification vector based on the
current dimension estimate, without explicitly modelling temporal dynamics or inter-class
relationships. It is simple and computationally efficient and provides reasonable classification
performance when the dimension estimates are accurate and the classes are well separated in the
feature space. It struggles with ambiguous cases where classes have overlapping dimension
distributions (e.g. bicycles and motorcycles) or when the dimension estimates are noisy. Since
the dimension grid map stabilizes the dimension estimate over time, the classification also
becomes more stable the longer a track exists.

Code Documentation
------------------

The look-up is implemented by ``DimensionClassificationUpdater`` in
``update/classification/dimension_classification_updater.hpp``. It reads the current dimension of
the track, so it has to run after the dimension updater (e.g. in a ``SequentialUpdater``). The
constructor takes the radius :math:`r` (default 0.2 m):

.. code-block:: cpp

    auto updater = std::make_shared<ufil::update::SequentialUpdater<Track>>();
    updater->addUpdater(dimension_updater);
    updater->addUpdater(
      std::make_shared<ufil::update::classification::DimensionClassificationUpdater<Track>>(0.2));

The OSN tracker uses this updater to classify the lidar tracks.
