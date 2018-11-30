# keras——ValueError: You are trying to load a weight file containing 12 layers into a model with 2 layers.


> > \>> model.save('./model/my_model_weights.h5')  
>
> \>> model=load_model('./model/my_model_weights.h5')  
>
> ValueError: You are trying to load a weight file containing 12 layers into a model with 2 layers.

因为这个神经网络是嵌套的，也算是这个python库的一个bug吧。

> from keras.models import model_from_json
>
> \>> model.save_weights('test.h5')  
>
> \>> model.load_weights('test.h5',by_name=True) 
>
> \>> json_string = model.to_json()  
>
> \>> model = model_from_json(json_string)  

