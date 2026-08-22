# Putnam-like errata

This file records confirmed issues in the released Putnam-like benchmark without
rewriting the historical problem statements, samples, or grades in place.

## Set 2, B6

The published problem statement asks to prove

\[
\int_0^\infty \frac{e^{-2x}}{1+x^2}\,dx
=
\int_0^\infty \frac{\cos x}{2+x}\,dx.
\]

This identity is false. The intended trigonometric integrand is `sin`, for which

\[
\int_0^\infty \frac{e^{-2x}}{1+x^2}\,dx
=
\int_0^\infty \frac{\sin x}{2+x}\,dx.
\]

A direct Laplace-transform calculation shows the distinction. Using

\[
\frac{1}{2+x}=\int_0^\infty e^{-(2+x)u}\,du,
\]

and exchanging the order of integration gives

\[
\int_0^\infty \frac{\cos x}{2+x}\,dx
=
\int_0^\infty \frac{u e^{-2u}}{1+u^2}\,du,
\]

whereas

\[
\int_0^\infty \frac{\sin x}{2+x}\,dx
=
\int_0^\infty \frac{e^{-2u}}{1+u^2}\,du.
\]

The grading rubric contains a compensating error. For

\[
g(t)=\int_0^\infty \frac{\cos x}{t+x}\,dx,
\]

the integration-by-parts boundary term is `1/t^2`, not `1/t`. Consequently the
cosine integral does not satisfy the same differential equation used for the
left-hand side. Replacing `cos` with `sin` makes the intended argument valid.

The existing Set 2/B6 samples and grades were produced against the published
`cos` statement and are intentionally left unchanged for reproducibility. Users
comparing historical benchmark results should treat this item as affected by the
erratum.

See issue #7 for the original report and derivation.
