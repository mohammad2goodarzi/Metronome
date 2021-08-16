from tkinter import *
import winsound
import threading
import os.path
from PIL import Image, ImageTk
from itertools import count


class ImageLabel(Label):
    """a label that displays images, and plays them if they are gif"""

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

    def set_delay(self, number2):
        self.delay = number2


loc = os.path.dirname(os.path.realpath(__file__))
locationText = loc + '\\location.txt'
locationSound = loc + '\\tick.wav'
if not os.path.isfile(locationText):  # creates a txt file if there isn't one
    file = open(locationText, "w+")
    file.close()


def searcher():
    textFile = open(locationText, 'r')
    soundLocationFromFile = textFile.read()
    textFile.close()
    if os.path.isfile(locationSound):  # if sound and metronome are in the same directory
        open(locationText, 'w').close()
        file2 = open(locationText, 'w')
        file2.write(locationSound)
        file2.close()
        return locationSound
    if os.path.isfile(soundLocationFromFile):
        return soundLocationFromFile
    if not os.path.isfile(locationSound) and not os.path.isfile(soundLocationFromFile):
        newSoundLocation = input('wav sound not found please Enter the directory\n')
        open(locationText, 'w').close()
        file2 = open(locationText, 'w')
        if os.path.isfile(newSoundLocation):
            file2.write(newSoundLocation)
            file2.close()
            return newSoundLocation
        else:
            newSoundLocation = wrongPath()
            return newSoundLocation


def wrongPath():
    newSoundLocation2 = input("Wrong Path! Please Enter A Valid Path\n")
    if os.path.isfile(newSoundLocation2):
        open(locationText, 'w').close()
        file3 = open(locationText, 'w')
        file3.write(newSoundLocation2)
        file3.close()
        return newSoundLocation2
    else:
        wrongPath()


def play():
    global row, tempo, t
    x = int(59 * (60 / tempo))
    lbl.set_delay(x)
    t = threading.Timer(60.0 / tempo, play)
    t.start()
    winsound.PlaySound(searcher(), winsound.SND_ASYNC)


def tagh():
    global tempo, number
    if e.get():
        temp = e.get()
        tempo = int(temp)
    else:
        e.insert(0, "120")
        tempo = 120
    if number == 1:
        number = 2
        the_label['text'] = 'Enter another tempo: '
        play()
        lbl.grid(row=1, column=0, columnspan=2)


t = None
tempo, number = 50, 1
row, column = 2, 0
root = Tk()
root.title("Metronome Pro")
root.iconbitmap('metronome_icon.ico')

frame = LabelFrame(root)
frame.pack()
the_label = Label(frame, text="        Enter the tempo: ")

e = Entry(frame, width=35, borderwidth=5)
the_button = Button(frame, text='tagh', command=tagh)
lbl = ImageLabel(frame)
lbl.load('metronome gif.gif')

the_label.grid(row=0, column=0)
e.grid(row=0, column=1)
the_button.grid(row=2, column=0, columnspan=2)


root.mainloop()
if t is not None:
    t.cancel()
