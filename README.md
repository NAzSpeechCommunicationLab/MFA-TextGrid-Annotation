# MFA-TextGrid-Annotation
This repository contains a scripts for annotating recordings with textgrids so that they can be aligned by the Montreal Forced Aligner (MFA). The scripts assume that all sounding portions of the recording belong to a single important interval where a prompt word is read and then a target word is elicited a specified number of times. The sounding portions of the recording automatically are detected and a buffer of specified length is added at either end of the sounding interval. If the sounding portion is too close to the beginning or end of the recording (there isn't enough "room" to add the buffer), it will set the boundaries to the beginning and/or end instead.

The hope is to further document each of the individual parameters here, but they can also be understood by reading through the Praat documentation for the silence detection function [here](https://www.fon.hum.uva.nl/praat/manual/Sound__To_TextGrid__silences____.html).

### Batch Processing
By using the process_batch.py script, one can generate textgrids for all recordings in a directory. This requires a CSV file with columns for the gloss, the prompt word, and the target word (see words.csv for an example). A specific filename is also expected ([language ISO code]_[speaker ID]_[fieldworker ID]_[timestamp]__[stimulus item]__[repetition].wav).

#### Citing this repository
Please use the built-in citation option on GitHub ("Cite this repository" button in the sidebar) or see the CFF file for the relevant information.

Thank you!