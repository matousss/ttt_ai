from keras.layers import Dense
from keras.models import Sequential as KerasModel


def create_model(input_shape=9, output_shape=9, hidden_layers=(9,)):
    """
    Creates a model for the neural network.
    :param input_shape: shape of the input data
    :param output_shape: shape of the output data
    :param hidden_layers: units of hidden layers
    :return: model
    """
    model = KerasModel()
    model.add(Dense(units=64, activation='relu', input_shape=input_shape))

    for i in hidden_layers:
        model.add(Dense(units=i, activation='relu'))

    model.add(Dense(units=output_shape, activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
