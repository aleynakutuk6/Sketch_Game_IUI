import tensorflow as tf

from Sketchformer.utils import *
import Sketchformer.models as models
import Sketchformer.dataloaders as dataloaders
import numpy as np
from rdp import rdp

tokenizer = tokenizer.Tokenizer("Sketchformer/prep_data/sketch_token/token_dict.pkl")

def get_classes():
    classes = []
    with open("Sketchformer/prep_data/quickdraw/list_quickdraw.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        classes.append(line.replace("\n",""))
    return classes

obj_classes = get_classes()

def get_model():

    Model = models.get_model_by_name("sketch-transformer-tf2")
    DataLoader = dataloaders.get_dataloader_by_name('stroke3-distributed')
    hps = hparams.combine_hparams_into_one(Model.default_hparams(),
                                                 DataLoader.default_hparams())

    hparams.load_config(hps, Model.get_config_filepath("Sketchformer/weights/", "cvpr_tform_tok_dict"))
    # utils.gpu.setup_gpu(0)
    dataset = DataLoader(hps, "Sketchformer/dataset/")
    model = Model(hps, dataset, "Sketchformer/weights/", "cvpr_tform_tok_dict")
    model.restore_checkpoint_if_exists("latest")

    return model

def _strokes_to_lines_alternative(strokes, scale=1.0, start_from_origin=False):
    """
    convert strokes3 to polyline format ie. relative x-y coordinates
    note: the sketch can be negative
    :param strokes: stroke3, Nx3
    :param scale: scale factor applied on stroke3
    :param start_from_origin: sketch starts from [0,0] if True
    :return: list of strokes, each stroke has format Nx2
    """
    x = 0
    y = 0
    lines = []
    line = [[0, 0]] if start_from_origin else []
    for i in range(len(strokes)):
        x_, y_ = strokes[i, :2] * scale
        line.append([x_, y_])
        if strokes[i, 2] == 1:
            line_array = np.array(line) + np.zeros((1, 2), dtype=np.uint8)
            lines.append(line_array)
            line = []
    if lines == []:
        line_array = np.array(line) + np.zeros((1, 2), dtype=np.uint8)
        lines.append(line_array)
    return lines

def apply_RDP(data):
    """
    author: Aleyna Kutuk
    applies RDP algorithm to the sketch which is given in stroke-3 format
    for each stroke in the sketch, - convert to its absolute x,y
                                   - apply rdp
                                   - convert back to its relative dx,dy
                                   - add p - lift to every dx,dy coordinates
                                   - loop over every stroke of sketch

    """

    try:
        data = np.asarray(data, dtype=float)

        # get bounds of sketch
        min_x, max_x, min_y, max_y = sketch.get_absolute_bounds(data)
        max_dim = max([max_x - min_x, max_y - min_y, 1])

        # set to top-left
        for i in range(1, data.shape[0]):
            data[i, 0] -= data[0, 0]
            data[i, 1] -= data[0, 1]
        data[0, 0] = 0.0
        data[0, 1] = 0.0

        data[:, :2] /= max_dim
        data[:, :2] *= 255.0

        # back to relative coords
        data = sketch.to_relative(data)
        los = _strokes_to_lines_alternative(data)
        simplified_sketch = []

        for stroke in los:
            stroke = sketch.convert_to_absolute(stroke)
            simplified_stroke = rdp(stroke, epsilon=2.0)
            rel_stroke = sketch.to_relative(simplified_stroke)
            zero_arr = np.zeros((len(rel_stroke), 1))
            arr_stroke = np.concatenate([rel_stroke, zero_arr], axis=1)
            arr_stroke[-1, -1] = 1
            simplified_sketch.extend(arr_stroke)

        simplified_sketch = np.asarray(simplified_sketch, dtype=float)
        return simplified_sketch

    except Exception as e:
        print('Error encountered: {} - {}'.format(type(e), e))
        raise

def normalize(data):
    data = np.asarray(data, dtype=float)

    min_x, max_x, min_y, max_y = sketch.get_bounds(data)
    max_dim = max([max_x - min_x, max_y - min_y, 1])
    data[:, :2] /= max_dim

    return data

def predict(model, batch_data):
    # Takes the data in stroke-3 and relative format
    predicted = []

    for data in batch_data:
        sketch_encoded = tokenizer.encode(data)
        pred = model.predict(sketch_encoded)
        cls = pred["class"][0]
        # print("pred embedding", pred["embedding"])
        predicted.append(obj_classes[cls])

    return predicted

def multi_predict(model, batch_data, k=3, conf_thold=-1):
    predicted = []

    for data in batch_data:
        batch_predicted = []
        sketch_encoded = tokenizer.encode(data)
        out = model.encode_from_seq(sketch_encoded)

        pred_labels = [tf.cast(val, tf.int32) for val in tf.argsort(out['class'], direction='DESCENDING', axis=-1)[0][:k]]
        for cls in pred_labels:
            if conf_thold < 0 or out['class'][0][cls] > conf_thold:
                batch_predicted.append(obj_classes[cls])
        predicted.append(batch_predicted)

    return predicted