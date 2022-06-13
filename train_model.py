import numpy

from ai.data import load_data
from ai.model import create_model, train


def get_raw(*paths):
    data_x_raw, data_y_raw = [], []
    for p in paths:
        loaded = load_data(p)
        for i in range(len(loaded[0])):
            data_x_raw.append(loaded[0][i])
            data_y_raw.append(loaded[1][i])

    return data_x_raw, data_y_raw


if __name__ == '__main__':
    raw = get_raw('./data/data_random-minimax.txt')
    data_x, data_y = numpy.array(raw[0]), numpy.array(raw[1])

    model = create_model(hidden_layers=[12, 14, 14, 12])
    model = train(model, (data_x, data_y), 300, 32)

    model.save('model.h5')
