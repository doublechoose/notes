# keras add tensorboard

```python
# This line creates a Callback Tensorboard object, you should capture that object and give it to the fit function of your model.
keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0,  
          write_graph=True, write_images=True)




tbCallBack = keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)
...
model.fit(...inputs and parameters..., callbacks=[tbCallBack])
```

This way you gave your callback object to the function. It will be ran during the training and will output files that can be used with tensorboard.

If you want to visualize the files created during training, run in your terminal



```
tensorboard --logdir path_to_current_dir/Graph 
```

