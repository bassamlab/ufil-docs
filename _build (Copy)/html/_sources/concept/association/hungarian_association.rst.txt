.. _hungarian_algorithm:

====================
Hungarian Algorithm
====================

Overview
--------
The Hungarian algorithm is a combinatorial optimization algorithm that solves
the linear assignment problem in polynomial time. It computes a globally
optimal one-to-one assignment between rows and columns of a cost matrix such
that the total cost is minimized.

In UFIL, the Hungarian algorithm is used to associate tracks and measurements
based on a previously computed cost matrix.

The algorithm guarantees:

- Globally optimal solution
- Deterministic behavior
- One-to-one assignments

Problem Formulation
-------------------
Given a cost matrix :math:`C \in \mathbb{R}^{n \times m}`, the goal is to find
an assignment matrix :math:`A` that minimizes:

.. math::

    \sum_{i,j} C_{ij} A_{ij}

subject to:

- Each row is assigned at most once
- Each column is assigned at most once
- :math:`A_{ij} \in \{0,1\}`

Characteristics
---------------
- Optimal solution
- Time complexity: :math:`\mathcal{O}(n^3)`
- Suitable for moderate-sized problems
- Widely used in tracking systems

Selection Note
--------------
The Hungarian algorithm is recommended when a guaranteed optimal assignment
is required and computation time is acceptable.

Code Documentation
-------------------

The interface to the Hungarian algorithm is implemented in ``association_functions.hpp``
and the underlying implementation in ``hungarian_algorithm.hpp``.

Function Definition
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

  namespace ufil
  {
  namespace association
  {

  inline void hungarian(
    const type::CostMatrix & cost_matrix, type::AssignmentMatrix & assignment_matrix)
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

    // Create and solve assignment problem with hungarian algorithm
    auto problem = HungarianAlgorithm<ufil::type::Scalar>(cost_matrix);
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
  ufil::association::hungarian(cost_matrix, assignment_matrix);
  std::cout << "Assignment Matrix:" << assignment_matrix << std::endl;

Parameters
~~~~~~~~~~~~~~~~~~~~~

- `cost_matrix`: The cost matrix to be used for hungarian assignment.
- `assignment_matrix`: The output assignment matrix.

References
--------------------------------

R. Burkard, M. Dell'Amico, S. and Martello, "Assignment Problems: Revised", Society for Industrial and Applied Mathematics (SIAM), 2012

Reference Implementation: M. Emam, https://github.com/mxemam/hungarianAlgorithm, 2020
