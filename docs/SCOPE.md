# Scope

The first release answers one question:

> For an area-one flat torus, which closed-loop lengths belong to the
> shape, and which apparent changes are only a change of lattice labels?

It does **not** claim to be a general computational-geometry platform.

## In scope

- The area-normalized lattice `Lambda_tau = y^{-1/2}(Z + tau Z)` with `Im(tau) > 0`.
- Exact lengths `ell_{m,n}(tau) = |m + n tau| / sqrt(y)` for integer windings.
- Wrapping a straight-line lift through the fundamental parallelogram.
- The modular generators `T: tau |-> tau+1` and `S: tau |-> -1/tau`, acting jointly
  on the shape parameter and the winding labels.
- A parallelogram figure drawn from the same `ClosedTrajectory` the
  tests use.

## Out of scope until implemented and tested

- Continuous paths through the upper half-plane, including hyperbolic
  geodesics of moduli space.
- Square-tiled surfaces other than the square torus, and interval-exchange
  maps.
- Numerical geodesic integrators and Jacobi fields.
- Metrics on symmetric positive-definite matrices.
- Discrete intrinsic geodesics on triangle meshes.
- Treating a smooth embedded torus of revolution as the computational
  object.

A change of representation must transform the trajectory description
along with the lattice description. The testbed refuses to treat
`ell_{m,n}(tau)` and `ell_{m,n}(tau+1)` as the same comparison.
