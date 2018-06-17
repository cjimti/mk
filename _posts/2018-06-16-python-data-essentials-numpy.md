---
published: true
layout: post
title: Python Data Essentials - Numpy
tags: coding python
featured: python coding
mast: sorting
---
Python is one of [The Most Popular Languages for Data Science], and because of this adoption by the [data science] community, we have libraries like [NumPy], [Pandas] and [Matplotlib]. [NumPy] at it's core provides a powerful N-dimensional array objects in which we can perform linear algebra, [Pandas] give us data structures and data analysis tools, similar to working with a specialized database or powerful spreadsheets and finally [Matplotlib] to generate plots, histograms, power spectra, bar charts, error charts and scatterplots to name a few.

**Quick Reference:**

* Do not remove this line (for toc on rendered blog)
{:toc}

## Microservices Data Eco-System

I am not a data scientist, but like most software architects and full stack developers, I interact with data science at many points. However, where I spend the majority of my time building frameworks and pipelines, data science has been busy churning out amazing libraries.

One of the advantages of microservice architecture allows not only a higher level of the separation of responsibility but allowing each service to leverage the ecosystem most suited to it. While Monoliths often embed DSLs like SQL or use language bindings libraries to use C drivers in a Java application, they must be written to the strengths of the language to get the most out of them.

It's 2018, and in my world [Go] binaries power most of my containerized API endpoints, Python functions run in [kubeless] configurations, and it's all wired together in [kubernetes] with it's robust [services] and [ingress] management. In this team of experts, I let Python do the math, why? Because libraries like [NumPy] and [Pandas] make the kind of math, I need easy, fast and maintainable.

The [NumPy] and [Pandas] libraries have a tremendous number of options far too many to cover here, but the documentation is fantastic, so, for this reason, I'll only be going over the essentials. Once you get past the essentials, you'll need the documentation. However, if you are like me you don't do the same job every day, so you only need to be an expert in the essentials of many things and the documentation and google lead you to the experts in whatever niche of functionality you are set to build.

This article will focus on [NumPy] because it is one of the core numeric libraries that most of the [scientific Python ecosystem](http://www.physics.nyu.edu/pine/pymanual/html/apdx3/apdx3_resources.html) is built on. Understanding and using [NumPy] is vital to effective use of [Pandas] and even [Matplotlib].

[data science]:http://www.scipy-lectures.org/intro/intro.html#why-python
[kubeless]:https://kubeless.io/
[kubernetes]: http://localhost:4000/tag/kubernetes/
[go]:https://golang.org/
[Numpy]:http://www.numpy.org/
[pandas]:https://pandas.pydata.org/
[Matplotlib]:https://matplotlib.org/
[The Most Popular Languages for Data Science]: https://dzone.com/articles/which-are-the-popular-languages-for-data-science
[services]: https://kubernetes.io/docs/concepts/services-networking/service/
[ingress]: https://kubernetes.io/docs/concepts/services-networking/ingress/
[Juypter Notebooks]: http://jupyter.readthedocs.io/en/latest/install.html#installing-jupyter-using-anaconda-and-conda
[Anaconda]: https://www.anaconda.com/download/#macos

## Getting Started with Numpy

This article is written using [Juypter Notebooks] installed and running under [Anaconda]. If you don't already have this setup I highly recomend it, along with download this article itself as a notbook and executing the following examples. All the following code is executes here in [Juypter Notebooks].



```python
!conda list numpy
```

    # packages in environment at /Users/cjimti/anaconda3:
    #
    # Name                    Version                   Build  Channel
    numpy                     1.13.3           py36ha9ae307_4  
    numpy-base                1.14.3           py36ha9ae307_2  
    numpydoc                  0.8.0                    py36_0  


I am running numpy 1.13.3 for the following examples.

### Numpy 1.13 Resources

If you get stuck or interested in learning far more than the examples below, I suggest the following resources:

- [NumPy 1.13 Manual](https://docs.scipy.org/doc/numpy-1.13.0/contents.html)
- [NumPy 1.13 User Guide](https://docs.scipy.org/doc/numpy-1.13.0/user/index.html)
- [NumPy 1.13 Reference](https://docs.scipy.org/doc/numpy-1.13.0/reference/index.html#reference)

For a deep dive on all things [NumPy] try [Scipy Lectures on Numpy](http://www.scipy-lectures.org/intro/numpy/index.html).

Why NumPy? Let's say we would like to find the mean of one hundred million random numbers:


```python
import numpy as np
```


```python
# create some random numbers
x = np.random.random(100000000)
```


```python
%%timeit -n1 -r1
sum(x) / len(x)
```

    6.52 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)



```python
%%timeit -n1 -r1
np.mean(x)
```

    65.7 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)


We wrote less code, arguably more verbose code, and accomplished the same task over one hundred times faster. It's more code if you include the import statment, but that is long forgotton with the 100x speed increase.

Finding the mean of one hundred million random numbers is great use of NumPy, but it get's a lot more interesting with NumPy's powerful N-dimensional arrays. 

### Creating Arrays


```python
x = np.array([1,2,3,4,5])

print(f'data:\n{x}')
print(f' type: {type(x)}')
print(f' size: {x.size}')
print(f'shape: {x.shape}')
```

    data:
    [1 2 3 4 5]
     type: <class 'numpy.ndarray'>
     size: 5
    shape: (5,)



```python
y = np.array([[1,1,1],[2,2,2],[3,3,3]])

print(f' data:\n{y}')
print(f' type: {type(y)}')
print(f' size: {y.size}')
print(f'shape: {y.shape}')
```

     data:
    [[1 1 1]
     [2 2 2]
     [3 3 3]]
     type: <class 'numpy.ndarray'>
     size: 9
    shape: (3, 3)


### Built-in Array Creation Functions


```python
zros = np.zeros((10,12))
print(f' data:\n{zros}')
print(f' type: {type(zros)}')
print(f' size: {zros.size}')
print(f' size: {zros.dtype}')
print(f'shape: {zros.shape}')
```

     data:
    [[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]]
     type: <class 'numpy.ndarray'>
     size: 120
     size: float64
    shape: (10, 12)



```python
f = np.full((5,5), 5)
print(f'5x5 of 5s:\n{f}\n')

print(f' size: {f.size}')
print(f'dtype: {f.dtype}')
print(f'shape: {f.shape}')
```

    5x5 of 5s:
    [[5 5 5 5 5]
     [5 5 5 5 5]
     [5 5 5 5 5]
     [5 5 5 5 5]
     [5 5 5 5 5]]
    
     size: 25
    dtype: int64
    shape: (5, 5)



```python
# Identity and Diagonal Matrix
ident = np.eye(8)
print(f'Identity matrix:\n{ident}\n')

diag = np.diag([2,4,5,6,8,10,12])
print(f'Diagonal Matrix:\n{diag}\n')
```

    Identity matrix:
    [[ 1.  0.  0.  0.  0.  0.  0.  0.]
     [ 0.  1.  0.  0.  0.  0.  0.  0.]
     [ 0.  0.  1.  0.  0.  0.  0.  0.]
     [ 0.  0.  0.  1.  0.  0.  0.  0.]
     [ 0.  0.  0.  0.  1.  0.  0.  0.]
     [ 0.  0.  0.  0.  0.  1.  0.  0.]
     [ 0.  0.  0.  0.  0.  0.  1.  0.]
     [ 0.  0.  0.  0.  0.  0.  0.  1.]]
    
    Diagonal Matrix:
    [[ 2  0  0  0  0  0  0]
     [ 0  4  0  0  0  0  0]
     [ 0  0  5  0  0  0  0]
     [ 0  0  0  6  0  0  0]
     [ 0  0  0  0  8  0  0]
     [ 0  0  0  0  0 10  0]
     [ 0  0  0  0  0  0 12]]
    


### Ranges, Random and Reshaping


```python
# arange rank 1 arrays
ar1 = np.arange(10)
ar2 = np.arange(50,60)
ar3 = np.arange(2,100,10)

print(f'Stop at 10:\n{ar1}\n')
print(f'Start at 50 and stop at 60:\n{ar2}\n')
print(f'Start at 2 and stop at 100 by 10:\n{ar3}\n')
```

    Stop at 10:
    [0 1 2 3 4 5 6 7 8 9]
    
    Start at 50 and stop at 60:
    [50 51 52 53 54 55 56 57 58 59]
    
    Start at 2 and stop at 100 by 10:
    [ 2 12 22 32 42 52 62 72 82 92]
    



```python
lsp1 = np.linspace(0, 20, 15)
lsp2 = np.linspace(0, 20, 15, endpoint=False)

print(f'10 evenly spaced floats from .0-20.:\n{lsp1}\n')
print(f'excluding the endpoint:\n{lsp2}\n')
```

    10 evenly spaced floats from .0-20.:
    [  0.           1.42857143   2.85714286   4.28571429   5.71428571
       7.14285714   8.57142857  10.          11.42857143  12.85714286
      14.28571429  15.71428571  17.14285714  18.57142857  20.        ]
    
    excluding the endpoint:
    [  0.           1.33333333   2.66666667   4.           5.33333333
       6.66666667   8.           9.33333333  10.66666667  12.          13.33333333
      14.66666667  16.          17.33333333  18.66666667]
    



```python
r1 = np.arange(10)
r2 = np.reshape(r1, (2,5))

print(f'reshaped range of 10 to a 2x5:\n{r2}\n')
```

    reshaped range of 10 to a 2x5:
    [[0 1 2 3 4]
     [5 6 7 8 9]]
    



```python
rnd1 = np.random.random((4,4))
rnd2 = np.random.randint(0,100,(5,5))

print(f'random 4x4.:\n{rnd1}\n')
print(f'random interger 5x5 between 0 and 99.:\n{rnd2}\n')
```

    random 4x4.:
    [[ 0.18782149  0.24735819  0.62014626  0.21425457]
     [ 0.99544511  0.50932097  0.25081655  0.87713039]
     [ 0.30737421  0.44161637  0.81432926  0.16024983]
     [ 0.95860737  0.35157861  0.8393971   0.25599258]]
    
    random interger 5x5 between 0 and 99.:
    [[37 65 16 31 40]
     [ 0 15 41 64 97]
     [50 79 58 37 37]
     [34 34 19 21 95]
     [84 35 86 56 37]]
    



```python
# random numbers drawn from probability distributions
rn1 = np.random.normal(2,0.5, size=(10,4))
print(f'random normals with mean of 2\n and standard deviation of .5.:\n{rn1}\n')
print(f'mean: {rn1.mean()}')
print(f' std: {rn1.std()}')
```

    random normals with mean of 2
     and standard deviation of .5.:
    [[ 1.54646756  1.43589436  2.09875212  1.3974066 ]
     [ 1.08325865  2.0021442   1.47672472  2.85984543]
     [ 1.21980609  2.45491494  1.82050565  1.88821092]
     [ 1.94656678  2.0377511   2.29745424  1.84229137]
     [ 1.28723268  2.1499935   3.07733785  1.86075005]
     [ 2.32299782  2.28247921  2.19014796  1.89490517]
     [ 2.19440292  1.97758462  2.64923712  1.93849335]
     [ 2.58946891  1.7157246   2.46026935  1.95457179]
     [ 2.2315923   2.10719654  2.86608878  1.41678298]
     [ 2.04466755  1.00684125  2.36590025  2.88980114]]
    
    mean: 2.0220615601772067
     std: 0.49562922344472393


### Accessing, Deleting, and Inserting


```python
adi1 = np.arange(1,26).reshape(5,5)
print(adi1)
```

    [[ 1  2  3  4  5]
     [ 6  7  8  9 10]
     [11 12 13 14 15]
     [16 17 18 19 20]
     [21 22 23 24 25]]



```python
print(f'row 1, col 2: {adi1[0][1]}')
print(f'row 2, col 3: {adi1[2][2]}')
```

    row 1, col 2: 2
    row 2, col 3: 13



```python
# return matrix without rows 1-2
adi2 = np.delete(adi1, [1,2], axis=0)
print(f'with rows 1-2 removed:\n{adi2}')
```

    with rows 1-2 removed:
    [[ 1  2  3  4  5]
     [16 17 18 19 20]
     [21 22 23 24 25]]



```python
# return matrix without cols 1-2
adi3 = np.delete(adi1, [1,2], axis=1)
print(f'with cols 1-2 removed:\n{adi3}')
```

    with cols 1-2 removed:
    [[ 1  4  5]
     [ 6  9 10]
     [11 14 15]
     [16 19 20]
     [21 24 25]]



```python
# simple append
ap = np.arange(3)
ap = np.append(ap, [3,4])

print(f'append output: {ap}')
```

    append output: [0 1 2 3 4]



```python
print(adi1)
```

    [[ 1  2  3  4  5]
     [ 6  7  8  9 10]
     [11 12 13 14 15]
     [16 17 18 19 20]
     [21 22 23 24 25]]



```python
apnd1 = np.append(adi1, [[0,0,0,0,0]], axis=0)
apnd2 = np.append(adi1, [[0],[0],[0],[0],[0]], axis=1)

print(f'append row:\n{apnd1}\n')
print(f'append column:\n{apnd2}\n')
```

    append row:
    [[ 1  2  3  4  5]
     [ 6  7  8  9 10]
     [11 12 13 14 15]
     [16 17 18 19 20]
     [21 22 23 24 25]
     [ 0  0  0  0  0]]
    
    append column:
    [[ 1  2  3  4  5  0]
     [ 6  7  8  9 10  0]
     [11 12 13 14 15  0]
     [16 17 18 19 20  0]
     [21 22 23 24 25  0]]
    



```python
params = np.array([0,0,0,0])
params2 = np.insert(params, 2, [1,1,1])
print(f'inserting [1,1,1] at index 2:\n{params2}\n')
```

    inserting [1,1,1] at index 2:
    [0 0 1 1 1 0 0]
    



```python
ins = np.full((5,5), 0)
ins2 = np.insert(ins, 3, np.full(5, 4), axis=0)
ins3 = np.insert(ins, 3, np.full(5, 4), axis=1)

print(f'insert a row of 4s at row index 3:\n{ins2}\n')
print(f'insert a column of 4s at column index 3:\n{ins3}\n')
```

    insert a row of 4s at index 3:
    [[0 0 0 0 0]
     [0 0 0 0 0]
     [0 0 0 0 0]
     [4 4 4 4 4]
     [0 0 0 0 0]
     [0 0 0 0 0]]
    
    insert a column of 4s at index 3:
    [[0 0 0 4 0 0]
     [0 0 0 4 0 0]
     [0 0 0 4 0 0]
     [0 0 0 4 0 0]
     [0 0 0 4 0 0]]
    



```python
# stacking 
s1 = np.full((5,5), 0)
s2 = np.full((5,5), 1)
vs = np.vstack((s1, s2))
hs = np.hstack((s1, s2))

print(f'verticle stacking:\n{vs}\n')
print(f'horizontal stacking:\n{hs}\n')
```

    verticle stack:
    [[0 0 0 0 0]
     [0 0 0 0 0]
     [0 0 0 0 0]
     [0 0 0 0 0]
     [0 0 0 0 0]
     [1 1 1 1 1]
     [1 1 1 1 1]
     [1 1 1 1 1]
     [1 1 1 1 1]
     [1 1 1 1 1]]
    
    horizontal stack:
    [[0 0 0 0 0 1 1 1 1 1]
     [0 0 0 0 0 1 1 1 1 1]
     [0 0 0 0 0 1 1 1 1 1]
     [0 0 0 0 0 1 1 1 1 1]
     [0 0 0 0 0 1 1 1 1 1]]
    


### Slicing


```python
slc = np.arange(1, 21).reshape(4,5)
slc1 = slc[1:4, 2:5]
slc2 = slc[:, 1:2]
slc3 = slc[:, [0,3,4]]
cpy  = slc2.copy()

print(f'a 4x5 range:\n{slc}\n')
print(f'a slice from row 1 to 4 and cols 2 to 5:\n{slc1}\n')
print(f'a slice of all rows of column 2:\n{slc2}\n')
print(f'a slice of all rows of colums [0,3,4]:\n{slc3}\n')
print(f'a copy:\n{cpy}\n')
```

    a 4x5 range:
    [[ 1  2  3  4  5]
     [ 6  7  8  9 10]
     [11 12 13 14 15]
     [16 17 18 19 20]]
    
    a slice from row 1 to 4 and cols 2 to 5:
    [[ 8  9 10]
     [13 14 15]
     [18 19 20]]
    
    a slice all rows of column 2:
    [[ 2]
     [ 7]
     [12]
     [17]]
    
    a slice all rows of colums [0,3,4]:
    [[ 1  4  5]
     [ 6  9 10]
     [11 14 15]
     [16 19 20]]
    
    a copy:
    [[ 2]
     [ 7]
     [12]
     [17]]
    


### Boolean Indexing and Sorting


```python
seq = np.arange(25).reshape(5,5)
seq2 = seq|seq < 7
seq3 = seq[(seq > 7) & (seq < 12)]
seq4 = seq[seq % 2 < 1]

print(f'sequence from 0 to 24:\n{seq} \n')
print(f'less than 7:\n{seq2}\n')
print(f'even numbers:\n{seq4}\n')
```

    sequence from 0 to 24:
    [[ 0  1  2  3  4]
     [ 5  6  7  8  9]
     [10 11 12 13 14]
     [15 16 17 18 19]
     [20 21 22 23 24]] 
    
    less than 7:
    [[ True  True  True  True  True]
     [ True  True False False False]
     [False False False False False]
     [False False False False False]
     [False False False False False]]
    
    even numbers:
    [ 0  2  4  6  8 10 12 14 16 18 20 22 24]
    


### Arithmetic and Broadcasting

### Mean normalization
