.. _complex_scenario:

Complex Scenario
=================

For this complex scenario we design a fully fledged infrastructure-based perception system using all the components that Ufil provides.  
The scenario consists of:

- A single section of road with **in-road sensing** (``ufil_ssl``)
- A **roadside lidar** node (``ufil_osn``)
- Multiple vehicles equipped with **V2X communication** (``ufil_obu``)

The scenario is designed to be as close as possible to a real-world application.

.. image:: /images/complex_scenario.png
   :width: 400px
   :align: center
   :alt: Complex scenario of a full infrastructure-based perception system

Sensitive Surface Layer (``ufil_ssl``)
--------------------------------------

The ``ufil_ssl`` component implements the **SSL-based in-road sensing** pipeline. It converts raw load measurements into an object list in the map frame.

**Input:** ``nav_msgs/OccupancyGrid`` (pressure distribution from a grid of load cells)

**Processing:**

1. **Wheel detection**
   - Extracts local maxima from each pressure map
   - Computes intensity-weighted centroids inside a dilation area around each maximum
   - Provides wheel positions robust to overlapping contact patches and grid discretisation

2. **Wheel tracking**
   - Kalman filter with constant-velocity model (lane direction only)
   - Mahalanobis-distance based association
   - Includes track confirmation and deletion logic

3. **Vehicle identification**
   - Groups wheel tracks using axle and wheel templates
   - Checks geometric consistency (track width, axle spacing, velocity coherence)
   - Computes vehicle existence factor from per-wheel quality and number of assigned wheels

**Output:** ``ufil_msgs/ObjectList`` containing:
   - State and covariance
   - Approximate dimensions
   - Classification vector
   - Axle topology (track widths, centre-to-axle distances where available)
   - Existence probability

Lidar-based OSN (``ufil_osn``)
------------------------------

A model-based roadside lidar sensor node that performs: preprocessing, detection, tracking, dimension estimation, classification, and existence estimation.

**Input:** ``sensor_msgs/PointCloud2`` from a static lidar

**Processing:**

- **Preprocessing**
  - Transform to ground-aligned base frame
  - Remove ground and known static structures (height + crop-box filters)
  - Voxel downsampling

- **Object detection**
  - Euclidean clustering of filtered point cloud
  - Oriented bounding-box fitting:
    - L-shape fitting for extended objects
    - Cylindrical model for small or nearly circular objects

- **Tracking**
  - Kalman filter with planar constant-velocity and yaw-rate motion model (6D state: position, velocity, yaw, yaw rate)
  - Two-stage association:
    - First: predicted box overlap
    - Second: distance-based (Euclidean or Mahalanobis)

- **Dimension estimation**
  - 1D grid-map per axis (length, width, height)
  - Variance-aware binary Bayes update with forgetting produces a robust mean dimension and its associated variance

- **Classification**
  - Class-conditioned normal distributions per dimension
  - Bayes' rule computes a posterior over discrete classes, which is then normalized to obtain the classification vector

- **Existence probability**
  - Option A: lightweight heuristic (aggregates age, association ratio, shape stability, motion consistency)
  - Option B: Bayesian estimator (persistence field + detection/clutter likelihoods + association history)

**Output:** ``ufil_msgs/ObjectList`` in map frame, including:
  - State and covariance
  - Dimensions with covariance
  - Classification vector
  - Existence probability
  - Optional static flag

On-Board Unit and V2I (``ufil_obu``)
------------------------------------

Provides the **on-board unit (OBU)** interface that converts vehicle self-state estimates into V2I messages and into the internal Ufil object representation.

**Input:** Ego vehicle's state (fused GNSS/inertial pose and velocity) + dimensions from domain-specific interfaces

**Processing:**

- Transform positions from WGS84 to UTM and finally to the map frame (georeferencing pipeline).
- Populate internal Ufil object with state, covariance, and dimensions
- Map to **ETSI CAM** (position, speed, heading, dimensions where supported)
- Transmit over UDP to RSU
- Optionally publish ``ufil_msgs/ObjectList`` directly (classification = one-hot encoding, existence = 1.0)

**Note:** Resolution limits of CAM fields and vehicle-side estimation characteristics are reflected in the covariance attached to the object.

Central Fusion on the RSU
-------------------------

Subscribes to heterogeneous object lists from ``ufil_ssl``, ``ufil_osn``, and ``ufil_obu`` and fuses them into a single global object list in the map frame.

**Core cycle (multi-object tracking):**

- Prediction of all global tracks to current fusion time
- Association of incoming sensor objects to global tracks
- Update of state, dimensions, classification, and existence
- Track management (births / deletions)

**Handling latency & out-of-order data:**

- Maintains a time-ordered buffer over a configurable horizon
- Processes messages chronologically before predicting to publish time

**Fusion methods:**

- **State fusion:** dynamic measurement models select only provided components (covariance mask), Kalman update with chosen motion model (e.g. constant velocity, random walk)

- **Dimension fusion:** uses the same grid-map estimator as the roadside node to combine length, width, and height measurements from different modalities with different uncertainties.

- **Classification fusion:** Dempster-Shafer theory over reduced powerset (fine-grained classes + superclasses: vehicle, VRU, stationary). Sensor-specific trust values + conflict-adaptive forgetting avoid overconfidence.

- **Existence fusion:** either heuristic aggregation or Bayesian estimator (Dempster-Shafer again). Combines persistence, visibility, detection/clutter likelihoods, per-sensor trust. Hide/delete thresholds control publication.

**Output:** Time-triggered (e.g. 50 Hz) ``ufil_msgs/ObjectList`` with unified, uncertainty-aware description of all tracked road users.

Example Implementations
-----------------------

We provide two example implementations:

.. toctree::
   :maxdepth: 1

   carla/carla
   cpm_lab/cpm_lab