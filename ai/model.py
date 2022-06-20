import numpy
from keras.layers import Dense

from keras.models import Sequential as KerasModel
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split


def create_model(input_shape=(9,), output_shape=9, hidden_layers=(1,)):
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


def train(model, data, epochs, batch_size, include_metrics=False):
    input_data = data[0]
    output_data = data[1]

    x = numpy.array(input_data)
    y = numpy.array(output_data)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    model.fit(x=x_train, y=y_train,
              batch_size=batch_size, epochs=epochs,
              shuffle=True, verbose=0,
              validation_split=0.3)

    pred = model.predict(x_test)

    mae, mse = mean_absolute_error(y_test, pred), mean_squared_error(y_test, pred, squared=False)

    print(f"MAE: {mae}, MSE: {mse}")

    if include_metrics:
        return model, mae, mse
    return model
