# tf.keras & 风格迁移

[reference](https://github.com/tensorflow/models/blob/master/research/nst_blogpost/4_Neural_Style_Transfer_with_Eager_Execution.ipynb)

1. Visualize data
2. Basic Preprocessing/preparing our data
3. Set up loss functions
4. Create model
5. Optimize for loss function

To get the most out of this post, you should:

- Read [Gatys' paper](https://arxiv.org/abs/1508.06576) - we'll explain along the way, but the paper will provide a more thorough understanding of the task
- [Understand reducing loss with gradient descent](https://developers.google.com/machine-learning/crash-course/reducing-loss/gradient-descent)



```
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (10,10)
mpl.rcParams['axes.grid'] = False
```

### numpy.expand_dims

https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.expand_dims.html

Expand the shape of an array.

Insert a new axis, corresponding to a given position in the array shape.

Examples

\>>>

```
>>> x = np.array([1,2])
>>> x.shape
(2,)
```

The following is equivalent to `x[np.newaxis,:]` or `x[np.newaxis]`:

\>>>

```
>>> y = np.expand_dims(x, axis=0)
>>> y
array([[1, 2]])
>>> y.shape
(1, 2)
```

\>>>

```
>>> y = np.expand_dims(x, axis=1)  # Equivalent to x[:,newaxis]
>>> y
array([[1],
       [2]])
>>> y.shape
(2, 1)
```

Note that some examples may use `None` instead of `np.newaxis`. These are the same objects:

\>>>

```
>>> np.newaxis is None
True
```

### np.squeeze(img,axis=0)

Remove single-dimensional entries from the shape of an array.

Examples

```
>>> x = np.array([[[0], [1], [2]]])
>>> x.shape
(1, 3, 1)
>>> np.squeeze(x).shape
(3,)
>>> np.squeeze(x, axis=0).shape
(3, 1)
>>> np.squeeze(x, axis=1).shape
Traceback (most recent call last):
...
ValueError: cannot select an axis to squeeze out which has size not equal to one
>>> np.squeeze(x, axis=2).shape
(1, 3)
```

