import threading
import time
from keras.activations import relu, sigmoid
from keras.models import load_model
from tensorflow import keras
from keras import regularizers
import myo
import numpy as np
from tensorflow.python.keras.activations import softmax
from tensorflow_addons.callbacks import TQDMProgressBar

import stream_service as Stream
from constants import *
import matplotlib.pyplot as plt
import datetime as dt


class Classification:
    def __init__(self,
                 subject_name: str = None,
                 subject_age: int = 0,
                 batch_size: int = 10,
                 epochs: int = 300,
                 ):
        self.batch_size = batch_size
        self.epochs = epochs
        self.subject_name = subject_name
        self.subject_age = subject_age
        self.training_samples = samples * 10
        self.validation_samples = samples
        self.all_training_set = []
        self.exercises = PREDEFINED_EXERCISES
        self.number_of_gestures = len(self.exercises)

        self.div = batch_size  # every 25 batch ( 500/25 -> 20 data )
        self.training_averages = int(self.training_samples / batch_size)
        self.validation_averages = int(self.validation_samples / (batch_size / 10))
        self.all_training_set = {}
        self.all_averages = []

        for i in range(0, self.number_of_gestures):
            self.all_training_set[i] = np.zeros((8, self.training_samples))
            self.all_averages.append(np.zeros((int(self.training_averages), 8)))

        self.training_set = np.zeros((8, self.training_averages))
        self.validation_set = np.zeros((8, self.validation_averages))

        self.input_data = None
        self.history = None

        self.hub = myo.Hub()

    def PrepareTrainingData(self):
        for x in range(0, self.number_of_gestures):
            time.sleep(1)
            exercise = self.exercises[x]
            print("Recording - ", exercise.name)
            print("---------------------------")
            print("Instructions: ", exercise.instruction)
            time.sleep(1)
            while True:
                try:
                    hub = myo.Hub()
                    listener = Stream.Listener(self.training_samples)
                    hub.run(listener.on_event, 3000)
                    self.all_training_set[x] = np.array(data)
                    print(self.all_training_set[x].shape)
                    data.clear()
                    break
                except Exception as e:
                    print(e)
                    while not Stream.MyoService.restart_process():
                        pass
                    # Wait for 3 seconds until Myo Connect.exe starts
                    time.sleep(3)

            print(exercise.name, "data READY.")
            time.sleep(1)

        conc_data = self.calculateMeanData()
        self.SaveTrainingData(conc_data)

    def calculateMeanData(self):
        # Absolutes of foot gesture data
        for x in range(0, self.number_of_gestures):
            self.all_training_set[x] = np.absolute(self.all_training_set[x])

        for i in range(1, self.training_averages + 1):
            for x in range(0, self.number_of_gestures):
                self.all_averages[x][i - 1, :] = np.mean(
                    self.all_training_set[x][(i - 1) * self.div:i * self.div, :], axis=0)

        # Here we stack all the data row wise
        conc_array = np.concatenate(self.all_averages, axis=0)
        return conc_array

    def TestLatency(self, reps):
        average = 0.0
        counter = 0
        model = load_model(TRAINING_MODEL_PATH + self.subject_name + '.h5')
        validation_averages = np.zeros((int(self.validation_averages), 8))
        listener = Stream.PredictListener(self.validation_samples)
        thread = threading.Thread(target=lambda: self.hub.run_forever(listener.on_event, 100))
        thread.start()

        while counter < reps:
            start = time.time()

            while len(data) < samples:
                pass

            current_data = data[-samples:]  # get last nr_of_samples elements from list
            self.validation_set = np.array(current_data)
            self.validation_set = np.absolute(self.validation_set)

            print(self.validation_set)
            # We add one because iterator below starts from 1
            batches = int(samples / self.div) + 1  # 50/25 => 2+1 = 3
            for i in range(1, batches):
                validation_averages[i - 1, :] = np.mean(self.validation_set[(i - 1) * self.div:i * self.div, :],
                                                        axis=0)

            validation_data = validation_averages
            predictions = model.predict(validation_data, batch_size=validation_data.shape[0])
            print(validation_data.shape)

            predicted_value = np.argmax(predictions[0])

            end = time.time()
            data.clear()
            print(
                "Predicted:", predicted_value
                , "Latency:", (end - start) * 1000, "ms"
            )
            average += (end - start) * 1000
            counter += 1

        self.hub.stop()
        thread.join()
        print("Average: ", average / counter)

    def LoadTrainingData(self):
        print("Loading data from disk!")
        if self.input_data is None:
            try:
                input_data = np.loadtxt(TRAINING_DATA_PATH + self.subject_name + '.txt')
                return input_data
            except FileNotFoundError:
                return []
        else:
            return self.input_data

    def SaveTrainingData(self, training_data):
        try:
            np.savetxt(TRAINING_DATA_PATH + self.subject_name + '.txt', training_data, fmt='%i')
            self.input_data = training_data
            print("Saving training data successful!")
        except Exception as e:
            print(e)
            print("Saving training data failed!")

    def TrainEMG(self):
        input_data = self.LoadTrainingData()
        print("Input data:", input_data.shape)
        labels = []

        samples = input_data.shape[0] / self.number_of_gestures
        print("Preprocess EMG data of ", self.subject_name, "with ", samples, " samples per", self.number_of_gestures,
              "exercise, training data with a nr. of ",
              self.batch_size, "batch size, for a total of ", self.epochs, "epochs.")

        # Now we append all data in training label
        for i in range(0, self.number_of_gestures):
            for j in range(0, int(samples)):
                labels.append(i)
        labels = np.asarray(labels)
        permutation_function = np.random.permutation(input_data.shape[0])
        total_samples = input_data.shape[0]
        all_shuffled_data, all_shuffled_labels = input_data[permutation_function], labels[permutation_function]

        number_of_training_samples = int(np.floor(0.8 * total_samples))
        train_data = all_shuffled_data[0:number_of_training_samples, :]
        train_labels = all_shuffled_labels[0:number_of_training_samples, ]
        print("Length of train data is ", train_data.shape)

        validation_data = all_shuffled_data[number_of_training_samples:total_samples, :]
        validation_labels = all_shuffled_labels[number_of_training_samples:total_samples, ]
        print("Length of validation data is ", validation_data.shape, " validation labels is ", validation_labels.shape)

        print("Building model...")
        instructions = "Building model..."

        model = keras.Sequential([
            keras.layers.Dense(8, activation=relu, input_dim=8, kernel_regularizer=regularizers.l2(0.1)),
            keras.layers.BatchNormalization(),
            keras.layers.Dense(self.number_of_gestures, activation=softmax)])
        adam_optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0,
                                               amsgrad=False)
        model.compile(optimizer=adam_optimizer,
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        print(model.summary())
        print("Fitting training data to the model...")
        tqdm_callback = TQDMProgressBar(
            show_epoch_progress=False,
            leave_overall_progress=False,
            leave_epoch_progress=False
        )
        history = model.fit(train_data, train_labels, epochs=self.epochs,
                            validation_data=(validation_data, validation_labels),
                            batch_size=self.batch_size, verbose=0,
                            callbacks=[tqdm_callback],
                            )
        print("Training model successful!")
        print("Max accuracy:", history.history['val_accuracy'][-1])
        print("Saving model for later...")
        save_path = TRAINING_MODEL_PATH + self.subject_name + '.h5'
        model.save(save_path)
        self.history = history.history
        return history.history

    def DisplayResult(self, data):
        history = data
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        # Here we display the training and test loss for model
        ax1.plot(history['accuracy'])
        ax1.plot(history['val_accuracy'])
        ax1.set_title('model accuracy')
        ax1.set_ylim((0, 1.05))
        # ax1.c('accuracy')
        ax1.set_xlabel('epoch')
        ax1.legend(['train', 'test'], loc='lower right')
        # ax1.show()
        # summarize history for loss
        ax2.plot(history['loss'])
        ax2.plot(history['val_loss'])
        ax2.set_title('model loss')
        ax2.set_xlabel('loss')
        ax2.set_xlabel('epoch')
        ax2.legend(['train', 'test'], loc='upper right')
        plt.interactive(False)
        self.save_plot(plt)
        plt.show()

    def save_plot(self, plot):
        save_file = self.subject_name + '_' + (dt.datetime.now()).strftime("%Y-%m-%d-%H+%M+%S") + '_train.png'
        plot.savefig(FIGURES_PATH + save_file, bbox_inches='tight')
        print(save_file + " :figure saved successfully!")
