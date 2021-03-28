import numpy as np
from oap.deep.models import f1
from oap.__conf__ import COLUMN, ROSETTE
from tensorflow.keras.models import load_model
from pkg_resources import resource_filename


class ParticleClassifier:

    def __init__(self, p_type):
        if p_type == COLUMN:
            filename = resource_filename("oap.deep", "models/final_column_mc_pre14_e11_acc0.98_fs0.98.hdf5")
        elif p_type == ROSETTE:
            filename = resource_filename("oap.deep", "models/final_rosette_mc_pre06_e05_acc0.97_fs0.97.hdf5")
        else:
            raise Exception
        self.model = load_model(filename, custom_objects={'f1': f1})

        # ToDo: this is very messy, delete as soon as possible!
        # This is necessary for now, because the tensorflow log
        # (which unfortunately can't be switched off at the moment)
        # will otherwise destroy the layout of the console output...
        self.model.predict(np.zeros(shape=(1, 64, 64, 1)))

    def predict(self, batch):
        prediction = self.model.predict(batch)
        return prediction
