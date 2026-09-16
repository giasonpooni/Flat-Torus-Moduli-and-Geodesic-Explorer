# Development workflow

Maintain the Flat-Torus Moduli and Geodesic Explorer as one project on `main`.

- Work directly on `main` and push completed, validated changes to `origin/main`.
- Do not create development branches, separate project copies, or pull requests unless
  the user explicitly requests them.
- Fetch before pushing, preserve concurrent work, and never force-push `main`.
- Run the default test suite and the quickstart example before pushing library changes.
- Keep the README focused on delivered functionality. Mark research extensions as planned
  until implemented and validated.
- Delivered scope is the area-one flat torus, exact loop lengths, integer windings,
  modular invariance under T, S, and general SL(2, Z) words, a fundamental-domain
  fold, and a parallelogram view that consumes those objects.
- Do not treat a doughnut embedding as the metric. Do not treat a change of lattice
  basis as a change of shape. Do not compare windings without transforming their labels.
- Motion through moduli space, translation surfaces, Jacobi fields, covariance geometry,
  and mesh geodesics belong to other projects or later phases.
