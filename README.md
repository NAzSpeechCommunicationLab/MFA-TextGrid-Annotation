# MFA-TextGrid-Annotation
This repository contains a Praat script for annotating recordings with textgrids so that they can be aligned by the Montreal Forced Aligner (MFA). The script assumes that all sounding portions of the recording belong to a single important utterance. It detects the sounding portion of the recording automatically and adds a buffer of specified length at either end of the sounding interval. If the sounding portion is too close to the beginning or end of the recording (there isn't enough "room" to add the buffer), it will set the boundaries to the beginning and/or end instead.

The hope is to further document each of the individual parameters here, but they can also be understood by reading through the Praat documentation for the silence detection function [here](https://www.fon.hum.uva.nl/praat/manual/Sound__To_TextGrid__silences____.html).

### Batch Processing
Scripts for processing multiple files are in development. Check back here for information on batch processing.

#### Citing this repository
Please use the built-in citation option on GitHub ("Cite this repository" button in the sidebar) or see the CFF file for the relevant information.

Thank you!