---
layout: post
title: LaTeX in Markdown
description: >
  Note: This is just a test post. Will be up and running asap!
math: true
---

$$\LaTeX$$ is an amazing language for typesetting beautiful looking documents. It's especially  useful if you deal with a lot of math. Here's an example:

$$\dot{v} = - \zeta v + \eta(t)$$

## Getting started with Markdown

Markdown is a nice tool to quickly write nicely formatted plaintext (without all the fuss).

Let's get started! 

It's quite easy to format text in markdown: This is **bold**. And this is *italics*.

>This is a blockquote.
>
> *"You can write some quotes here."*

Now some grocery list. Comes in quite handy:

1. Apples
2. Bananas
3. Guavas

You can also have bullets. Great Scott!

- One bullet
- Two bullets
- Three bullets

Typing another equation . . .

$$\alpha+\beta+\gamma=0$$

How about some *inline* math, like $$ F = m a $$ .

Or would you like something fancy? See [KaTeX](http://katex.org):

$$\displaystyle \frac{1}{\Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{\frac25 \pi}} = 1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}} {1+\frac{e^{-8\pi}} {1+\cdots} } } }$$

*Note*: I'm using MathJax now with a Jekyll plugin.

Here's some *C* code. Indent text to get a codeblock:

    printf("%s\n","I'm a codeblock.");

*Note*: Markdown (on it's own) doesn't support syntax highlighting.

If you want nicely colored code, use "fenced" codeblocks:
``` c
printf("%s\n","I'm a codeblock.");
// with syntax highlighting
```

You can also do it the Jekyll way:

{% highlight c %}
    /* Some ritualistic code*/
    #include <stdio.h>
    #include <math.h>

    int main()
    {
        printf("%s\n","Hello world!");
    }
    //=> prints 'Hello world!' to STDOUT.
 
{% endhighlight %}


This is some text, followed by a footnote [^1].

[^1]: Some *crazy* footnote, As You Like It.

*TO BE UPDATED* . . .

(As I learn More)
