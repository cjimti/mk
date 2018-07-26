---
published: false
layout: post
title: Essential PyTorch
tags: coding python
featured: coding python
mast: torch
---

The Facebook AI Research team released [PyTorch], "a deep learning framework for fast, flexible experimentation." as an open source project in early 2017. [PyTorch] has gained rapid adoption by the deep learning community for building neural networks in Python, and working seamlessly with [numpy], [PyTorch] could even be used as a [numpy] replacement.


### Install

Install using [Anaconda]:

```bash
conda install pytorch torchvision -c pytorch
```

### Tensors

[PyTorch] allows you to build neural networks using tensors. Tensors in [PyTorch] are easily converted to and from nsarrays in [numpy]. So, if you have worked with [numpy] you have worked with [PyTorch] tensors.



[PyTorch]: https://pytorch.org/
[numpy]: https://mk.imti.co/python-data-essentials-numpy/
[tensor]: https://en.wikipedia.org/wiki/Tensor
[Anaconda]: https://conda.io/docs/user-guide/install/download.html


```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

%matplotlib inline

# http://pytorch.org/
!pip3 install torch torchvision
import torch

a = [[1,2], [3,4]]
print(a)

np.array(a)
```

    Collecting torch
    [?25l  Downloading https://files.pythonhosted.org/packages/69/43/380514bd9663f1bf708abeb359b8b48d3fabb1c8e95bb3427a980a064c57/torch-0.4.0-cp36-cp36m-manylinux1_x86_64.whl (484.0MB)
    [K    100% |████████████████████████████████| 484.0MB 28kB/s 
    tcmalloc: large alloc 1073750016 bytes == 0x5c760000 @  0x7f043cbec1c4 0x46d6a4 0x5fcbcc 0x4c494d 0x54f3c4 0x553aaf 0x54e4c8 0x54f4f6 0x553aaf 0x54efc1 0x54f24d 0x553aaf 0x54efc1 0x54f24d 0x553aaf 0x54efc1 0x54f24d 0x551ee0 0x54e4c8 0x54f4f6 0x553aaf 0x54efc1 0x54f24d 0x551ee0 0x54efc1 0x54f24d 0x551ee0 0x54e4c8 0x54f4f6 0x553aaf 0x54e4c8
    [?25hCollecting torchvision
    [?25l  Downloading https://files.pythonhosted.org/packages/ca/0d/f00b2885711e08bd71242ebe7b96561e6f6d01fdb4b9dcf4d37e2e13c5e1/torchvision-0.2.1-py2.py3-none-any.whl (54kB)
    [K    100% |████████████████████████████████| 61kB 9.4MB/s 
    [?25hRequirement already satisfied: six in /usr/local/lib/python3.6/dist-packages (from torchvision) (1.11.0)
    Requirement already satisfied: numpy in /usr/local/lib/python3.6/dist-packages (from torchvision) (1.14.5)
    Collecting pillow>=4.1.1 (from torchvision)
    [?25l  Downloading https://files.pythonhosted.org/packages/d1/24/f53ff6b61b3d728b90934bddb4f03f8ab584a7f49299bf3bde56e2952612/Pillow-5.2.0-cp36-cp36m-manylinux1_x86_64.whl (2.0MB)
    [K    100% |████████████████████████████████| 2.0MB 1.9MB/s 
    [?25hInstalling collected packages: torch, pillow, torchvision
      Found existing installation: Pillow 4.0.0
        Uninstalling Pillow-4.0.0:
          Successfully uninstalled Pillow-4.0.0
    Successfully installed pillow-5.2.0 torch-0.4.0 torchvision-0.2.1
    [[1, 2], [3, 4]]





    array([[1, 2],
           [3, 4]])




```python
torch.Tensor(a)
```




    tensor([[ 1.,  2.],
            [ 3.,  4.]])




```python
tensor_cpu = torch.ones(2,2)

# move to GPU if available (CPU is default)
if torch.cuda.is_available():
  print("GPU is available.")
  tensor_cpu.cuda()
    
tensor_cpu.cuda()
```

    GPU is available.





    tensor([[ 1.,  1.],
            [ 1.,  1.]], device='cuda:0')


