############################################################################################################
# Author: Tyler Schnoor
# Version: 1.1
# Last Updated: 2023-05-01
# Repository: https://github.com/NAzSpeechCommunicationLab/MFA-TextGrid-Annotation
#
# Description: This repository contains a Praat script for annotating recordings with textgrids so that they 
# 	can be aligned by the Montreal Forced Aligner (MFA). The script assumes that all sounding portions of 
# 	the recording belong to a single important utterance. It detects the sounding portion of the recording 
# 	automatically and adds a buffer of specified length at either end of the sounding interval. If the sounding 
# 	portion is too close to the beginning or end of the recording (there isn't enough "room" to add the buffer), 
# 	it will set the boundaries to the beginning and/or end instead.
#
# Citation: Schnoor, T. T. (2023). MFA TextGrid  Annotation Script (Version 1.0) [Computer software]. https://github.com/NAzSpeechCommunicationLab/MFA-TextGrid-Annotation
#############################################################################################################

form This script creates a textgrid and annotates the sounding portion with the given transcription.
	text Path_to_audio_file recordings\\test_recording.wav
	text Path_to_copied_audio_file annotated_recordings\\test_recording.wav
	text Path_to_textgrid annotated_recordings\\test_recording.textgrid
	text Transcription This is a test recording
	text Speaker_name tts
	positive Time_buffer 0.150
	# comment The following parameters are used to detect the sounding portion of the recording.
	# positive Minimum_pitch 100
	# real Time_step 0.0
	# real Silence_threshold -25
	# positive Minimum_silent_interval 0.1
	# positive Minimum_sounding_interval 0.1
	# comment Check this box to save the intermediate textgrid with automatically detected sounding intervals (for debugging)
	# boolean Save_silences_textgrid 0
	# comment Check this box if you want to copy the audio file to the specified path
	# boolean Copy_audio 1
endform

minimum_pitch = 100
time_step = 0.0
silence_threshold = -25
minimum_silent_interval = 0.1
minimum_sounding_interval = 0.1
save_silences_textgrid = 0
copy_audio = 1

Read from file: path_to_audio_file$
soundObject$ = selected$: "Sound"
dur = Get total duration

# These variables store temporary start and end indices
start = 0
end = 0

# Automatically detect sounding intervals
To TextGrid (silences): minimum_pitch, time_step, silence_threshold, minimum_silent_interval, minimum_sounding_interval, "", "sound"

# Save intermediate textgrid if specified
if save_silences_textgrid == 1
	Save as text file: "silences.textgrid"
endif

numberOfIntervals = Get number of intervals: 1

# Find the start of the sounding interval
text$ = Get label of interval: 1, 1
if text$ == "sound"
	# writeInfoLine: "first interval is sounding"
	start = Get start point: 1, 1
else
	# writeInfoLine: "first interval is silent"
	start = Get start point: 1, 2
endif

# Find the end of the sounding interval
text$ = Get label of interval: 1, numberOfIntervals
if text$ == "sound"
	# writeInfoLine: "last interval is sounding"
	end = dur
else
	# writeInfoLine: "last interval is silent"
	end = Get start point: 1, numberOfIntervals
endif	

# Add the buffer if there is enough room
Insert interval tier: 1, speaker_name$
if start - time_buffer > 0
	Insert boundary: 1, start - time_buffer
else
	# writeInfoLine: path_to_audio_file$, " - Not enough room to add start buffer"
endif
if end + time_buffer < dur
	Insert boundary: 1, end + time_buffer
else
	# writeInfoLine: path_to_audio_file$, " - Not enough room to add end buffer"
endif
Remove tier: 2

# Set the appropriate interval's text to the specified transcription
if start == 0
	Set interval text: 1, 1, transcription$
else
	Set interval text: 1, 2, transcription$
endif

# Save the textgrid
Save as text file: path_to_textgrid$

# Copy the audio if specified
if copy_audio == 1
	selectObject: "Sound "+soundObject$
	Save as WAV file: path_to_copied_audio_file$
endif

# Clean up
select all
Remove
