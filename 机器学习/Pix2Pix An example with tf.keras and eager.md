# Pix2Pix: An example with tf.keras and eager

origin:[pix2pix](https://github.com/tensorflow/tensorflow/blob/r1.11/tensorflow/contrib/eager/python/examples/pix2pix/pix2pix_eager.ipynb)

image to image translation using conditional GAN's.

useful:

1. colorize black and white photos
2. convert google maps to google earth
3. etc

target:

- convert building facades to real buildings

tool:

- tf.keras
- eager execution

dataset:

- [CMP Facade Database](http://cmp.felk.cvut.cz/~tylecr1/facade/)

each epoch takes 58 seconds on a single P100 GPU

output generated after training the model for 200 epochs.

![sample output_1](https://camo.githubusercontent.com/623ba268ffd0bd96c11e820a3117c229da0a7d49/68747470733a2f2f7777772e74656e736f72666c6f772e6f72672f696d616765732f67616e2f706978327069785f312e706e67)

![sample output_2](https://camo.githubusercontent.com/7ae12e1b410322152c3f902397de2bc88e474a69/68747470733a2f2f7777772e74656e736f72666c6f772e6f72672f696d616765732f67616e2f706978327069785f322e706e67)

knowledge:

### about `tf.stack`

```python
tf.stack(
    values,
    axis=0,
    name='stack'
)
```



Stacks a list of rank-`R` tensors into one rank-`(R+1)` tensor.

Packs the list of tensors in `values` into a tensor with rank one higher than each tensor in `values`, by packing them along the `axis` dimension. Given a list of length `N` of tensors of shape `(A, B, C)`;

if `axis == 0` then the `output` tensor will have the shape `(N, A, B, C)`. if `axis == 1` then the `output` tensor will have the shape `(A, N, B, C)`. Etc.

For example:

```python
x = tf.constant([1, 4])
y = tf.constant([2, 5])
z = tf.constant([3, 6])
tf.stack([x, y, z])  # [[1, 4], [2, 5], [3, 6]] (Pack along first dim.)
tf.stack([x, y, z], axis=1)  # [[1, 2, 3], [4, 5, 6]]
```

This is the opposite of unstack. The numpy equivalent is

```python
tf.stack([x, y, z]) = np.stack([x, y, z])
```

reference : https://www.tensorflow.org/api_docs/python/tf/stack



### tf.image.random_crop

Randomly crops a tensor to a given size.

Slices a shape `size` portion out of `value` at a uniformly chosen offset. Requires `value.shape >= size`.

If a dimension should not be cropped, pass the full size of that dimension. For example, RGB images can be cropped with `size = [crop_height, crop_width, 3]`.

### tf.image.flip_left_right

```python
tf.image.flip_left_right(image)
```

Defined in [`tensorflow/python/ops/image_ops_impl.py`](https://www.tensorflow.org/code/stable/tensorflow/python/ops/image_ops_impl.py).

Flip(弹，轻击) an image horizontally (left to right).

Outputs the contents of `image` flipped along the width dimension.

See also `reverse()`.

### tf.image.resize_images

```python
tf.image.resize_images(
    images,
    size,
    method=ResizeMethod.BILINEAR,
    align_corners=False,
    preserve_aspect_ratio=False
)
```

Defined in [`tensorflow/python/ops/image_ops_impl.py`](https://www.tensorflow.org/code/stable/tensorflow/python/ops/image_ops_impl.py).

Resize `images` to `size` using the specified `method`.

Resized images will be distorted if their original aspect ratio is not the same as `size`. To avoid distortions see [`tf.image.resize_image_with_pad`](https://www.tensorflow.org/api_docs/python/tf/image/resize_image_with_pad).

`method` can be one of:

- **ResizeMethod.BILINEAR**: [Bilinear interpolation.](https://en.wikipedia.org/wiki/Bilinear_interpolation)
- **ResizeMethod.NEAREST_NEIGHBOR**: [Nearest neighbor interpolation.](https://en.wikipedia.org/wiki/Nearest-neighbor_interpolation)
- **ResizeMethod.BICUBIC**: [Bicubic interpolation.](https://en.wikipedia.org/wiki/Bicubic_interpolation)
- **ResizeMethod.AREA**: Area interpolation.

The return value has the same type as `images` if `method` is`ResizeMethod.NEAREST_NEIGHBOR`. It will also have the same type as `images` if the size of `images` can be statically determined to be the same as `size`, because `images` is returned in this case. Otherwise, the return value has type `float32`.

### tf.data.Dataset.list_files(PATH+'train/*.jpg')

A dataset of all files matching a pattern.

NOTE: The default behavior of this method is to return filenames in a non-deterministic random shuffled order. Pass a `seed` or `shuffle=False` to get results in a deterministic order.

Example: If we had the following files on our filesystem: - /path/to/dir/a.txt - /path/to/dir/b.py - /path/to/dir/c.py If we pass "/path/to/dir/*.py" as the directory, the dataset would produce: - /path/to/dir/b.py - /path/to/dir/c.py

