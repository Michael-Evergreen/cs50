import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    load_data(sys.argv[1])
    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])


    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    img_list = []
    label_list = []
    for category in os.listdir(data_dir):
        category_path = os.path.join(data_dir, category)
        for image in os.listdir(category_path):
            image_path = os.path.join(category_path, image)
            image_ndarray = cv2.imread(image_path)
            image_ndarray = cv2.resize(image_ndarray, (30, 30))
            img_list.append(image_ndarray)
            label_list.append(category)

    return (img_list, label_list)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    # Create a convolutional neural network

    """
        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(28, 28, 1)
        ),

        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # Add an output layer with output units for all 10 digits
        tf.keras.layers.Dense(10, activation="softmax")
    ])

    # Create a neural network
    model = tf.keras.models.Sequential()

    # Add a hidden layer with 8 units, with ReLU activation
    model.add(tf.keras.layers.Dense(8, input_shape=(4,), activation="relu"))

    # Add output layer with 1 unit, with sigmoid activation
    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

    # Train neural network
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    """


    model = tf.keras.models.Sequential([

        # tf.keras.layers.Dense(90, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), activation="relu", name="input_layer"),
        #
        # tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        #
        # tf.keras.layers.Conv2D(
        #     32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        # ),
        #
        # tf.keras.layers.Flatten(),
        # # tf.keras.layers.Dropout(0.1),
        #
        # tf.keras.layers.Dense(128, activation="relu", name="layer_1"),
        # # tf.keras.layers.Dropout(0.1),
        #
        # tf.keras.layers.Dense(128, activation="relu", name="layer_2"),
        # # tf.keras.layers.Dropout(0.1),
        #
        # tf.keras.layers.Dense(128, activation="relu", name="layer_3"),
        # # tf.keras.layers.Dropout(0.1),
        #
        # tf.keras.layers.Dense(128, activation="relu", name="layer_4"),
        # # tf.keras.layers.Dropout(0.1),
        #
        #
        # tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")


        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            64, (3, 3), activation="relu"
        ),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dropout(0.33),

        # add output layer with NUM_CATEGORIES outputs
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")

    ])
    model.compile(
            optimizer="adam",
            loss="binary_crossentropy",
            metrics=["accuracy"]
    )
    return model


if __name__ == "__main__":
    main()
