from time import time
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.callbacks import TensorBoard
#from keras.utils import multi_gpu_model
from keras.layers import Lambda, concatenate
from keras import Model
import keras.backend as K



def bias(y_true, y_pred):
    return K.mean(y_true - y_pred)

def variance(y_true, y_pred):
    return K.mean((y_true - y_pred)**2)

def train (x_data,y_data, columns, iteraciones, station, contaminant, dirTrain):

    name = 'train_'+station+'_'+contaminant

    x_train = x_data
    y_target = y_data

    model = Sequential()

    model.add(Dense(columns-1, activation = 'sigmoid', input_dim = columns -1, name = 'dense_1'))
    model.add(Dense((columns-1)*2, activation = 'sigmoid', name='dense_2'))
    model.add(Dense(1,activation='sigmoid', name = 'dense_3'))

    model = multi_gpu_model(model, gpus=4)


    model.compile(loss='mean_squared_error', optimizer = 'adam', metrics =['accuracy'])
    #tensorboard = TensorBoard(log_dir="logs/" + station )
    model.fit(x_train, y_target, epochs=150, batch_size=64*4)
    model.save(dirTrain + station + '/' + name + '.h5')
    del model

def multi_gpu_model(model, gpus):
  if isinstance(gpus, (list, tuple)):
    num_gpus = len(gpus)
    target_gpu_ids = gpus
  else:
    num_gpus = gpus
    target_gpu_ids = range(num_gpus)

  def get_slice(data, i, parts):
    shape = tf.shape(data)
    batch_size = shape[:1]
    input_shape = shape[1:]
    step = batch_size // parts
    if i == num_gpus - 1:
      size = batch_size - step * i
    else:
      size = step
    size = tf.concat([size, input_shape], axis=0)
    stride = tf.concat([step, input_shape * 0], axis=0)
    start = stride * i
    return tf.slice(data, start, size)

  all_outputs = []
  for i in range(len(model.outputs)):
    all_outputs.append([])

  # Place a copy of the model on each GPU,
  # each getting a slice of the inputs.
  for i, gpu_id in enumerate(target_gpu_ids):
    with tf.device('/gpu:%d' % gpu_id):
      with tf.name_scope('replica_%d' % gpu_id):
        inputs = []
        # Retrieve a slice of the input.
        for x in model.inputs:
          input_shape = tuple(x.get_shape().as_list())[1:]
          slice_i = Lambda(get_slice,
                           output_shape=input_shape,
                           arguments={'i': i,
                                      'parts': num_gpus})(x)
          inputs.append(slice_i)

        # Apply model on slice
        # (creating a model replica on the target device).
        outputs = model(inputs)
        if not isinstance(outputs, list):
          outputs = [outputs]

        # Save the outputs for merging back together later.
        for o in range(len(outputs)):
          all_outputs[o].append(outputs[o])

  # Merge outputs on CPU.
  with tf.device('/cpu:0'):
    merged = []
    for name, outputs in zip(model.output_names, all_outputs):
      merged.append(concatenate(outputs,
                                axis=0, name=name))
    return Model(model.inputs, merged)