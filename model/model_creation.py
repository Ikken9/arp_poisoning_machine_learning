import tensorflow as tf


def set_labels(data):
    seen = []
    labels = []
    for pkt in data:
        if pkt not in seen:
            seen.append(pkt)

    n = len(seen)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if (seen[i][0] == seen[j][0]) and (seen[i][1] != seen[j][1]):
                labels[i] = 1
            else:
                labels[i] = 0

    return labels


def create_model():
    # Define the classifier model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


def train(model, x_train, y_train, x_test, y_test):
    # Train the model
    model.fit(x_train, y_train, batch_size=32, epochs=10, validation_data=(x_test, y_test))

    return model


def evaluate_model(model, x_test, y_test):
    loss, accuracy = model.evaluate(x_test, y_test)
    print('Test Loss:', loss)
    print('Test Accuracy:', accuracy)


def save_model(model, path):
    model.save(path)


def load_model(path):
    loaded_model = tf.keras.models.load_model(path)
    return loaded_model