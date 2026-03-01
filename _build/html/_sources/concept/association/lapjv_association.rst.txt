.. _jonker_volgenant_algorithm:

=========================================================
Jonker–Volgenant Algorithm
=========================================================

Overview
--------
The Linear Assignment Problem (LAP) aims to optimally assign object tracks to
measurement tracks while minimizing the total association cost.

The Jonker–Volgenant (LAPJV) algorithm is an optimized variant of the
Hungarian algorithm. It solves the assignment problem with polynomial time
complexity :math:`\mathcal{O}(n^3)` while achieving significantly improved
practical performance.

In UFIL, the Jonker–Volgenant algorithm computes a globally optimal
one-to-one assignment based on a given cost matrix.

Problem Formulation
-------------------
Given a cost matrix :math:`C \in \mathbb{R}^{n \times m}`, the objective is to
find an assignment matrix :math:`A` minimizing:

.. math::

    \sum_{i,j} C_{ij} A_{ij}

subject to:

- Each row is assigned at most once
- Each column is assigned at most once
- :math:`A_{ij} \in \{0,1\}`

Algorithm Structure
-------------------

The algorithm consists of the following major steps:

- **Column Reduction**  
  Subtract the smallest element of each column.

- **Initialization and Reduction Transfer**  
  Transfer reductions between assigned and unassigned rows.

- **Augmenting Path Search**  
  Identify improving assignment paths using dual variables and labels.

- **Label Updates**  
  Dynamically update reduced costs to maintain optimality conditions.

Characteristics
---------------
- Globally optimal solution
- Deterministic behavior
- Polynomial complexity :math:`\mathcal{O}(n^3)`
- Faster in practice than Hungarian
- Suitable for dense cost matrices

Limitations
-----------
- Requires a full cost matrix
- Limited benefit for sparse matrices
- Designed for linear assignment without additional constraints

Selection Note
--------------
Choose the Jonker–Volgenant algorithm when:

- Optimal one-to-one assignments are required
- Predictable runtime is desired
- The cost matrix is static and dense

Consider alternative methods if additional constraints or non-linear
formulations are required.

Code Documentation
--------------------

The interface to the LAPJV algorithm is implemented in ``association_functions.hpp``
and the underlying implementation in ``jonker_volgenant_algorithm.hpp``.

Function Definition
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

  namespace ufil
  {
  namespace association
  {

  inline void jonker_volgenant(
    const type::CostMatrix & cost_matrix,
    type::AssignmentMatrix & assignment_matrix)
  {
    const auto n_rows = cost_matrix.rows();
    const auto n_cols = cost_matrix.cols();

    // Resize and initialize assignment matrix
    assignment_matrix.resize(n_rows, n_cols);
    assignment_matrix.setZero();

    // No assignment if matrix is empty
    if (!(n_rows > 0 && n_cols > 0)) {
      return;
    }

    // Create and solve assignment problem with Jonker-Volgenant algorithm
    auto problem = JonkerVolgenantAlgorithm<ufil::type::Scalar>(cost_matrix);
    problem.SolveAssignmentProblem();

    // Set assignment matrix with solution
    problem.GetAssignmentMatrix(assignment_matrix);
  }

  }  // namespace association
  }  // namespace ufil

Example Usage
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

  #include <iostream>
  #include <ufil_object_tracking/ufil_object_tracking.hpp>

  // Get cost matrix and prepare assignment matrix buffer

  ufil::type::AssignmentMatrix assignment_matrix;
  ufil::association::jonker_volgenant(cost_matrix, assignment_matrix);
  std::cout << "Assignment Matrix:" << assignment_matrix << std::endl;

Parameters
~~~~~~~~~~~~~~~~~~~~~

- `cost_matrix`: The cost matrix to be used for Jonker-Volgenant assignment.
- `assignment_matrix`: The output assignment matrix.

References
--------------------------------

S. Blackman and R. Popoli, "Design and Analysis of Modern Tracking Systems", Artech House: Norwood, MA, 1999