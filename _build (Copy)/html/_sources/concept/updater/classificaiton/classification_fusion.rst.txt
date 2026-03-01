Classification Fusion
=======================

The classification Fusion makes use of a sensor-to-global fusion strategy.
For that the Dempster Shafer Theorem is used as described by the work of Aeberhard. 
First the mutually exclusive classes for discernment :math:`\Theta` with possible Objects got defined as

- Car
- Truck
- Motorcycle
- Pedestrian
- Bicycle
- Stationary

Other is not included as it is not a class for an identifiable object and only exists as placeholder for objects that do not have the characteristics of any other class.
As we have six classes 64 combinations for the frame of discernment would be possible. We reduce those powerset to the following:

.. math::
    2^\Theta_r \subset 2^\Theta = \{\emptyset, \{C_{Car}\}, \{C_{Truck}\}, \{C_{Motorcycle}\}, \{C_{Pedestrian}\}, \{C_{Bicycle}\}, \{C_{Stationary}\},
    
    \{C_{Vehicle}\}, \{C_{VRU}\}, \{C_{Vehicle}, C_{Stationary}\}, \{C_{VRU}, C_{Stationary}\}, \Theta\}

where 

- :math:`\{C_{Vehicle}\} = \{C_{Car}, C_{Truck}, C_{Motorcycle}\}`
- :math:`\{C_{VRU}\} = \{C_{Pedestrian}, C_{Bicycle}\}`
- :math:`\{C_{Traffic}\} = \{C_{Vehicle}, C_{VRU}\}`

The set vehicle defines a so called "super class" that contains all objects that can reach high speeds and the set VRU is for vulnerable road users that are not protected by their vehicles.
The set traffic contains both since all of those classes participate in the traffic. The super sets are very useful for sensors that are not that great in differentiating each class but in observing the different features the supersets inherit.

The basic belief assignments, from now on referred to as bbas, are now defined for our reduced powerset as 

.. math::
    m:2^\Theta_r \rightarrow [0, 1]

The sum of these bbas add up to one and are tracked over time by the central fusion. 
Then the new sensor evidence is combined into the new  global basic belief assignment by 

.. math:: 
    m^G_k(C) = \frac{\sum_{A \cap B = C} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}

Now as we don't trust every sensor completely and also some differently with their ability to recognize classes or in general we introduce a trust factor which reduces the bbas of those sensors.
Each class has a separate trust factor and those are either given by the sensor or calculated by experiment.
Using those we now calculate the bbas of the sensor like

1. :math:`m^i_k(\{C_{Car}\}) = p^i_{trust}(C_{Car}) * p^i_k(C_{Car})`

2. :math:`m^i_k(\{C_{Truck}\}) = p^i_{trust}(C_{Truck}) * p^i_k(C_{Truck})`

3. :math:`m^i_k(\{C_{Motorcycle}\}) = p^i_{trust}(C_{Motorcycle}) * p^i_k(C_{Motorcycle})`

4. :math:`m^i_k(\{C_{Pedestrian}\}) = p^i_{trust}(C_{Pedestrian}) * p^i_k(C_{Pedestrian})`

5. :math:`m^i_k(\{C_{Bicycle}\}) = p^i_{trust}(C_{Bicycle}) * p^i_k(C_{Bicycle})`

6. :math:`m^i_k(\{C_{Stationary}\}) = p^i_{trust}(C_{Stationary}) * p^i_k(C_{Stationary})`

Now we have some remaining evidence which will be used for our super classes.

For that we additionally add a move probability which will be calculated via: 

.. math::
    velocity = |v_x| + |v_y|

    p^i_{moved} = 1 - e^{-1 * 2 * velocity}

For the calculation of the bbas we need the probabilities of Vehicle and VRU. Those we calculate as following:

1.  :math:`p^i_{C_{Vehicle}} = \frac{m^i_k(\{C_{Car}\}) + m^i_k(\{C_{Truck}\}) + m^i_k(\{C_{Motorcycle}\})}{m^i_k(\{C_{Car}\}) + m^i_k(\{C_{Truck}\}) + m^i_k(\{C_{Motorcycle}\}) + m^i_k(\{C_{Pedestrian}\}) + m^i_k(\{C_{Bicycle}\}) }`

2.  :math:`p^i_{C_{VRU}} = \frac{m^i_k(\{C_{Pedestrian}\}) + m^i_k(\{C_{Bicycle}\})}{m^i_k(\{C_{Car}\}) + m^i_k(\{C_{Truck}\}) + m^i_k(\{C_{Motorcycle}\}) + m^i_k(\{C_{Pedestrian}\}) + m^i_k(\{C_{Bicycle}\}) }`

Now we calculate the bbas for the super classes:

1.  :math:`m^i_k(C_{Vehicle}) = p^i_{moved} * p^i_{C_{Vehicle}} * [(1 - p_{trust}(C_{Car})) * p^i_k(C_{Car})`
        :math:`+ (1 - p_{trust}(C_{Truck})) * p^i_k(C_{Truck}) + (1 - p_{trust}(C_{Motorcycle})) * p^i_k(C_{Motorcycle})]`

2.  :math:`m^i_k(C_{VRU}) = p^i_{moved} * p^i_{C_{VRU}} * [(1 - p_{trust}(C_{Pedestrian})) * p^i_k(C_{Pedestrian})`
        :math:`+ (1 - p_{trust}(C_{Bicycle})) * p^i_k(C_{Bicycle})]`

3.  :math:`m^i_k(C_{Traffic}) = p^i_{moved} * p^i_{C_{VRU}} * [(1 - p_{trust}(C_{Car})) * p^i_k(C_{Car})`
        :math:`+ (1 - p_{trust}(C_{Truck})) * p^i_k(C_{Truck}) + (1 - p_{trust}(C_{Motorcycle})) * p^i_k(C_{Motorcycle})]`
        :math:`+ p^i_{moved} * p^i_{C_{Vehicle}} * [(1 - p_{trust}(C_{Pedestrian})) * p^i_k(C_{Pedestrian})`
        :math:`+ (1 - p_{trust}(C_{Bicycle})) * p^i_k(C_{Bicycle})]`

4.  :math:`m^i_k(C_{Vehicle}, C_{Stationary}) = (1 -p^i_{moved}) * p^i_{C_{Vehicle}} * [(1 - p_{trust}(C_{Car})) * p^i_k(C_{Car})`
        :math:`+ (1 - p_{trust}(C_{Truck})) * p^i_k(C_{Truck}) + (1 - p_{trust}(C_{Motorcycle})) * p^i_k(C_{Motorcycle})]`

5.  :math:`m^i_k(C_{VRU}, C_{Stationary}) = (1 -p^i_{moved}) * p^i_{C_{VRU}} * [(1 - p_{trust}(C_{Pedestrian})) * p^i_k(C_{Pedestrian})`
        :math:`+ (1 - p_{trust}(C_{Bicycle})) * p^i_k(C_{Bicycle})]`

As the next step we will use the Dempster Shafer rule as declared above:

1.  :math:`m^G_k(C_{Car}) = \frac{\sum_{A \cap B = C_{Car}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`

2.  :math:`m^G_k(C_{Truck}) = \frac{\sum_{A \cap B = C_{Truck}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`  

3.  :math:`m^G_k(C_{Motorcycle}) = \frac{\sum_{A \cap B = C_{Motorcycle}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`
  
4.  :math:`m^G_k(C_{Pedestrian}) = \frac{\sum_{A \cap B = C_{Pedestrian}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`
  
5.  :math:`m^G_k(C_{Bicycle}) = \frac{\sum_{A \cap B = C_{Bicycle}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`
  
6.  :math:`m^G_k(C_{Stationary}) = \frac{\sum_{A \cap B = C_{Stationary}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`
  
7.  :math:`m^G_k(C_{Vehicle}) = \frac{\sum_{A \cap B = C_{Vehicle}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`
  
8.  :math:`m^G_k(C_{VRU}) = \frac{\sum_{A \cap B = C_{VRU}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`
   
9.  :math:`m^G_k(C_{Traffic}) = \frac{\sum_{A \cap B = C_{Traffic}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`
   
10.  :math:`m^G_k(C_{Vehicle}, C_{Stationary}) = \frac{\sum_{A \cap B = C_{Vehicle}, C_{Stationary}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`
  
11.  :math:`m^G_k(C_{VRU}, C_{Stationary}) = \frac{\sum_{A \cap B = C_{VRU}, C_{Stationary}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`
 
12.  :math:`m^G_k(C_{\Theta}) = \frac{\sum_{A \cap B = C_{\Theta}} m^G_{k-1} (A) * m^i_k (B)}{1 - \sum_{A \cap B = \emptyset} m^G_{k-1} (A) * m^i_k (B)}`

Now we need to convert the vector bbas into the classification vector. For that we use the Pignistic transformation but without containing the frame of discernment.

.. math::
    BetP(A) = \sum_{B \subseteqq \Theta B\neq \Theta} \frac{|A \cap B|}{|B|} * m(B)

where :math:`m^G(\Theta)` should be equivalent to :math:`p^G_k(C_{Other})`

Now the general formula for the fused probabilites is 

.. math::
    p^G_k(C_i) = BetP(\{C_i\}) = \sum_{B \subseteqq \Theta B\neq \Theta} \frac{|\{C_i\} \cap B|}{|B|} * m^G_k(B)

After evaluation the probabilities for the classes are now as follows:

1.  :math:`p^G_k(C_{Car}) = m^G_k(\{C_{Car}\}) + \frac{1}{3} * m^G_k(\{C_{Vehicle}\}) + \frac{1}{5} * m^G_k(\{C_{Traffic}\})`
        :math:`+ \frac{1}{4} * m^G_k(\{C_{Vehicle}, C_{Stationary}\})`

2.  :math:`p^G_k(C_{Truck}) = m^G_k(\{C_{Truck}\}) + \frac{1}{3} * m^G_k(\{C_{Vehicle}\}) + \frac{1}{5} * m^G_k(\{C_{Traffic}\})`
        :math:`+ \frac{1}{4} * m^G_k(\{C_{Vehicle}, C_{Stationary}\})`  

3.  :math:`p^G_k(C_{Motorcycle}) = m^G_k(\{C_{Motorcycle}\}) + \frac{1}{3} * m^G_k(\{C_{Vehicle}\}) + \frac{1}{5} * m^G_k(\{C_{Traffic}\})`
        :math:`+ \frac{1}{4} * m^G_k(\{C_{Vehicle}, C_{Stationary}\})`

4.  :math:`p^G_k(C_{Pedestrian}) = m^G_k(\{C_{Pedestrian}\}) + \frac{1}{2} * m^G_k(\{C_{VRU}\}) + \frac{1}{5} * m^G_k(\{C_{Traffic}\})`
        :math:`+ \frac{1}{3} * m^G_k(\{C_{VRU}, C_{Stationary}\})`
  
5.  :math:`p^G_k(C_{Bicycle}) = m^G_k(\{C_{Bicycle}\}) + \frac{1}{2} * m^G_k(\{C_{VRU}\}) + \frac{1}{5} * m^G_k(\{C_{Traffic}\})`
        :math:`+ \frac{1}{3} * m^G_k(\{C_{VRU}, C_{Stationary}\})`
  
6.  :math:`p^G_k(C_{Stationary}) = m^G_k(\{C_{Stationary}\}) + \frac{1}{4} * m^G_k(\{C_{Vehicle}, C_{Stationary}\})`
        :math:`+ \frac{1}{3} * m^G_k(\{C_{VRU}, C_{Stationary}\})`

and the probability for the class other now is 

:math:`1 - [p^G_k(C_{Car}) + p^G_k(C_{Truck}) + p^G_k(C_{Motorcycle}) + p^G_k(C_{Pedestrian})`
    :math:`+ p^G_k(C_{Bicycle}) + p^G_k(C_{Stationary})]`

With that the classification vector adds up to one and we are finished.

References
--------------------------------

M\. Aeberhard, "Object-level fusion for surround environment perception in automated driving applications," VDI Verlag, 2017