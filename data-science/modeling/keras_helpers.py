import tensorflow as tf

def create_model(x_train, y_train, input_shape, 
                 n_class):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        tf.keras.layers.Conv2D(
            32, kernel_size=(3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            64, kernel_size=(3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(n_class, 
                              activation="softmax"),
    ])
    model.compile(loss="categorical_crossentropy",
                  optimizer="adam", 
                  metrics=["accuracy"])
    model.fit(x_train, y_train, 
              batch_size=32, epochs=1, 
              validation_split=0.1)
    return model
