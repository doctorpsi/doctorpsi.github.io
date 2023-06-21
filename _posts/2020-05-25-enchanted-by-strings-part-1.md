---
layout: post
title: Enchanted by Strings | Part 1
description: >
    Diabolically stolen from the classic Plischke & Bergensen
math: true
---

> **TL;DR**: This series consists of my personal notes on a beautiful chapter on *polymers* and *membranes* that I found amusing. The contents of this blog are directly taken from here. Please refer to the original text of *Equilibrium Statistical Physics* by Plischke & Bergersen for more details. If you are afraid of math and scary looking equations, then this post and the others are not for you. The material covered is pretty elementary though, suitable for an ambitious upper undergraduate or a graduate (presumably in Physics).
>
> In this episode, we discuss the basic aspects of the statistical mechanics of flexible linear polymers.

As promised in our [last episode](/2020/05/23/enchanted-by-strings-part-0.html), we will now discuss linear polymers, which is the simplest architecture or topology we can think of. In what follows, we will treat polymers to be simply long flexible chains. Imagine a really long string or a spaghetti strand. We will ignore all the microscopic details as mentioned before. Plischke & Bergersen give a quick run through the basic chemistry of the flexibility mechanism right at the beginning. We will, however, skip this portion and jump straight to the interesting part. The reader is strongly encouraged to refer to the original text.

Now to talk about flexibility, it is fairly intuitive that as you go along the chain there will be a rapid loss of "memory". What we mean by memory will be clear in a second. There is a peculiar length scale $$ l $$ over which the bond orientations become uncorrelated, known as the *persistence length*. It is an important feature which gives flexible polymers their universal structural properties. This length depends on microscopic details and is different for various kinds of polymers. Any polymer having its persistence length much smaller than the contour length, *i.e.*, $$ l \ll Na $$ ( $$ a $$ being the bond length) should have physical properties depending *universally* on $$ Na/l $$. This is true because one can always think in terms of beads or monomers of size $$ l $$ instead of actual atoms [^1]. Chain segments smaller than the persistence length are practically straight (correlations "persist"). On the other hand, if we consider lengths greater than $$ l $$, we see that the correlations now vanish entirely allowing the chain to freely flex or bend. The polymer chain can then be treated as a long flexible mass of $$ Na/l $$ links, with all its global properties depending only on this particular number ("universality").

Interestingly, the highly disordered bond orientations make the polymer configuration close in many ways to a *biased random walk*. For flexible polymers, we will show that the statistical mechanics of these systems is nothing but a maximization of the entropy of a random walk to a first approximation. However, this deep connection or rather analogy does not make the polymer problem any simpler. In fact, it is far more challenging than the familiar random walk problem as the polymer chain can never cross itself. The atoms on the chain have hard core repulsion which prevent them from occupying the same region in space. So we have what is called a *self-avoiding walk*, which is not so easy to deal with. The chain expands (or swells) in a nontrivial manner at least for dimensions $$ d < 4 $$, which is the *upper critical dimension* [^2] for our problem at hand. We will talk more about this concept later since it plays an important role in the study of critical phenomena.

Now the appearance of an upper critical dimension hints at something really deep: the polymer problem is in a sense a critical phenomenon problem. We shall see soon that this is certainly true. It is this duality which allows us to cleverly map the former onto the latter, and hence take advantage of the huge wealth of information that is known about critical phenomena (along with its rich machinery [^3]). It should be noted that this hardcore (or *excluded volume*) interaction, although short ranged in $$ d $$-dimensional space is *long ranged* if we consider the distance along the chain. Monomers far apart along the chain can interact strongly if the chain folds back unto itself. This feature makes our polymer problem a highly nontrivial one.

In the next section, we begin our main discussion of the statistical mechanics of polymers by taking the simplest model, *viz.* the "freely jointed chain".

## The freely jointed chain

*COMING SOON* . . . :trident: 

[^1]: This is the gist of *coarse-graining* we talked about earlier.

[^2]: See any text on phase transitions and critical phenomena.

[^3]: The wizardry of field theory and the renormalization group.
