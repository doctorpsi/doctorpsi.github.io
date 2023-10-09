---
layout: post
title: The Landau Argument
date: 2023-06-21 19:38 +0530
math: true
---

There is a famous argument, usually attributed to Landau [^footnote1], against the existence of long-range order
in one dimension with short-range forces. I'll present below a version given by David Thouless---of the
[Kosterlitz-Thouless](https://en.wikipedia.org/wiki/Berezinskii%E2%80%93Kosterlitz%E2%80%93Thouless_transition)
fame---in 1969. It was published in a remarkably short paper [^footnote2] of just over
two pages!

Consider the 1D Ising model [^footnote3] of $N$ spins at temperature $T = 0$. There are only two possible
ground states---one where spins are all pointing up and the other where they are all pointing down. Now imagine
increasing the temperature to $T > 0$. Will the initial ordered state remain stable against thermal fluctuations?

Let us flip the first few spins. This will create an excited state with an excess energy $\Delta U$ of
$2 J$ (coupling $J > 0$) as only one boundary, costing energy $2 J$, separates the "up" and "down" spin regions.
Since there are $N$ possible ways of arranging the *domain wall*, the change in entropy $\Delta S$ is proportional
to $ln N$.

Whenever the entropic contribution $k_BT ln N > 2 J$,[^footnote4] the system will flip spins to decrease its free
energy: $\Delta F = \Delta U - T \Delta S < 0$. This must happen for any nonzero temperature $T$ in the
thermodynamic limit, $N \rightarrow \infty$. So the ordered state can never be stable. In other words, long-range
order is impossible in 1D!

## A Fun Little Exercise
Let us suppose that the interaction is long range, so that the coupling constant $J_{ij}$
between the $i$ spin and the $j$ spin decays as $|i - j|^{–a}$, where $a$ is a positive constant.
Show that Landau’s argument is not valid if $a < 2$. (Peliti, 2011) [^footnote5]


> Try solving on your own first. If you need help, you can have a look at Lecture 21 of Tridib Sadhu's
[TIFR Graduate School course on Advanced Statistical Physics: February - July, 2021](https://theory.tifr.res.in/~tridib/ASPCourse.html)
below. These lectures are highly recommended to any graduate student wanting to brush up on their
Statistical Mechanics. Be warned that some of the lectures are quite advanced, even for yours truly!

{% include embed/youtube.html id='mMAVPah6iIw?start=1422&end=2009' %}

P.S. The above exercise is undoubtedly adapted from Thouless's [1969 paper](https://journals.aps.org/pr/abstract/
10.1103/PhysRev.187.732), which played an important role in the development of the
[prize-winning](https://www.nobelprize.org/prizes/physics/2016/summary/) Kosterlitz-Thouless theory later on.

[^footnote1]: LD Landau and EM Lifshitz, *Statistical Physics* (Pergamon Press, London, 1958), p.482
[^footnote2]: DJ Thouless, Long-range order in one-dimensional Ising systems, *Physical Review* **187**, 732–733 (1969).
[^footnote3]: For simplicity, assume that the magnetic field is zero: $H_{Ising} = -\sum_{\langle i j \rangle} J S_i S_j$
[^footnote4]: Note that the RHS (or $J$) is independent of N only for short-range interactions.
[^footnote5]: Luca Peliti, *Statistical Mechanics in a Nutshell*, Exercise 5.5, p.142 (2011)
