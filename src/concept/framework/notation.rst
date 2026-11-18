.. _notation:

========================
Notation and Conventions
========================

This page summarizes the notation and conventions used throughout this documentation. 
Understanding these symbols and formats is essential for reading formulas, 
algorithms, and descriptions consistently.

Vectors and Matrices
======================================

- **Vectors** are represented by lowercase **bold** letters, e.g., :math:`\pmb{a}`.
- **Matrices** are represented by uppercase **bold** letters, e.g., :math:`\pmb{A}`.
- **Elements** of vectors or matrices are written in non-bold with subscripts, e.g., :math:`a_i` or :math:`A_{i,j}`, referring to the corresponding vector :math:`\pmb{a}` or matrix :math:`\pmb{A}`.

Sets
====

- Sets of elements are denoted using **calligraphic letters**, e.g., :math:`\mathcal{A}`.

Operations
==========

- The **transpose** of a vector or matrix is denoted by the superscript :math:`\left(.\right)^T`.
- The **inverse** of a matrix is denoted by :math:`\left(.\right)^{-1}`.

Scripts
=======

- An **estimate** of a true value :math:`\left(.\right)` is denoted by :math:`\hat{\left(.\right)}`.
- A **measurement** of a true value :math:`\left(.\right)` is denoted by :math:`\tilde{\left(.\right)}`.
- A **prior (predicted)** of a true value :math:`\left(.\right)` is denoted by :math:`\left(.\right)^{-}`.
- A **posterior (updated)** of a true value :math:`\left(.\right)` is denoted by :math:`\left(.\right)^{+}`.

Time Indexing
=============

- The subscript :math:`\left(.\right)_k` denotes the value at **time step** :math:`k`.
- The subscript :math:`\left(.\right)_{j,k}` denotes the **j-th value** of :math:`\left(.\right)` at time step :math:`k`.
- Predicted values **before including evidence from the current time step** are written as :math:`\left(.\right)_k^{-}`. 
  In some literature, the same value is written as :math:`\left(.\right)_{k|k-1}`.

Scope Indexing
==============

- Superscript :math:`\left(.\right)^i` indicates the value of :math:`\left(.\right)` in **scope** :math:`i`, 
  where :math:`i` identifies a particular (sub)system or aggregation level.