import os
import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf

models_dir = os.path.join(os.getcwd(), 'trained_models')
model_dir = os.path.join(os.getcwd(), 'model/1')
aug_model_dir = os.path.join(os.getcwd(), 'aug_model/1')

# The export path contains the name and the version of the model
tf.keras.backend.set_learning_phase(0)  # Ignore dropout at inference

# compile=False  is you have custom objects in model for ref
# https://stackoverflow.com/questions/61026476/loading-a-model-raise-valueerror-unknown-loss-function
# model = tf.keras.models.load_model('model_best_checkpoint.h5',compile=False)
model = tf.keras.models.load_model('aug_model_best_checkpoint.h5',compile=False)
export_path = aug_model_dir

# Fetch the Keras session and save the model
# The signature definition is defined by the input and output tensors
# And stored with the default serving key
with tf.keras.backend.get_session() as sess:
    tf.saved_model.simple_save(
        sess,
        export_path,
        inputs={'input_image': model.input},
        outputs={t.name: t for t in model.outputs})