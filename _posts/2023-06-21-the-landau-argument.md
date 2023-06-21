---
layout: post
title: The Landau Argument
date: 2023-06-21 19:38 +0530
math: true
---

At the temperature $T = 0$, a one-dimensional Ising system will be in one of the two states 
of minimal energy—for example, in the one in which all spins are aligned in the $+$ direction. 
The problem is whether this state can persist in the presence of thermal fluctuations 
at $T > 0$. Let us assume that we switch the direction of a certain number of consecutive 
spins—we will obtain an excited state, with an energy that is $2 J$ above the minimum. The 
number of states that have this energy is proportional to $ln N$, because we can arrange 
each boundary between $+$ and $-$ spins in $N$ different fashions. Therefore, as soon as $k_BT 
ln N > 2 J$, reversing a macroscopic number of spins leads to an advantage in free energy. 
But for $N \rightarrow \infty$, this will be true for any positive value of $T$. This 
argument can immediately be generalized to all cases of short-range interaction.

## Exercise
Let us suppose that the interaction is long range, so that the coupling constant $J_{ij}$ 
between the $i$ spin and the $j$ spin decays as $|i - j|^{–a}$, where $a$ is a positive constant. 
Show that Landau’s argument is not valid if $a < 2$.

> A solution to this problem can be found in Tridib Sahu's Advanced Statistical Mechanics lectures.

{% include embed/youtube.html id='mMAVPah6iIw' %}
