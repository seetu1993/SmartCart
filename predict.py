from keras_preprocessing import image
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.backend import set_session
import numpy as np


config = tf.compat.v1.ConfigProto()
first_graph = tf.Graph()
# first_session = tf.compat.v1.Session(config=config)

# tf_config = some_custom_config
# sess = tf.Session(config=tf_config)
fruitsAndVegitalbes = ['Apple', 'Banana','Kiwi',   'Lemon',   'Mango',  'Onion',  'Pepper Green',  'Tomato',   'Watermelon']



def predictfruit(path, model):
    img = image.load_img(path, target_size = (25, 25))
    array = image.img_to_array(img)
    x = np.expand_dims(array, axis=0)
    vimage = np.vstack([x])
    with first_graph.as_default():
        if model is None:
            model = tf.keras.models.load_model("saved_model/fruit_classifier")
        predictions = model.predict(vimage)
        return (fruitsAndVegitalbes[np.argmax(predictions)], model)
