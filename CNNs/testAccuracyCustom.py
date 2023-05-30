import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy as np
# Load the trained model to classify sign
from keras.models import load_model

model = load_model('traffic_classifier_custom.h5')

# Dictionary to label all traffic signs class.
classes = {1: '50 (0)',
           2: 'Verboden auto (1)',
           3: 'stop (2)',
           4: 'debug4',
           5: 'debug5',
           6: 'debug6',
           7: 'debug7',
           8: 'debug8',
           9: 'debug9',
           10: 'debug10',
           11: 'debug11'
           }


# Initialise GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Traffic sign classification')
top.configure(background='#CDCDCD')
label = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(top)


def classify(file_path):
    global label_packed
    image = Image.open(file_path)
    #mijn code
    #image = image.rotate(180)
    #einde mijn code
    image = image.resize((30, 30))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    pred_probs = model.predict(image)  # Get predicted probabilities for each class
    pred = np.argmax(pred_probs)  # Get the class label with highest probability using np.argmax

    print(pred)
    sign = classes[pred + 1]
    print(sign)
    label.configure(foreground='#011638', text=sign)


def show_classify_button(file_path):
    classify_b = Button(top, text="Classify Image", command=lambda: classify(file_path), padx=10, pady=5)
    classify_b.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
    classify_b.place(relx=0.79, rely=0.46)


def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        #mijn code
        #uploaded = uploaded.rotate(180)
        #einde mijn code
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass


upload = Button(top, text="Upload an image", command=upload_image, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
upload.pack(side=BOTTOM, pady=50)
sign_image.pack(side=BOTTOM, expand=True)
label.pack(side=BOTTOM, expand=True)
heading = Label(top, text="check traffic sign", pady=20, font=('arial', 20, 'bold'))
heading.configure(background='#CDCDCD', foreground='#364156')
heading.pack()
top.mainloop()
