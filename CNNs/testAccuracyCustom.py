#Fout: 
#Verboden voor auto's (wordt einde voorangsweg)
#Verboden in te gaan (wordt meerdere)
#Stoplichten++
#Voorangsweg
#Vijftig
#Doodlopen
#Eenrichtingspijl

import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy as np
# Load the trained model to classify sign
from keras.models import load_model

model = load_model('traffic_classifier_custom.h5')

# Dictionary to label all traffic signs class.
# classes = {1: 'Leeg (0)',
#            2: 'Vijftig (1)',
#            3: 'Doodlopende weg(2)',
#            4: 'Eenrichtingspijl (3)',
#            5: 'Einde voorangsweg(4)',
#            6: 'Haaientanden(5)',
#            7: 'Verboden voor auto\'s(6)',s
#            8: 'Verboden in te halen(7)',
#            9: 'Verboden in te gaan(8)',
#            10: 'Parkeerverbod(9)',
#            11: 'Verboden te stoppen (10)',
#            12: 'Stop! (11)',
#            13: 'Stoplicht oranje(12)',
#            14: 'Stoplicht groen(13)',
#            15: 'Stoplicht rood(14)',
#            16: 'Voorangsweg (15)'}

classes = {1: 'Stoplicht rood (0)',
           2: 'Stoplicht oranje (1)',
           3: 'Stoplicht groen (2)',
           4: 'Voorangsweg (3)',
           5: 'Vijftig (4)',
           6: 'Doodlopende weg (5)',
           7: 'Eenrichtingspijl (5)'}


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
