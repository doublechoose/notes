# Eager Execution

可用的Tensorflow API很多，但是建议从以下高级Tensorflow概念开始：

- 启用 [Eager Execution](https://www.tensorflow.org/programmers_guide/eager) 开发环境，
- 使用 [Datasets API](https://www.tensorflow.org/programmers_guide/datasets) 导入数据，
- 使用 TensorFlow 的 [Keras API](https://keras.io/getting-started/sequential-model-guide/) 构建模型和层。

本教程介绍了这些 API，并采用了与许多其他 TensorFlow 程序相似的结构：

1. 导入和解析数据集。
2. 选择模型类型。
3. 训练模型。
4. 评估模型的效果。
5. 使用经过训练的模型进行预测。



| 样本特征 | 标签 | 模型预测 |      |      |      |
| -------- | ---- | -------- | ---- | ---- | ---- |
| 5.9      | 3.0  | 4.3      | 1.5  | 1    | 1    |
| 6.9      | 3.1  | 5.4      | 2.1  | 2    | 2    |
| 5.1      | 3.3  | 1.7      | 0.5  | 0    | 0    |
| 6.0      | 3.4  | 4.5      | 1.6  | 1    | 2    |
| 5.5      | 2.5  | 4.0      | 1.3  | 1    | 1    |