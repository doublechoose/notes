# numpy basic

```python
from numpy import pi
import numpy as np

a= np.array([20,30,40,50])

b = np.arange(4) #array([0,1,2,3])

a = np.ones((2,3),dtype=int) 
-> array([[1, 1, 1],
          [1, 1, 1]])

b = np.random.random((2,3))
 ->array([[0.51534586, 0.58049742, 0.14020628],
       [0.91202226, 0.80372778, 0.53100347]])

 b = np.linspace(0,pi,3)
 ->array([0.        , 1.57079633, 3.14159265])
 
 b.dtype.name
 -> 'float64'
 
 c=array([ 1.        ,  2.57079633,  4.14159265])
 
 d = np.exp(c*1j)
 ->array([ 0.54030231+0.84147098j, -0.84147098+0.54030231j,
       -0.54030231-0.84147098j])
# np.exp(1) = 2.718281828459045 exp(x) = e^x
 
a = np.random.random((2,3))
a.sum()
a.min()
a.max()
 
b = np.arange(12).reshape(3,4)
>>>array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
b.sum(axis=0)
>>>array([12, 15, 18, 21])
b.min(axis=1)
>>>array([0,4,8])

# cumulative sum along each row
>>> b.cumsum(axis=1)                         
array([[ 0,  1,  3,  6],
       [ 4,  9, 15, 22],
       [ 8, 17, 27, 38]])

b = np.arange(3)
#开平方
np.sqrt(b)
array([0.        , 1.        , 1.41421356])

np.add(B,C)

a = np.arange(10)**3
array([  0,   1,   8,  27,  64, 125, 216, 343, 512, 729], dtype=int32)

a[2]
8
a[2:5]
array([ 8, 27, 64])

a[:6:2] = -1000    # equivalent to a[0:6:2] = -1000; from start to position 6, exclusive, set every 2nd element to -1000
a
array([-1000,     1, -1000,    27, -1000,   125,   216,   343,   512,   729])

a[ : :-1]                                 # reversed a
array([  729,   512,   343,   216,   125, -1000,    27, -1000,     1, -1000])

def f(x,y):
    return 10*x+y

b = np.fromfunction(f,(5,4),dtype=int)
array([[ 0,  1,  2,  3],
       [10, 11, 12, 13],
       [20, 21, 22, 23],
       [30, 31, 32, 33],
       [40, 41, 42, 43]])
b[0:5, 1]                       # each row in the second column of b
array([ 1, 11, 21, 31, 41])

b[ : ,1]                        # equivalent to the previous example
array([ 1, 11, 21, 31, 41])

b[1:3, : ]                      # each column in the second and third row of b
array([[10, 11, 12, 13],
       [20, 21, 22, 23]])

b[-1]                                  # the last row. Equivalent to b[-1,:]
array([40, 41, 42, 43])

x[1,2,...] is equivalent to x[1,2,:,:,:],
x[...,3] to x[:,:,:,:,3] and
x[4,...,5,:] to x[4,:,:,5,:].

c = np.array( [[[  0,  1,  2],               # a 3D array (two stacked 2D arrays)
                 [ 10, 12, 13]],
                [[100,101,102],
                 [110,112,113]]])

c.shape
(2,2,3)
c[1,...]                                   # same as c[1,:,:] or c[1]
array([[100, 101, 102],
       [110, 112, 113]])
       
c[...,2]                                   # same as c[:,:,2]
array([[  2,  13],
       [102, 113]])

for row in b:
	print(row)
[0 1 2 3]
[10 11 12 13]
[20 21 22 23]
[30 31 32 33]
[40 41 42 43]

for element in b.flat:
	print(element)
0
1
2
...
41
42
43

a = np.floor(10*np.random.random((3,4)))
array([[ 2.,  8.,  0.,  6.],
       [ 4.,  5.,  1.,  1.],
       [ 8.,  9.,  3.,  6.]])
a.shape
(3,4)

a.ravel()  # returns the array, flattened
array([ 2.,  8.,  0.,  6.,  4.,  5.,  1.,  1.,  8.,  9.,  3.,  6.])

a.reshape(6,2)  # returns the array with a modified shape
array([[ 2.,  8.],
       [ 0.,  6.],
       [ 4.,  5.],
       [ 1.,  1.],
       [ 8.,  9.],
       [ 3.,  6.]])
a.T  # returns the array, transposed
array([[ 2.,  4.,  8.],
       [ 8.,  5.,  9.],
       [ 0.,  1.,  3.],
       [ 6.,  1.,  6.]])

a.T.shape
(4, 3)
a.shape
(3, 4)

a.resize((2,6))
array([[ 2.,  8.,  0.,  6.,  4.,  5.],
       [ 1.,  1.,  8.,  9.,  3.,  6.]])

# 如果给的是-1，会自动计算出来
a.reshape(3,-1)
array([[ 2.,  8.,  0.,  6.],
       [ 4.,  5.,  1.,  1.],
       [ 8.,  9.,  3.,  6.]])



a = array([[ 8.,  8.],
       [ 0.,  0.]])

b = array([[ 1.,  8.],
           [ 0.,  4.]])
np.vstack((a,b))
array([[ 8.,  8.],
       [ 0.,  0.],
       [ 1.,  8.],
       [ 0.,  4.]])
np.hstack((a,b))
array([[ 8.,  8.,  1.,  8.],
       [ 0.,  0.,  0.,  4.]])

np.column_stack((a,b))     # with 2D arrays
array([[ 8.,  8.,  1.,  8.],
       [ 0.,  0.,  0.,  4.]])

a = np.array([4.,2.])
b = np.array([3.,8.])
np.column_stack((a,b))     # returns a 2D array
array([[ 4., 3.],
       [ 2., 8.]])
np.hstack((a,b))           # the result is different
array([ 4., 2., 3., 8.])

from numpy import newaxis
a[:,newaxis]               # this allows to have a 2D columns vector
array([[ 4.],
       [ 2.]])
np.column_stack((a[:,newaxis],b[:,newaxis]))
array([[ 4.,  3.],
       [ 2.,  8.]])

np.hstack((a[:,newaxis],b[:,newaxis]))   # the result is the same
array([[ 4.,  3.],
       [ 2.,  8.]])

np.r_[1:4,0,4]
array([1, 2, 3, 0, 4])

# Splitting one array into several smaller ones
a = array([[ 9.,  5.,  6.,  3.,  6.,  8.,  0.,  7.,  9.,  7.,  2.,  7.],
       [ 1.,  4.,  9.,  2.,  2.,  1.,  0.,  6.,  2.,  2.,  4.,  0.]])
np.hsplit(a,3)   # Split a into 3
[array([[ 9.,  5.,  6.,  3.],
       [ 1.,  4.,  9.,  2.]]), array([[ 6.,  8.,  0.,  7.],
       [ 2.,  1.,  0.,  6.]]), array([[ 9.,  7.,  2.,  7.],
       [ 2.,  2.,  4.,  0.]])]

np.hsplit(a,(3,4))   # Split a after the third and the fourth column
[array([[ 9.,  5.,  6.],
       [ 1.,  4.,  9.]]), array([[ 3.],
       [ 2.]]), array([[ 6.,  8.,  0.,  7.,  9.,  7.,  2.,  7.],
       [ 2.,  1.,  0.,  6.,  2.,  2.,  4.,  0.]])]

# Copies and views
a = np.arange(12)
b = a            # no new object is created
b is a           # a and b are two names for the same ndarray object
True
b.shape = 3,4    # changes the shape of a
a.shape
(3, 4)

# View or Shallow Copy
# The view method creates a new array object
# that looks at the same data.
c = a.view()
c is a
False
c.base is a                        # c is a view of the data owned by a
True
c.flags.owndata
False
c.shape = 2,6                      # a's shape doesn't change
a.shape
(3, 4)
c[0,4] = 1234                      # a's data changes
a
array([[   0,    1,    2,    3],
       [1234,    5,    6,    7],
       [   8,    9,   10,   11]])

# spaces added for clarity; could also be written "s = a[:,1:3]"
s = a[ : , 1:3]     
# s[:] is a view of s. Note the difference between s=10 and s[:]=10
s[:] = 10           
a
array([[   0,   10,   10,    3],
       [1234,   10,   10,    7],
       [   8,   10,   10,   11]])

# deep copy
d = a.copy()                          # a new array object with new data is created
d is a
False
d.base is a                           # d doesn't share anything with a
False
d[0,0] = 9999
a
array([[   0,   10,   10,    3],
       [1234,   10,   10,    7],
       [   8,   10,   10,   11]])

```

### Functions and Methods Overview

Here is a list of some useful NumPy functions and methods names ordered in categories. See [Routines](https://docs.scipy.org/doc/numpy/reference/routines.html#routines) for the full list.

- Array Creation

  [`arange`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html#numpy.arange), [`array`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html#numpy.array), [`copy`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.copy.html#numpy.copy), [`empty`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.empty.html#numpy.empty), [`empty_like`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.empty_like.html#numpy.empty_like), [`eye`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.eye.html#numpy.eye), [`fromfile`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.fromfile.html#numpy.fromfile), [`fromfunction`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.fromfunction.html#numpy.fromfunction), [`identity`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.identity.html#numpy.identity), [`linspace`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.linspace.html#numpy.linspace),[`logspace`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.logspace.html#numpy.logspace), [`mgrid`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.mgrid.html#numpy.mgrid), [`ogrid`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ogrid.html#numpy.ogrid), [`ones`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ones.html#numpy.ones), [`ones_like`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ones_like.html#numpy.ones_like), *r*, [`zeros`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.zeros.html#numpy.zeros), [`zeros_like`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.zeros_like.html#numpy.zeros_like)

- Conversions

  [`ndarray.astype`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy.ndarray.astype), [`atleast_1d`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.atleast_1d.html#numpy.atleast_1d), [`atleast_2d`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.atleast_2d.html#numpy.atleast_2d), [`atleast_3d`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.atleast_3d.html#numpy.atleast_3d), [`mat`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.mat.html#numpy.mat)

- Manipulations

  [`array_split`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.array_split.html#numpy.array_split), [`column_stack`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.column_stack.html#numpy.column_stack), [`concatenate`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.concatenate.html#numpy.concatenate), [`diagonal`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.diagonal.html#numpy.diagonal), [`dsplit`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.dsplit.html#numpy.dsplit), [`dstack`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.dstack.html#numpy.dstack), [`hsplit`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.hsplit.html#numpy.hsplit), [`hstack`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.hstack.html#numpy.hstack),[`ndarray.item`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.item.html#numpy.ndarray.item), [`newaxis`](https://docs.scipy.org/doc/numpy/reference/constants.html#numpy.newaxis), [`ravel`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ravel.html#numpy.ravel), [`repeat`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.repeat.html#numpy.repeat), [`reshape`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html#numpy.reshape), [`resize`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.resize.html#numpy.resize), [`squeeze`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.squeeze.html#numpy.squeeze), [`swapaxes`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.swapaxes.html#numpy.swapaxes), [`take`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.take.html#numpy.take),[`transpose`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.transpose.html#numpy.transpose), [`vsplit`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.vsplit.html#numpy.vsplit), [`vstack`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.vstack.html#numpy.vstack)

- Questions

  [`all`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.all.html#numpy.all), [`any`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.any.html#numpy.any), [`nonzero`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.nonzero.html#numpy.nonzero), [`where`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html#numpy.where)

- Ordering

  [`argmax`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.argmax.html#numpy.argmax), [`argmin`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.argmin.html#numpy.argmin), [`argsort`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.argsort.html#numpy.argsort), [`max`](https://docs.python.org/dev/library/functions.html#max), [`min`](https://docs.python.org/dev/library/functions.html#min), [`ptp`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ptp.html#numpy.ptp), [`searchsorted`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.searchsorted.html#numpy.searchsorted), [`sort`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.sort.html#numpy.sort)

- Operations

  [`choose`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.choose.html#numpy.choose), [`compress`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.compress.html#numpy.compress), [`cumprod`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.cumprod.html#numpy.cumprod), [`cumsum`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.cumsum.html#numpy.cumsum), [`inner`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.inner.html#numpy.inner), [`ndarray.fill`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.fill.html#numpy.ndarray.fill), [`imag`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.imag.html#numpy.imag), [`prod`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.prod.html#numpy.prod), [`put`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.put.html#numpy.put), [`putmask`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.putmask.html#numpy.putmask),[`real`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.real.html#numpy.real), [`sum`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html#numpy.sum)

- Basic Statistics

  [`cov`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.cov.html#numpy.cov), [`mean`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html#numpy.mean), [`std`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html#numpy.std), [`var`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.var.html#numpy.var)

- Basic Linear Algebra

  [`cross`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.cross.html#numpy.cross), [`dot`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.dot.html#numpy.dot), [`outer`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.outer.html#numpy.outer), [`linalg.svd`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.svd.html#numpy.linalg.svd), [`vdot`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.vdot.html#numpy.vdot)



待看。。。

## Less Basic

Broadcasting allows universal functions to deal in a meaningful way with inputs that do not have exactly the same shape.

The first rule of broadcasting is that if all input arrays do not have the same number of dimensions, a “1” will be repeatedly prepended to the shapes of the smaller arrays until all the arrays have the same number of dimensions.

The second rule of broadcasting ensures that arrays with a size of 1 along a particular dimension act as if they had the size of the array with the largest shape along that dimension. The value of the array element is assumed to be the same along that dimension for the “broadcast” array.

## Fancy indexing and index tricks

```python
索引的索引
>>> a = np.arange(12)**2                       # the first 12 square numbers
>>> i = np.array( [ 1,1,3,8,5 ] )              # an array of indices
>>> a[i]                                       # the elements of a at the positions i
array([ 1,  1,  9, 64, 25])
>>>
>>> j = np.array( [ [ 3, 4], [ 9, 7 ] ] )      # a bidimensional array of indices
>>> a[j]                                       # the same shape as j
array([[ 9, 16],
       [81, 49]])


>>> palette = np.array( [ [0,0,0],                # black
...                       [255,0,0],              # red
...                       [0,255,0],              # green
...                       [0,0,255],              # blue
...                       [255,255,255] ] )       # white
>>> image = np.array( [ [ 0, 1, 2, 0 ],           # each value corresponds to a color in the palette
...                     [ 0, 3, 4, 0 ]  ] )
>>> palette[image]                            # the (2,4,3) color image
array([[[  0,   0,   0],
        [255,   0,   0],
        [  0, 255,   0],
        [  0,   0,   0]],
       [[  0,   0,   0],
        [  0,   0, 255],
        [255, 255, 255],
        [  0,   0,   0]]])


>>> a = np.arange(12).reshape(3,4)
>>> a
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
>>> i = np.array( [ [0,1],                        # indices for the first dim of a
...                 [1,2] ] )
>>> j = np.array( [ [2,1],                        # indices for the second dim
...                 [3,3] ] )
>>>
>>> a[i,j]                                     # i and j must have equal shape
array([[ 2,  5],
       [ 7, 11]])
>>>
>>> a[i,2]
array([[ 2,  6],
       [ 6, 10]])
>>>
>>> a[:,j]                                     # i.e., a[ : , j]
array([[[ 2,  1],
        [ 3,  3]],
       [[ 6,  5],
        [ 7,  7]],
       [[10,  9],
        [11, 11]]])

>>> l = [i,j]
>>> a[l]                                       # equivalent to a[i,j]
array([[ 2,  5],
       [ 7, 11]])

#However, we can not do this by putting i and j into an array, because this array will be interpreted as indexing the first dimension of a.
>>> s = np.array( [i,j] )
>>> a[s]                                       # not what we want
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
IndexError: index (3) out of range (0<=index<=2) in dimension 0
>>>
>>> a[tuple(s)]                                # same as a[i,j]
array([[ 2,  5],
       [ 7, 11]])


>>> time = np.linspace(20, 145, 5)                 # time scale
>>> data = np.sin(np.arange(20)).reshape(5,4)      # 4 time-dependent series
>>> time
array([  20.  ,   51.25,   82.5 ,  113.75,  145.  ])
>>> data
array([[ 0.        ,  0.84147098,  0.90929743,  0.14112001],
       [-0.7568025 , -0.95892427, -0.2794155 ,  0.6569866 ],
       [ 0.98935825,  0.41211849, -0.54402111, -0.99999021],
       [-0.53657292,  0.42016704,  0.99060736,  0.65028784],
       [-0.28790332, -0.96139749, -0.75098725,  0.14987721]])
>>>
>>> ind = data.argmax(axis=0)                  # index of the maxima for each series
>>> ind
array([2, 0, 3, 1])
>>>
>>> time_max = time[ind]                       # times corresponding to the maxima
>>>
>>> data_max = data[ind, range(data.shape[1])] # => data[ind[0],0], data[ind[1],1]...
>>>
>>> time_max
array([  82.5 ,   20.  ,  113.75,   51.25])
>>> data_max
array([ 0.98935825,  0.84147098,  0.99060736,  0.6569866 ])
>>>
>>> np.all(data_max == data.max(axis=0))
True

>>> a = np.arange(5)
>>> a
array([0, 1, 2, 3, 4])
>>> a[[1,3,4]] = 0
>>> a
array([0, 0, 2, 0, 0])

>>> a = np.arange(5)
>>> a[[0,0,2]]=[1,2,3]
>>> a
array([2, 1, 3, 3, 4])
```





### Indexing with Boolean Arrays

When we index arrays with arrays of (integer) indices we are providing the list of indices to pick. With boolean indices the approach is different; we explicitly choose which items in the array we want and which ones we don’t.

The most natural way one can think of for boolean indexing is to use boolean arrays that have *the same shape* as the original array:

\>>>

```
>>> a = np.arange(12).reshape(3,4)
>>> b = a > 4
>>> b                                          # b is a boolean with a's shape
array([[False, False, False, False],
       [False,  True,  True,  True],
       [ True,  True,  True,  True]])
>>> a[b]                                       # 1d array with the selected elements
array([ 5,  6,  7,  8,  9, 10, 11])
```

This property can be very useful in assignments:

\>>>

```
>>> a[b] = 0                                   # All elements of 'a' higher than 4 become 0
>>> a
array([[0, 1, 2, 3],
       [4, 0, 0, 0],
       [0, 0, 0, 0]])
```

You can look at the following example to see how to use boolean indexing to generate an image of the [Mandelbrot set](http://en.wikipedia.org/wiki/Mandelbrot_set):

\>>>

```
>>> import numpy as np
>>> import matplotlib.pyplot as plt
>>> def mandelbrot( h,w, maxit=20 ):
...     """Returns an image of the Mandelbrot fractal of size (h,w)."""
...     y,x = np.ogrid[ -1.4:1.4:h*1j, -2:0.8:w*1j ]
...     c = x+y*1j
...     z = c
...     divtime = maxit + np.zeros(z.shape, dtype=int)
...
...     for i in range(maxit):
...         z = z**2 + c
...         diverge = z*np.conj(z) > 2**2            # who is diverging
...         div_now = diverge & (divtime==maxit)  # who is diverging now
...         divtime[div_now] = i                  # note when
...         z[diverge] = 2                        # avoid diverging too much
...
...     return divtime
>>> plt.imshow(mandelbrot(400,400))
>>> plt.show()
```

![../_images/quickstart-1.png](https://docs.scipy.org/doc/numpy/_images/quickstart-1.png)

The second way of indexing with booleans is more similar to integer indexing; for each dimension of the array we give a 1D boolean array selecting the slices we want:

\>>>

```
>>> a = np.arange(12).reshape(3,4)
>>> b1 = np.array([False,True,True])             # first dim selection
>>> b2 = np.array([True,False,True,False])       # second dim selection
>>>
>>> a[b1,:]                                   # selecting rows
array([[ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
>>>
>>> a[b1]                                     # same thing
array([[ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
>>>
>>> a[:,b2]                                   # selecting columns
array([[ 0,  2],
       [ 4,  6],
       [ 8, 10]])
>>>
>>> a[b1,b2]                                  # a weird thing to do
array([ 4, 10])
```

Note that the length of the 1D boolean array must coincide with the length of the dimension (or axis) you want to slice. In the previous example, `b1` has length 3 (the number of *rows* in `a`), and `b2` (of length 4) is suitable to index the 2nd axis (columns) of `a`.

### The ix_() function

The [`ix_`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ix_.html#numpy.ix_) function can be used to combine different vectors so as to obtain the result for each n-uplet. For example, if you want to compute all the a+b*c for all the triplets taken from each of the vectors a, b and c:

\>>>

```
>>> a = np.array([2,3,4,5])
>>> b = np.array([8,5,4])
>>> c = np.array([5,4,6,8,3])
>>> ax,bx,cx = np.ix_(a,b,c)
>>> ax
array([[[2]],
       [[3]],
       [[4]],
       [[5]]])
>>> bx
array([[[8],
        [5],
        [4]]])
>>> cx
array([[[5, 4, 6, 8, 3]]])
>>> ax.shape, bx.shape, cx.shape
((4, 1, 1), (1, 3, 1), (1, 1, 5))
>>> result = ax+bx*cx
>>> result
array([[[42, 34, 50, 66, 26],
        [27, 22, 32, 42, 17],
        [22, 18, 26, 34, 14]],
       [[43, 35, 51, 67, 27],
        [28, 23, 33, 43, 18],
        [23, 19, 27, 35, 15]],
       [[44, 36, 52, 68, 28],
        [29, 24, 34, 44, 19],
        [24, 20, 28, 36, 16]],
       [[45, 37, 53, 69, 29],
        [30, 25, 35, 45, 20],
        [25, 21, 29, 37, 17]]])
>>> result[3,2,4]
17
>>> a[3]+b[2]*c[4]
17
```

You could also implement the reduce as follows:

\>>>

```
>>> def ufunc_reduce(ufct, *vectors):
...    vs = np.ix_(*vectors)
...    r = ufct.identity
...    for v in vs:
...        r = ufct(r,v)
...    return r
```

and then use it as:

\>>>

```
>>> ufunc_reduce(np.add,a,b,c)
array([[[15, 14, 16, 18, 13],
        [12, 11, 13, 15, 10],
        [11, 10, 12, 14,  9]],
       [[16, 15, 17, 19, 14],
        [13, 12, 14, 16, 11],
        [12, 11, 13, 15, 10]],
       [[17, 16, 18, 20, 15],
        [14, 13, 15, 17, 12],
        [13, 12, 14, 16, 11]],
       [[18, 17, 19, 21, 16],
        [15, 14, 16, 18, 13],
        [14, 13, 15, 17, 12]]])
```

The advantage of this version of reduce compared to the normal ufunc.reduce is that it makes use of the [Broadcasting Rules](https://docs.scipy.org/doc/numpy/user/Tentative_NumPy_Tutorial.html#head-c43f3f81719d84f09ae2b33a22eaf50b26333db8) in order to avoid creating an argument array the size of the output times the number of vectors.

### Indexing with strings

See [Structured arrays](https://docs.scipy.org/doc/numpy/user/basics.rec.html#structured-arrays).

## Linear Algebra

Work in progress. Basic linear algebra to be included here.

### Simple Array Operations

See linalg.py in numpy folder for more.

\>>>

```
>>> import numpy as np
>>> a = np.array([[1.0, 2.0], [3.0, 4.0]])
>>> print(a)
[[ 1.  2.]
 [ 3.  4.]]

>>> a.transpose()
array([[ 1.,  3.],
       [ 2.,  4.]])

>>> np.linalg.inv(a)
array([[-2. ,  1. ],
       [ 1.5, -0.5]])

>>> u = np.eye(2) # unit 2x2 matrix; "eye" represents "I"
>>> u
array([[ 1.,  0.],
       [ 0.,  1.]])
>>> j = np.array([[0.0, -1.0], [1.0, 0.0]])

>>> j @ j        # matrix product
array([[-1.,  0.],
       [ 0., -1.]])

>>> np.trace(u)  # trace
2.0

>>> y = np.array([[5.], [7.]])
>>> np.linalg.solve(a, y)
array([[-3.],
       [ 4.]])

>>> np.linalg.eig(j)
(array([ 0.+1.j,  0.-1.j]), array([[ 0.70710678+0.j        ,  0.70710678-0.j        ],
       [ 0.00000000-0.70710678j,  0.00000000+0.70710678j]]))
Parameters:
    square matrix
Returns
    The eigenvalues, each repeated according to its multiplicity.
    The normalized (unit "length") eigenvectors, such that the
    column ``v[:,i]`` is the eigenvector corresponding to the
    eigenvalue ``w[i]`` .
```

## Tricks and Tips

Here we give a list of short and useful tips.

### “Automatic” Reshaping

To change the dimensions of an array, you can omit one of the sizes which will then be deduced automatically:

\>>>

```
>>> a = np.arange(30)
>>> a.shape = 2,-1,3  # -1 means "whatever is needed"
>>> a.shape
(2, 5, 3)
>>> a
array([[[ 0,  1,  2],
        [ 3,  4,  5],
        [ 6,  7,  8],
        [ 9, 10, 11],
        [12, 13, 14]],
       [[15, 16, 17],
        [18, 19, 20],
        [21, 22, 23],
        [24, 25, 26],
        [27, 28, 29]]])
```

### Vector Stacking

How do we construct a 2D array from a list of equally-sized row vectors? In MATLAB this is quite easy: if `x` and `y` are two vectors of the same length you only need do `m=[x;y]`. In NumPy this works via the functions `column_stack`, `dstack`, `hstack` and `vstack`, depending on the dimension in which the stacking is to be done. For example:

```
x = np.arange(0,10,2)                     # x=([0,2,4,6,8])
y = np.arange(5)                          # y=([0,1,2,3,4])
m = np.vstack([x,y])                      # m=([[0,2,4,6,8],
                                          #     [0,1,2,3,4]])
xy = np.hstack([x,y])                     # xy =([0,2,4,6,8,0,1,2,3,4])
```

The logic behind those functions in more than two dimensions can be strange.

See also

[NumPy for Matlab users](https://docs.scipy.org/doc/numpy/user/numpy-for-matlab-users.html)

### Histograms

The NumPy `histogram` function applied to an array returns a pair of vectors: the histogram of the array and the vector of bins. Beware: `matplotlib` also has a function to build histograms (called `hist`, as in Matlab) that differs from the one in NumPy. The main difference is that `pylab.hist` plots the histogram automatically, while `numpy.histogram` only generates the data.

\>>>

```
>>> import numpy as np
>>> import matplotlib.pyplot as plt
>>> # Build a vector of 10000 normal deviates with variance 0.5^2 and mean 2
>>> mu, sigma = 2, 0.5
>>> v = np.random.normal(mu,sigma,10000)
>>> # Plot a normalized histogram with 50 bins
>>> plt.hist(v, bins=50, density=1)       # matplotlib version (plot)
>>> plt.show()
```

![../_images/quickstart-2_00_00.png](https://docs.scipy.org/doc/numpy/_images/quickstart-2_00_00.png)

\>>>

```
>>> # Compute the histogram with numpy and then plot it
>>> (n, bins) = np.histogram(v, bins=50, density=True)  # NumPy version (no plot)
>>> plt.plot(.5*(bins[1:]+bins[:-1]), n)
>>> plt.show()
```

![../_images/quickstart-2_01_00.png](https://docs.scipy.org/doc/numpy/_images/quickstart-2_01_00.png)