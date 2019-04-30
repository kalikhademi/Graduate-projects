## Homework 1:
Homework consisted of two parts which are explained as follow:
# Polynomial curve fitting:
In this part, we were asked to write a small script to generate separate training and validation dataset from the true   function Sinc(x) with added zero-mean gaussian noise. Then, we fit our model into the data and compare the error accros different model orders to investigate the appropriate one for this problem. 
   
# Maximum Likelihood(ML)and Maximum A Posteriour(MAP)for Gaussian distribution:
wrote an iterative script that draws a point from the true Gaussian Distribution( with known mean). In each iteration, we compute ML and MAP solutions for gaussian mean. Right after each draw, the prior distribution would be updated by replacing it with the posterior distribution from previous draw. 
Following questions are investigated and responded in my report:
- What happens when the prior mean is initialized to the wrong value? To the correct value?
- What happens as you vary the prior variance from small to large?
- What happens when the likelihood variance is varied from small to large? 
- How do the initial values of the prior mean, prior variance, and likelihood variance interact to effect the final estimate of the mean?

Contributor: Kiana Alikhademi

Reference:
1. Bishop, C.M., 2006. Pattern recognition and machine learning (information science and
statistics) springer-verlag new york. Inc. Secaucus, NJ, USA.
