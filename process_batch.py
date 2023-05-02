############################################################################################################
# Author: Tyler Schnoor
# Version: 1.0
# Date: 2023-05-01
# Repository: https://github.com/NAzSpeechCommunicationLab/MFA-TextGrid-Annotation
#
# Description: 
#
# Citation: Schnoor, T. T. (2023). MFA TextGrid  Annotation (Version 1.0) [Computer software]. https://github.com/NAzSpeechCommunicationLab/MFA-TextGrid-Annotation
#############################################################################################################

# This is where the necessary libraries are imported.

import os
import pandas as pd
from datetime import datetime

#Import the required libraries
from tkinter import *
from tkinter import ttk

#Create an instance of Tkinter Frame
win = Tk()

#Set the geometry
win.geometry("700x500")

# Get Praat path
Label(win, text="Path to Praat.exe file").pack()
praat_path_input = Entry(win, width= 42)
praat_path_input.insert(0, "Praat.exe")
praat_path_input.pack()

# Get source directory
Label(win, text="Path to directory containing recordings").pack()
recording_dir_input = Entry(win, width= 42)
recording_dir_input.pack()
recording_dir_input.insert(0, "recordings")

# Get target directory
Label(win, text="Path to directory where textgrids will be saved").pack()
target_dir_input = Entry(win, width= 42)
target_dir_input.pack()
target_dir_input.insert(0, "annotated_recordings")

# Get CSV
Label(win, text="Path to the CSV file that contains the words").pack()
csv_path = Entry(win, width= 42)
csv_path.pack()
csv_path.insert(0, "words.csv")

# # Copy audio
# check = IntVar()
# Label(win, text="Check this box if you would like to copy the audio over to the target directory").pack()
# copy_audio = Checkbutton(win, variable=check)
# copy_audio.pack()

# Get number of repetitions
Label(win, text="Enter the number of times the elicited form is repeated").pack()
n_repetitions = Entry(win, width = 10)
n_repetitions.pack()
n_repetitions.insert(0, "5")

# Get gloss column header
Label(win, text="Enter the header for the column which contains the glosses (these are the words that should be in the filename)").pack()
gloss_header_input = Entry(win, width= 42)
gloss_header_input.pack()
gloss_header_input.insert(0, "gloss")

# Get prompt column header
Label(win, text="Enter the header for the column which contains the prompt word").pack()
prompt_header_input = Entry(win, width= 42)
prompt_header_input.pack()
prompt_header_input.insert(0, "prompt")

# Get target word column header
Label(win, text="Enter the header for the column which contains the elicited word").pack()
word_header_input = Entry(win, width= 42)
word_header_input.pack()
word_header_input.insert(0, "word")

# Get time buffer
Label(win, text="Enter the amount of buffer (in seconds) to add to the beginning and end of the interval").pack()
time_buffer_input = Entry(win, width = 10)
time_buffer_input.pack()
time_buffer_input.insert(0, "0.200")

def process_batch():
    # get parameters from form
    praat = praat_path_input.get()
    base_dir = recording_dir_input.get()
    target_dir = target_dir_input.get()
    csv = csv_path.get()
    # copy = check.get()
    repetitions = n_repetitions.get()
    gloss_header = gloss_header_input.get()
    prompt_header = prompt_header_input.get()
    word_header = word_header_input.get()
    time_buffer = time_buffer_input.get()
    
    # read CSV into memory
    labels = pd.read_csv(csv)

    # open log file
    f = open("batch.log", "a")

    # logging function
    def log(message):
        now = datetime.now()
        line = now.strftime("%d/%m/%Y %H:%M:%S") + "\t" + message + "\n"
        f.write(line)

    # Here are some sanity checks.
    if not os.path.isfile(praat):
        raise Exception("Invalid Praat path given.")
    if not os.path.isfile(csv_path.get()):
        raise Exception("Invalid CSV file path given.")
    
    # Gather all audio files into an array.

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            audio = os.path.join(base_dir, file)
            copy_audio = os.path.join(target_dir, file)
            if not os.path.isfile(audio): # sanity check
                raise Exception("Could not find audio file:", audio)
            if audio[-4:] != ".wav":
                raise Exception(file, "is not a *.WAV file")
            textgrid = os.path.join(target_dir, file[:-4]+".TextGrid")
            if os.path.isfile(textgrid): # check whether audio is already annotated
                log(os.path.basename(audio) + " is already annotated. Skipping...")
                continue
            if "zero" in audio: # check for zero files (special case for Piaroa 2022)
                log("Skipping zero file: " + os.path.basename(audio))
                continue
            
            # Get the appropriate word from the filename to look up information in the table.
            # Expects following form: [language ISO code]_[speaker ID]_[fieldworker ID]_[timestamp]__[stimulus item]__[repetition].wav
            lang_iso = file.split("_")[0]
            speaker = file.split("_")[1]
            fieldworker_id = file.split("_")[2]
            time_stamp = file.split("_")[3]
            gloss = file.split("_")[5]
            # gloss = file.split("_")[5][:-1]
            # gender = file.split("_")[5][-1]

            try: 
                line = labels[labels[gloss_header].str.fullmatch(gloss, na=False)] # find the line with the appropriate gloss
            except:
                log("WORD NOT FOUND - THIS IS A PROBLEM " + file)
                print("WORD NOT FOUND - THIS IS A PROBLEM", file)
                continue
            try:
                word = line.iloc[0][word_header]
                prompt = line.iloc[0][prompt_header]
            except:
                log("WORD NOT FOUND - THIS IS A PROBLEM " + file)
                print("WORD NOT FOUND - THIS IS A PROBLEM", file)
                continue
            log("Gloss: " + gloss + " | Prompt word: " + prompt + " | Elicited word: " + word)

            # Run the Praat scripts.
            start = prompt + " "
            end = (word + " ")*int(repetitions)
            word = start + end[:-1]
            script_path = "generate_textgrid.praat"
            print(f'{praat} --run {script_path} {audio} {copy_audio} {textgrid} "{word}" {speaker} {time_buffer}')
            os.system(f'{praat} --run {script_path} {audio} {copy_audio} {textgrid} "{word}" {speaker} {time_buffer}') # annotate boundaries

    f.write("END \n\n")
    f.close()

#Create a Button to get the input data
ttk.Button(win, text= "Submit", command= process_batch).pack()

win.mainloop()