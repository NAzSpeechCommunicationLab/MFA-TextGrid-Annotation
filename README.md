# MFA-TextGrid-Annotation
## Introduction
This repository contains a scripts for annotating recordings with textgrids so that they can be aligned by the Montreal Forced Aligner (MFA). The scripts assume that all sounding portions of the recording belong to a single important interval where a prompt word is read and then a target word is elicited a specified number of times. The sounding portions of the recording automatically are detected and a buffer of specified length is added at either end of the sounding interval. If the sounding portion is too close to the beginning or end of the recording (there isn't enough "room" to add the buffer), it will set the boundaries to the beginning and/or end instead.

The hope is to further document each of the individual parameters here, but they can also be understood by reading through the Praat documentation for the silence detection function [here](https://www.fon.hum.uva.nl/praat/manual/Sound__To_TextGrid__silences____.html).

### Batch Processing
By using the process_batch.py script, one can generate textgrids for all recordings in a directory. This requires a CSV file with columns for the gloss, the prompt word, and the target word (see words.csv for an example). A specific filename is also expected ([language ISO code]_[speaker ID]_[fieldworker ID]_[timestamp]__[stimulus item]__[repetition].wav)

#### Citing this repository
Please use the built-in citation option on GitHub ("Cite this repository" button in the sidebar) or see the CFF file for the relevant information. I have copied an example of the citation below:

Schnoor, T. T. (2023). MFA TextGrid  Annotation (Version 1.1) [Computer software]. https://github.com/NAzSpeechCommunicationLab/MFA-TextGrid-Annotation

Thank you!

### Installation and Compatibility
These scripts are tested on Windows 11. Although I have not tested these scripts using other operating systems, it is likely that they will not work perfectly on any non-Windows OS. That being said, it should require relatively little modification in order to make them work.

#### Installing Python
Python can be installed by following the instructions [here](https://wiki.python.org/moin/BeginnersGuide/Download).

#### Installing Pandas
Pandas is a Python package that is used in process_batch.py to find words in the CSV file. It can be installed easily using pip, a package manager that is automatically installed alongside Python. You can install Pandas using the following command:
```
pip install pandas
```

#### Installing Praat
Praat can be installed by following the instructions [here](https://www.fon.hum.uva.nl/praat/download_win.html).

### Running the scripts
A batch of files can be processed by running the Python script called process_batch.py in command line as follows:
```
python process_batch.py
```
This will open a GUI that will allow you to adjust the parameters according to your needs. If you want to generate a textgrid one file at a time (to debug something, perhaps), then run the Praat script by opening it in the Praat script and running it using CTRL+r. This will also open a GUI for parameter adjustment.

### Updates
##### 1.1 2023-05-01 (generate_textgrid.praat)
Parameters for silence detection are no longer specified in the form, as these will be kept as the defaults in most cases. This also simplifies the process of calling the Praat script from Python.
