import os
from keras.utils import load_img, img_to_array
import numpy as np
import matplotlib.pyplot as plt


def predict_digit(model, img_name : str) -> str:

    """
    summary: predict what is the digit from an image
    """

    img_pil = load_img(img_name,
                       color_mode='grayscale')
    img_arr = img_to_array(img_pil, dtype='float32') / 255.0
    img_arr = np.array([img_arr])  # convert to single batch
    y_pred = np.argmax(model.predict(img_arr))
    plt.imshow(img_arr[0], cmap='gray')
    plt.axis(False)
    plt.title(y_pred)
    name = os.path.split(img_name)[1]
    #plt.savefig(f'results/pred_{name}', bbox_inches='tight')

    return str(y_pred)
