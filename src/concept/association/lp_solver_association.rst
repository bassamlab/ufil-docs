.. _lp_solver_association:

=========================================================
Linear Programming Solver
=========================================================

Overview
--------
The LP Solver formulates the assignment problem as a linear programming (LP)
optimization problem and solves it using the Simplex method.

Unlike combinatorial solvers such as Hungarian or Jonker–Volgenant, this
approach models the assignment as a linear objective function subject to
linear constraints.

In UFIL, the solver converts the assignment problem into standard LP form and
computes a globally optimal solution.

Methodology
-----------

The solver uses a tableau-based Simplex implementation:

1. **Initialization**  
   Transform the assignment problem into standard LP form and construct
   the initial Simplex tableau.

2. **Pivot Selection**  
   - Select pivot column using the most negative reduced cost.
   - Select pivot row via minimum positive ratio test.

3. **Pivot Operation**  
   Normalize pivot row and eliminate other entries in the pivot column.

4. **Termination**  
   Stop when no negative values remain in the objective row.

5. **Assignment Extraction**  
   Construct the final assignment matrix from the optimal tableau.

Characteristics
---------------
- Globally optimal solution
- Flexible problem formulation
- Supports non-square matrices
- Suitable for extended constraint formulations

Limitations
-----------
- Potentially higher computational overhead
- Worst-case exponential complexity
- Sensitive to numerical scaling

Selection Notes
---------------
Choose the LP Solver when:

- The problem is naturally expressed as a linear optimization problem
- The cost matrix is non-square
- Additional linear constraints may be added in the future

Consider alternative algorithms when:

- Real-time constraints are strict
- The matrix is large and square
- The problem is non-linear or integer-constrained

Code Documentation
--------------------

The interface to the LP Solver is implemented in ``association_functions.hpp``
and the underlying implementation in ``lp_solver.hpp``.

Function Definition
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

  namespace ufil
  {
  namespace association
  {

  inline void lp_solver(
    const type::CostMatrix & cost_matrix,
    type::AssignmentMatrix & assignment_matrix)
  {
    const auto n_rows = cost_matrix.rows();
    const auto n_cols = cost_matrix.cols();

    // No assignment if matrix is empty
    if (!(n_rows > 0 && n_cols > 0)) {
      return;
    }

    const type::Scalar max_coeff = std::max(cost_matrix.maxCoeff(), static_cast<type::Scalar>(1.0));
    type::CostMatrix cost_matrix_invers = type::CostMatrix::Constant(n_rows, n_cols,
          max_coeff) - cost_matrix;

    // Resize and initialize assignment matrix
    assignment_matrix.resize(n_rows, n_cols);
    assignment_matrix.setZero();

    // Create and solve assignment problem with Jonker-Volgenant algorithm
    auto problem = LP_Solver<ufil::type::Scalar>(cost_matrix_invers);
    problem.SolveAssignmentProblem();

    type::AssignmentMatrix assignment_matrix_padded;
    assignment_matrix_padded.resize(n_rows, n_cols);
    assignment_matrix_padded.setZero();

    // Set assignment matrix with solution
    problem.GetAssignmentMatrix(assignment_matrix_padded);

    assignment_matrix.resize(n_rows, n_cols);
    assignment_matrix.setZero();
    assignment_matrix = assignment_matrix_padded.block(0, 0, n_rows, n_cols);
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
  ufil::association::lp_solver(cost_matrix, assignment_matrix);
  std::cout << "Assignment Matrix:" << assignment_matrix << std::endl;

Parameters
~~~~~~~~~~~~~~~~~~~~~

- `cost_matrix`: The cost matrix to be used for LP Solver assignment.
- `assignment_matrix`: The output assignment matrix.

