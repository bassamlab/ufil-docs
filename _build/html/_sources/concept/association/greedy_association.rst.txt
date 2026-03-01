.. _greedy_associator:

=========================================================
Greedy Associator
=========================================================

Overview
--------
The Greedy Associator implements a fast heuristic solution to the linear
assignment problem.

Instead of guaranteeing global optimality, it iteratively selects the smallest
available cost and assigns the corresponding row and column.

This approach significantly reduces computational effort and is well suited
for real-time systems.

Algorithm Steps
---------------

1. **Initialization**  
   Create row and column index sets.

2. **Row Minima Computation**  
   Determine the minimum-cost column for each row.

3. **Greedy Selection**  
   Select the smallest cost among row minima.
   - If the column is free, assign it.
   - Otherwise, update the row minimum.

4. **Iteration**  
   Remove assigned rows and columns and repeat.

5. **Termination**  
   Stop when no rows or columns remain.

Characteristics
---------------
- Very fast
- Low computational complexity
- Scales well for large problems
- Works with non-square matrices

Limitations
-----------
- Does not guarantee optimality
- Assignment quality depends on cost distribution

Selection Notes
---------------
Choose the Greedy Associator when:

- Speed is more important than optimality
- Approximate solutions are acceptable
- Real-time performance is critical

Use alternative algorithms when:

- High accuracy is required
- Global optimality is mandatory

Code Documentation
-------------------

The interface to the Greedy Associator is implemented in ``association_functions.hpp``
and the underlying implementation in ``greedy_associator.hpp``.

Function Definition
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

  namespace ufil
  {
  namespace association
  {

  inline void greedy(
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
    auto problem = GreedyAssociator<ufil::type::Scalar>(cost_matrix);
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
  ufil::association::greedy(cost_matrix, assignment_matrix);
  std::cout << "Assignment Matrix:" << assignment_matrix << std::endl;

Parameters
~~~~~~~~~~~~~~~~~~~~~

- `cost_matrix`: The cost matrix to be used for greedy assignment.
- `assignment_matrix`: The output assignment matrix.