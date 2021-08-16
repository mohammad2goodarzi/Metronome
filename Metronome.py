import winsound
import threading
import os.path


def searcher():
    textFile = open(locationText, 'r')
    soundLocationFromFile = textFile.read()
    textFile.close()
    if os.path.isfile(locationSound):  # if sound and metronome are in the same directory
        open(locationText, 'w').close()
        file = open(locationText, 'w')
        file.write(locationSound)
        file.close()
        return locationSound
    if os.path.isfile(soundLocationFromFile):
        return soundLocationFromFile
    if not os.path.isfile(locationSound) and not os.path.isfile(soundLocationFromFile):
        newSoundLocation = input('wav sound not found please Enter the directory\n')
        open(locationText, 'w').close()
        file = open(locationText, 'w')
        if os.path.isfile(newSoundLocation):
            file.write(newSoundLocation)
            file.close()
            return newSoundLocation
        else:
            newSoundLocation = wrongPath()
            return newSoundLocation


def wrongPath():
    newSoundLocation2 = input("Wrong Path! Please Enter A Valid Path\n")
    if os.path.isfile(newSoundLocation2):
        open(locationText, 'w').close()
        file = open(locationText, 'w')
        file.write(newSoundLocation2)
        file.close()
        return newSoundLocation2
    else:
        wrongPath()


def play():
    threading.Timer(60.0 / tempo, play).start()
    winsound.PlaySound(searcher(), winsound.SND_ASYNC)


loc = os.path.dirname(os.path.realpath(__file__))
locationText = loc + '\\location.txt'
locationSound = loc + '\\tick.wav'
if not os.path.isfile(locationText):  # creates a txt file if there isn't one
    file = open(locationText, "w+")
    file.close()


if os.path.isfile(searcher()):
    try:
        temp = int(input('Enter The Tempo\n'))
    except ValueError:
        print("Number must be an Integer like:\n120")
        temp = 120
    if 0 < temp < 401:
        tempo = int(temp)
    while not (0 < temp < 401):
        print("number must be between 1 and 400")
        temp = int(input('Enter The Tempo\n'))
        if 0 < temp < 401:
            tempo = int(temp)

    play()

    while os.path.isfile(searcher()):
        try:
            temp = int(input('Enter another Tempo\n'))
        except ValueError:
            print("Number must be an Integer")
        if 0 < temp < 401:
            tempo = int(temp)
        while not (0 < temp < 401):
            print("number must be between 1 and 400")
            temp = int(input('Enter The Tempo\n'))
            if temp > 0 and temp < 401:
                tempo = int(temp)
