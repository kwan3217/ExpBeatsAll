## The Race

Let's have a race between functions. In the red corner, we
have $x^2$, and in the blue corner, we have $e^x$. 
  > Graphic: red $f(x)=x^2$, then blue $g(x)=e^x$

Which function is greater as $x$ increases?

Let's compare the two contestants on a graph:

  >graph - red $x^2$ curve and blue $e^x$ curve, scaled
  >to fit on the y axis, and running from about [0,5] on
  >the x axis.

In this race, it's no contest. $e^x$ is greater than $x^2$ 
at every point in time. What about $x^5$? 

  > graph - scale power in polynomial smoothly from 2 to 5, red curve
  > will go off top of screen. Once finished, change vertical scale
  >to fit red curve, showing that red curve exceeds blue curve

In this case, $x^5$ starts out greater but $e^x$ passes it in about
15 time units. 

  > scale horizontally to wide enough to show blue curve overtaking
  > red curve

Even for $x^20$, although it takes a while, $e^x$ will eventually pass it.

  > Same thing, vary power from 5 to 20, scale graph vertically to fit,
  > scale graph horizontally enough to show blue winning
 
It turns out that no matter what $n$ you choose for 
$x^n$, $e^x$ will eventually exceed it.


## LHopital2A - The Rule Introduced

We can use a spreadsheet and check which function is greater,
but how do we know that the curves will never cross back over?
Actually, we can prove this a couple of ways. One way is to use
L'Hopital's rule. This theorem allows us to evaluate $f(x)/g(x)$
as $x$ grows without bounds. 

 > Show the definition of L'Hopital's rule:
 > if $\lim_{x->\infty} f(x)=\infty$
 > and $\lim_{x->\infty} g(x)=\infty$
 > then $\lim_{x->\infty} \frac{f(x)}{g(x)}=\frac{f'(x)}{g'(x)}$

If you want an explanation of why it's true, I recommend the
3blue1brown video from his excellent *Essence of Calculus* series.
 > Clip of his video with an i card pointing at it

Here, we will just use the result. Let's start off with both $f$ and $g$
being polynomials, say $f(x)=x^4$ and $g(x)=x^5$. 
 > Split the screen and show the definition on the left and numerator
 > and denominator on upper and lower right respectively. Crank through
 > the differentiation, doing the upper and lower separately but
 > ultimately the same number of times, until one isn't infinite any more. 

### Paragraph 2
This is indeterminate,
so we can apply the rule and take the derivative of both functions, knowing
that *their* ratio is the same as the original indeterminate ratio. In this
case, the ratio is *still* indeterminate, so we keep differentiating the top and the bottom until
one of the functions is ground down to a constant. Then we have to stop, as
we no longer have an indeterminate form. In this case, the numerator has
been ground down to a constant, while the denominator still has an $x$ in
it and will therefore still go to infinity as $x$ does. Our form is now
a finite number divided by infinity, which is always zero. This means
that this is *also* the ratio of the original form. The numerator, even
though it is infinite, is a much smaller infinity than the denominator, such
that it is literally nothing in comparison.

If the upper polynomial were to have a greater order and remain infinite,
then the final answer would be infinity divided by a finite number, which
remains infinity. If the term "infinity" bothers you, just replace the offending
word with "increases without bound as $x$ increases without bound". That's what I 
mean by infinity in this context, and it *is* rigorous.

Note that the same thing happens if we have polynomials with multiple terms:
the lower-order terms get ground down to a constant, then to zero, before the
higher order terms come into play. The highest-order term on either side is
the only one that matters, and whichever side has the *higher* highest-order
term wins.

Even if the polynomials have coefficients, the coefficients don't matter. The
coefficients of the lower terms get ground off with their terms, and the
coefficient of the highest term gets lumped in with the final finite number.

### LHopital 2C - Applied to the race 

Now that we've played around with L'Hopital's machine a bit, let's use it for
our original problem. We will use $f(x)$ for the polynomial and $g(x)$ for the
exponential. As we saw before, the derivative of a polynomial eventually gets ground
down to a constant, at which point you have to stop L'Hopital's rule,
because you don't have the indeterminate form any more. However, 
the exponential function is indestructible -- its derivative is
always equal to itself. Once the polynomial is ground down, the
exponential will still go to infinity, and then you'll have a
finite number divided by infinity. Any finite number divided by
infinity is zero. This means that in the long run, any polynomial
is insignificant next to the exponential. The exponential beats all.

## Taylor Series
Another way to look at it is with the Taylor series. For any 
polynomial, the Taylor series is just that polynomial. For
the exponential, since it is indestructible, it will have
derivatives of all orders, and its Taylor series is itself
effectively an infinite degree polynomial. The higher terms
are divided by large factorials, but eventually each term
grows large enough to overcome its denominator and dominate
the function, until the next term takes over, etc etc forever
and ever.  

So what is this little gem used for? The one near and dear to my 
heart is in aerospace engineering, and it's called maximum dynamic
pressure. In a rocket launch, dynamic pressure tells us how hard
the relative wind is blowing against the rocket. Once the rocket passes 
through maximum dynamic pressure, or max $q$, the pressure on the rocket
decreases, even though the speed and altitude are still increasing.
The rocket has punched through the thick part of the atmosphere and
things just get easier from there on. Once the rocket has passed max
$q$, it has cleared one of the highest hurdles on the way to orbit.

So why is there a *max* $q$? Dynamic pressure itself is calculated
from two terms, one of which is proportional to the square of the
speed, and one of which is proportional to the atmospheric density.
This density itself is an exponentially decaying function of altitude.
As a first approximation, let's say that both the speed and altitude
are proportional to time. In this case, the speed term is a polynomial,
and multiplying by an exponential decay is the same as dividing by an
exponential. Our dynamic pressure is then in the $f(x)/g(x)$ form
we've seen before. As our rocket launches, the polynomial term starts
out winning, and dynamic pressure increases. But eventually as we have
seen, the exponential term catches up, passes the polynomial term, and
stays increasingly ahead from then on. We've now passed max $q$ and
dynamic pressure decreases from then on. In the limit, the polynomial
term is so much smaller than the exponential term that dynamic pressure
goes to zero, as we reach the near-vacuum of space.

I'd like to give a big shout-out to 3blue1brown and the Summer of Math 
Explanation program, for the inspiration to finally do *something* and
get it posted. Thanks also to Think Twice for inspiration about mathematics
videos that don't have to be a full lesson, just one shiny gem. This has
been kwan3217, saying if at first you don't succeed, fly, fly again.