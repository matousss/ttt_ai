import numpy

from ai.data import get_raw_data
from ai.model import create_model, train

if __name__ == '__main__':
    raw = get_raw_data('./data.txt')
    data_x, data_y = numpy.array(raw[0]), numpy.array(raw[1])

    # model = create_model(hidden_layers=[12, 14, 14, 12])
    model = create_model(hidden_layers=[1])
    model = train(model, (data_x, data_y), 300, 32)

    model.save('model.h5')
