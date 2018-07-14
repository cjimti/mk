---
published: false
layout: post
title: The Foundational Mathematics of Machine Learning
tags: coding python
featured: coding python
mast: math
---
This article is brief overview of the foundational mathematics of machine learning. At it's core, the math is simple summation and multiplication. Machine learnings most complext parts come at the higher levels of implementation.


[LaTex]:https://en.wikibooks.org/wiki/LaTeX/Mathematics

## Prediction

$$\hat{y} = \sigma\left(W_x + b\right)$$


## Error Function

$${E}\left({W}\right) = -\frac{1}{m}\sum_{i=1}^{m} y_iln\left(\hat{y_i}\right) + \left(1 - y_i\right)ln\left(1 - \hat{y_i}\right)$$

## Gradient (Decent) of The Error Function

$$\nabla{E} = \left(\frac{\partial E}{\partial w_1},\cdots,\frac{\partial E}{\partial w_n},\frac{\partial E}{\partial w_b}\right)$$

## Gradient Descent with Squared Errors

$$ E = \frac{1}{2}\sum_{\mu}\sum_{j}\left[y^\mu_j - \hat{y}^\mu_j\right]^2$$

>The SSE is a good choice for a few reasons. The square ensures the error is always positive and larger errors are penalized more than smaller errors. Also, it makes the math nice, always a plus.

- ${y}$ is the true value
- $\hat{y}$ is the prediction
- ${j}$ represents the output units of the network
- ${\mu}$ is a sum over all the data points

> Remember that the output of a neural network, the prediction, depends on the weights

$$\hat{y}^\mu_j = f\left(\sum_{i}w_{ij} x^\mu_i\right)$$

> and accordingly the error depends on the weights



```python
import numpy as np
```

## Sigmoid $\sigma(x)$


```python
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

sigmoid(2.5)
```




    0.92414181997875655



## Prediction $\hat{y}$


```python
def predict(W,x,b):
    return sigmoid((W * x) + b)

print(predict(16,.38,10))
(predict(1,.38,.1))
```

    0.999999896117





    0.61774787476924897




```python
# Activation (sigmoid) function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def sigmoid_prime(x):
    return sigmoid(x) * (1-sigmoid(x))
def error_formula(y, output):
    return - y*np.log(output) - (1 - y) * np.log(1-output)
```
