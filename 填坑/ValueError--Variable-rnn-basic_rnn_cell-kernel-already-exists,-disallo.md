# [ValueError: Variable rnn/basic_rnn_cell/kernel already exists, disallowed. Did you mean to set reuse=True or reuse=tf.AUTO_REUSE in VarScope?](https://stackoverflow.com/questions/47296969/valueerror-variable-rnn-basic-rnn-cell-kernel-already-exists-disallowed-did-y)

原因：
  计算图已存在，清理之。

解决办法：
 -  重置图：
```
tf.reset_default_graph()
```
- 重启kernel
