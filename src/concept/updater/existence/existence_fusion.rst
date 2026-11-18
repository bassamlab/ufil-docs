Existence Probability Fusion
============================

The existence probability fusion uses a sensor-to-global fusion strategy and is modelled with the Dempster-Shafer Evidence Theory as presented by Aeberhard.
The Theorem specifies a so called frame of discernment :math:`\Theta` that consists of mutually exclusive hypotheses, in this case existence and non-existence.
Next we create the powerset :math:`2^\Theta = \{\emptyset, \exists, \nexists, \{\exists, \nexists\}\}`. As we now not only have the existence and non-existence we can use the mutually exclusive hypotheses to model uncertainty.

Now so called Basic Belief Assignments (BBAs) are created that represents the level of evidence we have for an element of the powerset to be true. It is defined as:

.. math::
    m: 2^\Theta \rightarrow [0, 1].

and all values add up to one.

Additionally we have a belief function Bel(A) that contains all the BBAs of the subsets of A defined and can be seen as the lower-bound probability of A's evidence. The upper-bound is the so called plausability Pl(A) that contains all the sets that support the belief in A. 
The functions are defined as follows:

.. math::
    Bel(A) = \sum_{B:B \subseteqq A} m(B) 
    
    Pl(A) = \sum_{B:B \cap A \neq \emptyset} m(B)

The difference between the values is then the uncertainty.

Prediction
----------

First we start with the prediction of the existence probability. For that we use a weight :math:`\gamma` to transfer a certain percentage of the existence and non-existence into the uncertainty.
The weight is modelled over time with the function :math:`\gamma = 1 - e^{-3 * \Delta t}` and is clamped between the parameters ``existence.min_weight`` and ``existence.max_weight``. So the higher the weight the more amount of uncertainty we have.
The prediction is now calculated as follows:

.. math::
    \begin{align*}
    &m_{k|k-1}^G(\{\exists\}) = (1 - \gamma) * m^G_{k-1|k-1}(\{\exists\}) \\
    &m_{k|k-1}^G(\{\nexists\}) = (1 - \gamma) * m^G_{k-1|k-1}(\{\nexists\}) \\
    &m_{k|k-1}^G(\{\exists, \nexists\}) = m^G_{k-1|k-1}(\{\exists, \nexists\}) + \gamma (m^G_{k-1|k-1}(\{\exists\}) + m^G_{k-1|k-1}(\{\nexists\}))
    \end{align*}

Persistence Probability
-----------------------

Next we need the so called persistence probability to calculate the BBAs.
It is modelled by using the FOV of the sensor and consists of a range and angle part. It is calculated in polar coordinates as follows:

.. math::
    p^{mod}_p (r, \phi) = p_p(r) * p_p(\phi)

The range r and the the angle :math:`\phi` are calculated from the distance to the sensor and as we use cartesian coordinates we first need to convert them into polar coordinates.
The maximum persistence probability is denoted as :math:`p^{max}_p` and :math:`\alpha` is another parameter for the log function.
The values :math:`m_r` and :math:`m_\phi` are cutoff ranges / angles where we dont expect the sensor to be that accurate anymore.
The range persistence probability is modelled as follows:

.. math::
    p_p(r) = 
    \begin{cases}
        0                                                                                           &\text{if } r < r_{min} \\
        p^{max}_p                                                                                   &\text{if } r_{min} \leq r < r_{max} * (1 - m_r) \\
        p^{max}_p * (e^{\frac{-log(\alpha) * (r - r_{max})}{r_{max} - r_{max} * (1 - m_r)} } + 1)   &\text{if } r_{max} * (1 - m_r) \leq r \leq r_{max} \\
        0                                                                                           &\text{if } r > r_{max} \\
    \end{cases}

The angle persistence probability is modelled as:

.. math::
    p_p(\phi) = 
    \begin{cases}
    0                                                                                                                            &\text{if } \phi < -\phi_{max} \\
        p^{max}_p * \frac{1}{2} * (e^{\frac{-log(\alpha) * (\phi + \phi_{max})}{\phi_{max} * (1 - m_\phi)- \phi_{max} }} + 1)    &\text{if } -\phi_{max} \leq \phi \leq -\phi_{max} * (1 - m_\phi) \\
        p^{max}_p                                                                                                                &\text{if } -\phi_{max} * (1 - m_\phi) < \phi < \phi_{max} * (1 - m_\phi) \\
        p^{max}_p * \frac{1}{2} * (e^{\frac{-log(\alpha) * (\phi + \phi_{max})}{\phi_{max} - \phi_{max} * (1 - m_\phi)}} + 1)    &\text{if } \phi_{max} * (1 - m_\phi) \leq \phi \leq \phi_{max} \\
        0                                                                                                                        &\text{if } \phi > \phi_{max} \\
    \end{cases}

If we have a metric for occlusion and the object is occluded the persistence probability is set to 0.

Combination of BBAs
-------------------

Now that we have our BBAs the DST now defines a rule of the combination of the BBAs to fuse the data of differnt sensors i into the global object G.

.. math::
    m^G_{k|k}(C) = \frac{\sum_{A \cap B = C} m^G_{k|k-1}(A) * m^i_k(B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k|k-1}(A) * m^i_k(B)}

Next we have two different cases: either the global object got associated with an object of the sensor or it did not.

Update with associated object
-----------------------------

We start with the case of the association:
For the assingment we need a trust value from the sensor which defines the ability of its performance in calculation of the existence probability.

The assignments are as follows:

.. math::
    \begin{align*}
    &m^i_k(\{\exists\}) = p^i_p(x_{k|k}) * p^i_{trust} * p^i_k(\exists x_k) \\
    &m^i_k(\{\nexists\}) = p^i_p(x_{k|k}) * p^i_{trust} * [1 - p^i_k(\exists x_k)] \\
    &m^i_k(\{\exists, \nexists \}) = 1 - [m^i_k(\{\exists\}) + m^i_k(\{\nexists\})]\\
    \end{align*}

The BBAs for the global objects are then updated like this:

.. math::
    \begin{align*}
    &m^G_{k|k}(\{\exists\}) = \frac{m^G_{k|k-1}(\{\exists\}) * m^i_k(\{\exists\}) + m^G_{k|k-1}(\{\exists\}) * m^i_k(\{\exists, \nexists\}) + m^G_{k|k-1}(\{\exists, \nexists\}) * m^i_k(\{\exists\})}{1 - [m^G_{k|k-1}(\{\exists\}) * m^i_k(\{\nexists\}) + m^G_{k|k-1}(\{\nexists\}) * m^i_k(\{\exists\})]} \\
    &m^G_{k|k}(\{\nexists\}) = \frac{m^G_{k|k-1}(\{\nexists\}) * m^i_k(\{\nexists\}) + m^G_{k|k-1}(\{\nexists\}) * m^i_k(\{\exists, \nexists\}) + m^G_{k|k-1}(\{\exists, \nexists\}) * m^i_k(\{\nexists\})}{1 - [m^G_{k|k-1}(\{\exists\}) * m^i_k(\{\nexists\}) + m^G_{k|k-1}(\{\nexists\}) * m^i_k(\{\exists\})]} \\
    &m^G_{k|k}(\{\exists, \nexists\}) = \frac{m^G_{k|k-1}(\{\exists, \nexists\}) * m^i_k(\{\exists, \nexists\}) }{1 - [m^G_{k|k-1}(\{\exists\}) * m^i_k(\{\nexists\}) + m^G_{k|k-1}(\{\nexists\}) * m^i_k(\{\exists\})]} \\
    \end{align*}

Update without associated object
--------------------------------

Now we have the case of no object association:
The global object is only updated this way if it lies in the FOV of the sensor and is not occluded, i.e. if the persistence probability is greater than 0.
The BBA for the existence is now zero as no object was matched to the gloabl object.
The sensor BBAs are defined as:

.. math::
    \begin{align*}
    &m^i_k(\{\exists\}) = 0 \\
    &m^i_k(\{\nexists\}) = p^i_p(x_{k|k}) * p^i_{trust} \\
    &m^i_k(\{\exists, \nexists \}) = 1 - p^i_p(x_{k|k}) * p^i_{trust} \\
    \end{align*}

Now the only update for the global object that changes in comparison to the associated object is the update for the existence. It is now defined as:

.. math::
    m^G_{k|k}(\{\exists\}) = \frac{m^G_{k|k-1}(\{\exists\}) * m^i_k(\{\exists, \nexists\})}{1 - m^G_{k|k-1}(\{\exists\}) * m^i_k(\{\nexists\})} \\

Conversion of the bbas into the existence probability
-----------------------------------------------------
Since the existence probability is only a single value we now need to convert our BBAs into the real existence probability.
We do that with this formula:

.. math::
    p^G(\exists x_k) = m^G_{k|k} (\{\exists\}) + \frac{1}{2} * m^G_{k|k} (\{\exists, \nexists\})

With that we are now finished.

Sensors without Field of View
-----------------------------

Not every source provides a field of view: CAMs and the sensitive surface layer report objects
without an FOV or occlusion topic (``fov_topic: ""``). For these sensors the persistence
probability is zero and the Dempster-Shafer update above cannot be applied. Instead, an
associated measurement is blended with the previous existence probability, weighted with the
sensor trust:

.. math::
    p^G(\exists x_k) = \frac{1}{2} p^i_{trust} \, p^i_k(\exists x_k) + \frac{1}{2} (2 - p^i_{trust}) \, p^G(\exists x_{k-1})

clamped to :math:`[0, 1]`. Without an associated measurement the existence probability decays
(see below). Objects of CAM sensors (``is_cam: true``) start with an existence probability of
zero, so a vehicle that only sends CAMs has to be confirmed over time.

Decay of Unobserved Tracks
--------------------------

A track that is not associated with a measurement in consecutive updates loses existence
probability. With :math:`n` the number of consecutive updates without association,
:math:`\Delta t` the time since the last update and :math:`\lambda` the parameter
``existence.decay_factor``:

.. math::
    p^G(\exists x_k) = p^G(\exists x_{k-1}) \left(1 - \min\left(1, n \, \lambda \, \Delta t\right)\right) \quad \text{for } n > 1.

The decay is also applied when the fusion only predicts the tracks (no sensor data at that time).

Parameters
----------

The existence fusion of the central fusion is configured with the following parameters (see
:ref:`packages_rsu`):

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Parameter
     - Default
     - Meaning
   * - ``existence.min_weight``
     - 0.2
     - Lower clamp of the prediction weight :math:`\gamma`
   * - ``existence.max_weight``
     - 0.8
     - Upper clamp of the prediction weight :math:`\gamma`
   * - ``existence.decay_factor``
     - 0.05
     - Decay factor :math:`\lambda` of unobserved tracks
   * - ``<sensor>.trust.existence``
     - 0.7 to 0.8
     - Trust :math:`p^i_{trust}` in the existence estimate of a sensor
   * - ``<sensor>.fov_topic``, ``<sensor>.occlusion_topic``
     -
     - Sources of the field of view and the occlusion grid of a sensor

The implementation is ``ProbDempsterShaferUpdater`` in ``ufil_central_fusion``.

References
--------------------------------

M\. Aeberhard, "Object-level fusion for surround environment perception in automated driving applications," VDI Verlag, 2017