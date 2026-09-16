# Methods

## Area normalization

Write `tau = x + i y` with `y > 0`. The un-normalized lattice `Z + tau Z`
has fundamental area `y`. Scaling generators by `y^{-1/2}` produces

```text
omega1 = y^{-1/2},     omega2 = tau * y^{-1/2}.
```

The parallelogram they span has area

```text
Im(conjugate(omega1) * omega2) = 1.
```

Two values `tau = i` and `tau = 4i` therefore describe different shapes of
the same area. Their primitive generator lengths are `(1, 1)` and
`(1/2, 2)`.

## Closed geodesics

On a flat torus every geodesic lifts to a Euclidean straight line. The
line in class `(m, n)` is the lattice vector `m omega1 + n omega2`. Its length
is exact. In lattice coordinates the same geodesic is the periodic path
`(alpha0 + m t, beta0 + n t)` reduced modulo `1`.

Integer windings close after time `1` in that parametrization. The
number of side hits in one period is `|m| + |n|` when the start is
generic; a start at a lattice point can send the path through corners.

## Modular invariance

`SL(2, Z)` acts on the upper half-plane by fractional linear
transformations. The first-release checks use the standard generators

```text
T = [[1, 1], [0, 1]]     tau |-> tau + 1
S = [[0, -1], [1, 0]]    tau |-> -1/tau
```

Winding labels transform by `g^{-1}` so that `m omega1 + n omega2` names the
same cover vector after the basis change. For `T` this is
`(m, n) |-> (m - n, n)`. Directly:

```text
(m - n) + n (tau + 1) = m + n tau
```

so the un-normalized numerator is identical and `y` is unchanged.

`T` leaves the lattice set `Lambda_tau` itself fixed. `S` produces an isometric
area-one torus (the lattice is rotated). Both leave `ell` invariant once
labels move. They do not leave `ell` invariant if the labels are held
fixed.

## What a figure is allowed to do

The explorer draws the computed parallelogram and the computed wrapped
polyline. It does not integrate a curved metric, and it does not own a
second copy of `ell_{m,n}`.
