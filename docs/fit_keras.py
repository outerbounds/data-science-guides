from metaflow import FlowSpec, step, Parameter, batch
import tensorflow as tf
import tempfile

class KerasFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.get_data)
        
    @step
    def get_data(self):
        import numpy as np
        self.n_class = 10
        self.input_shape = (28, 28, 1)
        mnist = tf.keras.datasets.mnist.load_data()
        (x_train, y_train), (x_test, y_test) = mnist
        x_train = x_train.astype("float32") / 255
        x_test = x_test.astype("float32") / 255
        self.x_train = np.expand_dims(x_train, -1)
        self.x_test = np.expand_dims(x_test, -1)
        self.y_train = tf.keras.utils.to_categorical(
            y_train, self.n_class)
        self.y_test = tf.keras.utils.to_categorical(
            y_test, self.n_class)
        self.next(self.fit_model) 
    
    @step
    def fit_model(self):
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Input(
                    shape=self.input_shape),
                tf.keras.layers.Conv2D(
                    32, kernel_size=(3, 3), 
                    activation="relu"),
                tf.keras.layers.MaxPooling2D(
                    pool_size=(2, 2)),
                tf.keras.layers.Conv2D(
                    64, kernel_size=(3, 3),
                    activation="relu"),
                tf.keras.layers.MaxPooling2D(
                    pool_size=(2, 2)),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(
                    self.n_class, activation="softmax"),
            ]
        )
        model.compile(loss="categorical_crossentropy", 
                      optimizer="adam", 
                      metrics=["accuracy"])
        model.fit(self.x_train, self.y_train, 
                  batch_size=32, epochs=1, 
                  validation_split=0.1)
        with tempfile.NamedTemporaryFile() as f:
            tf.keras.models.save_model(model, f.name, 
                                       save_format='h5')
            self.model = f.read()
        self.next(self.evaluate_model)
        
    @step
    def evaluate_model(self):
        with tempfile.NamedTemporaryFile() as f:
            f.write(self.model)
            f.flush()
            model =  tf.keras.models.load_model(f.name)
        self.score = model.evaluate(self.x_test, 
                                    self.y_test, 
                                    verbose=0)
        self.next(self.end)
    
    @step
    def end(self):
        print("Test loss:", self.score[0])
        print("Test accuracy:", self.score[1])

if __name__ == "__main__":
    KerasFlow()
