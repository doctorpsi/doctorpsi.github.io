---
layout: post
title: The Landau Argument
date: 2023-06-21 19:38 +0530
math: true
---

There is a famous argument, usually attributed to Landau, against the existence of long-range order in 1D.
Consider the one-dimensional Ising model at temperature $T = 0$. There are only two possible ground states—
one where all the spins are pointing upwards, and the other where spins are pointing downwards. Now imagine
gradually increasing the temperature to $T > 0$. Will the initial state remain stable against thermal
fluctuations?

Let us now flip a few adjacent spins. This will creates a excited state with an excess energy of $2 J$.
Since we can arrange each $+/-$ spin boundary in $N$ different ways, the number of microstates is proportional
to $ln N$. As soon as $k_BT ln N > 2 J$, flipping a large number of spins leads to a free energy advantage.
The system will keep flipping spins to minimize free energy and thus won't remain stable. This will be true
for any nonzero temperature $T$ in the thermodynamic limit, $N \rightarrow \infty$.

## Exercise
Let us suppose that the interaction is long range, so that the coupling constant $J_{ij}$
between the $i$ spin and the $j$ spin decays as $|i - j|^{–a}$, where $a$ is a positive constant.
Show that Landau’s argument is not valid if $a < 2$. (see *Peliti, Statistical Mechanics in a Nutshell*, 2011)

> A straightforward solution to this problem can be found in Lecture 21 of [TIFR Graduate School course on
Advanced Statistical Physics: February - July, 2021](https://theory.tifr.res.in/~tridib/ASPCourse.html) by
Tridib Sadhu. These lectures are highly recommended to any graduate student in dire need of brushing up on their
Statistical Mechanics.

{% include embed/youtube.html id='mMAVPah6iIw?start=1422&end=2009' %}

P.S. The above exercise was in fact published as a short paper (less than 2 pages!) by David Thouless way back
in 1969. This was highly instrumental in the development of the famous theory of Kosterlitz-Thouless transition
later on. The 2016 Nobel Prize in Physics was awarded to the duo (along with Duncan Haldane) for this highly
cited work among others.
