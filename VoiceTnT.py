# VoiceTnT.py
# a tool for translation and dictation of live speech
# for instructions see ReadMe.md

import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator, constants
import pygame
import os
import mmap
import keyboard
import time
import argparse

# default settings
language1="de"
language2="ro"
hotkey = ["alt+1","alt+2","alt+3"]
keyboardMode=False

# global variables
count = 0
inLanguage=""
outLanguage=""
running=True
translator = Translator()
r = sr.Recognizer()
# Note: following parameters could be used if the Recognizer doesn't properly discriminate speech from silence:
# r.energy_threshold = 4000
# r.dynamic_energy_threshold = True
# r.min_phrase_length = 5
# r.max_phrase_length = 50

def play(fileName):
    pygame.mixer.music.load(fileName)
    pygame.mixer.music.play()

def speakNow (msg, loc):
    global count
    speech = gTTS(text=msg, lang=loc)  # converts text to speech
    # save the audio to a temporary file
    # Note: as pygame mixer doesn't close the file properly, two alternating files are used
    speech_file = f'./data/speech{count%2}.mp3'
    count += 1
    speech.save(speech_file)    
    play(speech_file)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def loadhotkey():
    global hotkey
    with open("hotkeys.txt", "r") as parameterFile:
        allLines=parameterFile.readlines()
    hotkey = [s.rstrip() for s in allLines]

def recordhotkey():
    global hotkey
    print('Press and release your desired hotkey for Language1: ', end="", flush=True)
    hotkey[0] = keyboard.read_hotkey(suppress=False)
    print (hotkey[0])
    time.sleep(1)

    print('Press and release your desired hotkey for Language2: ', end="", flush=True)
    hotkey[1] = keyboard.read_hotkey(suppress=False)
    print (hotkey[1])
    time.sleep(1)

    print('Press and release your desired hotkey for ModeChange: ', end="", flush=True)
    hotkey[2] = keyboard.read_hotkey(suppress=False)
    print (hotkey[2])

    with open("hotkeys.txt", "w+") as parameterFile:
        parameterFile.writelines([actkey + "\n" for actkey in hotkey])

def recognizeVoice():
    play("./data/attention.wav")
    print("Listening ....")
    with sr.Microphone() as source:
        #r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        # recognize speech using Google Speech Recognition via the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # for using Whisper offline, use  `r.recognize_whisper(audio, language="english") `
        recognizedText = r.recognize_google(audio, language=inLanguage)
        print("I think you said: " + recognizedText)
        if keyboardMode == False:
            translation = translator.translate(recognizedText, src=inLanguage, dest=outLanguage)
            print ("translated text: " + str(translation.text.encode("utf-8")))
            speakNow (translation.text, outLanguage)
        else:
            print('typing text ..')
            keyboard.write(recognizedText)

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))

def on_KeyRecognize1():
    global inLanguage, outLanguage
    inLanguage=language1
    outLanguage=language2
    recognizeVoice()

def on_KeyRecognize2():
    global inLanguage, outLanguage
    inLanguage=language2
    outLanguage=language1
    recognizeVoice()

def on_KeyToggleKeyboardMode():
    global keyboardMode
    if keyboardMode == True:
        keyboardMode=False
        print('Swichted to Translation mode (no keyboard-typing).')
    else:
        keyboardMode=True
        print('Swichted to Keyboard mode (no translation).')
    play("./data/toggleMode.wav")
        
def on_KeyEscape():
    global running
    running=False
    play("./data/exit.wav")

# main action starts here .. 
# first: check commandline arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-l1", help="the first language which shall be recognized/translated (default=de)")
argParser.add_argument("-l2", help="the second language which shall be recognized/translated (default=ro)")
argParser.add_argument('-k', "--keyboard", help="start in keyboard mode (type recognized text, do not translate)", action='store_true')
argParser.add_argument('-r', "--record", help="record hotkeys", action='store_true')

args = argParser.parse_args()
keyboardMode=args.keyboard
if args.l1 != None:
    language1=args.l1
if args.l2 != None:
    language2=args.l2

# init pygame / media player
pygame.init() 
pygame.mixer.init()

# welcome message and sound
print ("\nWelcome to VoiceTnT!")
play('./data/startup.wav')

# record/load/bind hotkey
if args.record == True:
    print ("Now recording new hotkeys!")
    recordhotkey()
    
loadhotkey()
keyboard.add_hotkey(hotkey[0], on_KeyRecognize1)
keyboard.add_hotkey(hotkey[1], on_KeyRecognize2)
keyboard.add_hotkey(hotkey[2], on_KeyToggleKeyboardMode)
keyboard.add_hotkey('esc', on_KeyEscape)
print ("\nThe active hotkeys are:")
print ("  listen to language 1:" + hotkey[0])
print ("  listen to language 2:" + hotkey[1])
print ("  toggle mode (translation / keyboard):" + hotkey[2])
print ("  exit: Esc")


# nothing to do in the main loop ..
while running==True:
    time.sleep(1)