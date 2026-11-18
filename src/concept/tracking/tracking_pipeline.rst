.. _tracking_pipeline:

Tracking Pipeline
=================

``ufil_object_tracking`` is the tracking framework at the heart of Ufil. It is a header-only C++20
library without ROS 2 dependencies (it uses Eigen, Boost, PCL and TBB). The outdoor sensor node
tracker, the central fusion of the RSU and the pedestrian example tracker are all built from it.

Include the whole library with

.. code-block:: cpp

   #include <ufil_object_tracking/ufil_object_tracking.hpp>

and link against the CMake target ``ufil_object_tracking::ufil_object_tracking``:

.. code-block:: cmake

   find_package(ufil_object_tracking REQUIRED)
   target_link_libraries(my_tracker PUBLIC ufil_object_tracking::ufil_object_tracking)

Types
-----

A track is a ``ufil::type::Track`` parametrized with the types of its parts. Each part is chosen
from ``ufil::type``:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Part
     - Available types
   * - State
     - ``state::Position2D``, ``PositionVelocity2D``, ``PositionVelocityAcceleration2D``,
       ``Pose2D``, ``PoseVelocity2D``, ``PoseVelocityAcceleration2D``, ``NoState``
   * - Dimension
     - ``dimension::Dimension2D``, ``Dimension3D``, ``NoDimension``
   * - Classification
     - ``classification::ObjectClassification`` (the seven classes of :ref:`messages`)
   * - Existence
     - ``ExistenceProbability`` (probability and Dempster-Shafer basic belief assignment)
   * - Control
     - ``control::None``
   * - Measurement
     - ``measurement::Position2D``, ``Pose2D``, ``Pose2DWithDimension2D``,
       ``Pose2DWithDimension3D``, ``Position3D``

.. code-block:: cpp

   using State = ufil::type::state::PoseVelocity2D;
   using Dimension = ufil::type::dimension::Dimension3D;
   using Classification = ufil::type::classification::ObjectClassification;
   using Control = ufil::type::control::None;
   using Measurement = ufil::type::measurement::Pose2DWithDimension3D;
   using ExistenceProbability = ufil::type::ExistenceProbability;

   using Track = ufil::type::Track<
     State, Dimension, Classification, ExistenceProbability, Control, Measurement>;

Every track keeps a time-stamped history of its estimates and associated measurements, which
allows out-of-order processing and the evaluation of past associations.

Processing Steps
----------------

``ufil::tracking::MultiTargetTracker<Track, Detection>`` runs the following steps for every call
of ``update(detections, timestamp)``:

.. container:: mermaid-tall

   .. mermaid::
      :caption: Processing steps of ``MultiTargetTracker::update``
      :alt: Flowchart of the seven steps predict, detect, associate, update, initiate, delete and prune
      :align: center

      flowchart TB
         IN(["update(detections, timestamp)"])
         subgraph EST["Estimation"]
            direction LR
            P["1 Predict<br/>predict::Predictor"] --> D["2 Detect<br/>detection::Detector"] --> A["3 Associate<br/>association::Associator"] --> U["4 Update<br/>update::Updater"]
         end
         subgraph MGT["Track management"]
            direction LR
            I["5 Initiate<br/>management::Initiator"] --> X["6 Delete<br/>management::Deleter"] --> R["7 Prune<br/>management::Pruner"]
         end
         TR[("tracks")]

         IN --> EST
         EST -->|"updated tracks,<br/>unassociated measurements"| MGT
         MGT --> TR
         TR -. "next update" .-> EST

.. list-table::
   :header-rows: 1
   :widths: 5 18 32 45

   * - #
     - Step
     - Interface
     - Implementations
   * - 1
     - **Predict**
     - ``predict::Predictor``
     - ``ModelStatePredictor`` (state with a :ref:`motion model <models>`),
       ``SelectivePredictor`` (model per object class), ``DimensionPredictor``,
       ``ClassificationPredictor``, ``ExistencePredictor``, ``OcclusionPredictor``;
       combined with ``ParallelPredictor`` / ``SequentialPredictor``
   * - 2
     - **Detect**
     - ``detection::Detector``
     - ``SimpleDetector`` (detections are measurements), ``PointCloudDetector`` (clustering and
       shape fitting of point clouds)
   * - 3
     - **Associate**
     - ``association::Associator``
     - ``FunctionAssociator(distance, assignment, threshold)`` with a
       :ref:`distance measure <hypothesize>` and an :doc:`assignment algorithm <../association/association>`
   * - 4
     - **Update**
     - ``update::Updater``
     - ``ModelStateUpdater`` (:ref:`Kalman filter <state>`), ``DimensionGridmapUpdater``
       (:ref:`dimension grid map <dimension>`), ``ClassificationUpdater``,
       ``DimensionClassificationUpdater``, ``ExistenceUpdater``, ``ExistenceEstimator``;
       combined with ``SequentialUpdater`` / ``ParallelUpdater``
   * - 5
     - **Initiate**
     - ``management::Initiator``
     - ``SimpleInitiator``, ``FunctionInitiator`` (user-defined initialization of a new track
       from an unassociated measurement)
   * - 6
     - **Delete**
     - ``management::Deleter``
     - ``TimedDeleter`` (no association for a duration), ``ExistenceDeleter`` (existence below a
       threshold), ``JsonHistoryDeleter`` (also writes the history of deleted tracks to JSON)
   * - 7
     - **Prune**
     - ``management::Pruner``
     - ``TimedPruner`` (history older than a duration), ``LengthPruner`` (maximum number of
       history entries)

All building blocks are passed as ``std::shared_ptr`` and can be replaced by own implementations
of the interfaces.

Example: Pedestrian Tracker
---------------------------

The tracker of the :doc:`pedestrian example <../../examples/pedestrian/pedestrian>`
(``ufil_examples_pedestrian_tracker``) is a compact, complete example. It tracks pedestrian
detections with a random walk model, associates them with the Wasserstein distance and the
Hungarian algorithm, estimates the dimensions with the grid map updater and deletes tracks that
were not updated for one second:

.. code-block:: cpp

   #include <ufil_object_tracking/association/association_functions.hpp>
   #include <ufil_object_tracking/association/associator.hpp>
   #include <ufil_object_tracking/detection/simple_detector.hpp>
   #include <ufil_object_tracking/management/deleter/timed_deleter.hpp>
   #include <ufil_object_tracking/management/initiator/function_initiator.hpp>
   #include <ufil_object_tracking/management/pruner/timed_pruner.hpp>
   #include <ufil_object_tracking/models/measurement/linear_kalman_measurement_model.hpp>
   #include <ufil_object_tracking/models/transition/random_walk_transition_model.hpp>
   #include <ufil_object_tracking/predict/state/model_state_predictor.hpp>
   #include <ufil_object_tracking/tracking/multi_target_tracker.hpp>
   #include <ufil_object_tracking/update/composite_updater.hpp>
   #include <ufil_object_tracking/update/dimension/dimension_gridmap_updater.hpp>
   #include <ufil_object_tracking/update/state/model_state_updater.hpp>

   using TransitionModel = ufil::model::transition::RandomWalkTransitionModel<State, Control>;
   using MeasurementModel = ufil::model::LinearKalmanMeasurementModel<State, Measurement>;

   // Initialization of a new track from an unassociated measurement
   void initiateNewTrack(
     const Measurement & measurement, State & state, Dimension & dimension,
     Classification & classification, ExistenceProbability & existence)
   {
     state.x() = measurement.x();
     state.y() = measurement.y();
     state.yaw() = measurement.yaw();
     state.covariance() = State::CovarianceMatrixType::Identity() * 100.0F;

     dimension.length() = measurement.dimension().length();
     dimension.width() = measurement.dimension().width();
     dimension.covariance() = Dimension::CovarianceMatrixType::Identity() * 100.0F;

     classification.pedestrian() = 1.0;
     classification.normalize();

     existence.existence() = measurement.existenceProbability();
   }

   auto makeTracker(float process_noise, double track_timeout)
   {
     // 1. Predict: random walk with the given process noise per axis
     TransitionModel::NoiseMatrixType noise;
     noise << process_noise, 0.0F, 0.0F, process_noise;
     auto predictor = std::make_shared<ufil::predict::ModelStatePredictor<Track>>(
       std::make_shared<TransitionModel>(noise));

     // 2. Detect: detections are already measurements
     auto detector = std::make_shared<ufil::detection::SimpleDetector<Track, Measurement>>();

     // 3. Associate: Wasserstein distance + Hungarian algorithm
     auto associator = std::make_shared<ufil::association::FunctionAssociator<Track>>(
       &ufil::association::wasserstein<Track>, &ufil::association::hungarian);

     // 4. Update: Kalman filter for the state, grid map for the dimension
     auto updater = std::make_shared<ufil::update::ParallelUpdater<Track>>();
     updater->addUpdater(std::make_shared<ufil::update::state::ModelStateUpdater<Track>>(
       std::make_shared<MeasurementModel>()));
     updater->addUpdater(
       std::make_shared<ufil::update::dimension::DimensionGridmapUpdater<Track>>());

     // 5.-7. Track management
     auto initiator = std::make_shared<ufil::management::FunctionInitiator<Track>>(&initiateNewTrack);
     auto deleter = std::make_shared<ufil::management::TimedDeleter<Track>>(
       ufil::from_seconds<ufil::type::Duration>(track_timeout));
     auto pruner = std::make_shared<ufil::management::TimedPruner<Track>>(std::chrono::seconds(1));

     return std::make_unique<ufil::tracking::MultiTargetTracker<Track, Measurement>>(
       0.7F /* existence threshold */, predictor, detector, associator, updater,
       initiator, deleter, pruner);
   }

   // In the processing loop
   auto tracker = makeTracker(10.0F, 1.0);
   tracker->update(std::move(detections), timestamp);   // std::set<Measurement>, ufil::type::Timestamp
   for (const auto & [id, track] : tracker->tracks()) {
     const auto & state = track.currentState();
     // state.x(), state.y(), state.covariance(), ...
   }

The ROS 2 component of the package only converts the incoming ``ufil_msgs/ObjectList`` into a
``std::set<Measurement>`` and the tracks back into an object list (with ``ufil_ros``), and resets
the tracker when the time jumps backwards or by more than ``max_time_gap``.

Trackers in Ufil
----------------

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - Building block
     - OSN tracker (``ufil_osn_tracker``)
     - Central fusion (``ufil_central_fusion``)
     - Pedestrian tracker
   * - Motion model
     - extended constant velocity
     - random walk (pedestrians), extended constant velocity (other classes)
     - random walk
   * - Detector
     - ``PointCloudDetector``
     - ``SimpleDetector``
     - ``SimpleDetector``
   * - Distance / assignment
     - Euclidean / Hungarian
     - Euclidean / Hungarian
     - Wasserstein / Hungarian
   * - Updaters
     - state and dimension grid map, existence estimator, classification from the dimensions;
       occlusion-aware prediction
     - state, dimension grid map, Dempster-Shafer existence and classification
     - state, dimension grid map
   * - Deletion
     - existence
     - existence
     - timed
