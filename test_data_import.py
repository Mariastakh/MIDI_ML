import numpy as numpy
from scipy import stats
#import pandas as pd 
import pretty_midi
import music21 # http://web.mit.edu/music21/ 
import warnings
import os

# Now load the output MIDI file into a PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI('/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/out.mid')
midi_path = '/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/Scales/CMajor.mid'
midi_path = '/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/out.mid'

# INCOMING MIDI FILES NEED TO BE FORMATTED INTO TWO CORRESPONDING FORMS:
# An array consisting of features, and an array consisting of actual note positions and pitches. 

# ------------ FEATURE ARRAY ----------------

# KEY:
score = music21.converter.parse(midi_path )
key = score.analyze('key')
key_sig = key.tonic.name
key_mode = key.mode
#print(key_sig, key_mode)

# Number of notes in the MIDI file:
numNotes = len(midi_data.instruments[0].notes)

# Note lengths and note Averages:
lengthsOfNotes = []
noteLengthsAdded = 0
for i in range (len(midi_data.instruments[0].notes)):
	lengthsOfNotes.append(midi_data.instruments[0].notes[i].end - midi_data.instruments[0].notes[i].start)
	noteLengthsAdded += midi_data.instruments[0].notes[i].end - midi_data.instruments[0].notes[i].start

averageNoteLength = noteLengthsAdded / len(midi_data.instruments[0].notes)
modeNoteLength = stats.mode(lengthsOfNotes)
print(modeNoteLength)


# Final feature is the occurence of motifs (i.e. repetitions)
# Would be good to construct a table of every note's length, pitch, and frequency (times it occurs compared to other notes)


# FINAL FEATURE ARRAY:
# number of notes, average note lengths
features = []
temp_feature_array = [0, 1, 2, 3]

temp_feature_array[0] = numNotes
temp_feature_array[1] = modeNoteLength
features += temp_feature_array
print(features)


#-------  NOTES ARRAY: ---------------------

# For a single midi file, create a 2D array, each note being represented by start, end and pitch : 
# THIS WILL BE THE TARGET(Y) 
#[[0 for x in range(columns)] for y in range(rows)]
notes_array = [[0 for x in range(3)] for y in range(len(midi_data.instruments[0].notes))]

#print(midi_data.instruments[0].notes[0].pitch)
#print(midi_data.instruments[0].notes)
for i in range (len(midi_data.instruments[0].notes)):

	notes_array[i][0] = midi_data.instruments[0].notes[i].start
	notes_array[i][1] = midi_data.instruments[0].notes[i].end
	notes_array[i][2] = midi_data.instruments[0].notes[i].pitch
	#notes_array.append(temp_note_array)

# print('new notes array')
#print(notes_array)
#s1 = music21.stream.Stream()
#s1.append(music21.note.Note('C#4', type='half'))
#print(s1[0])

#----------------------------



# FEATURE EXTRACTION:
#path = '/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/lmd_full/0/0a5e534d640455415ca1fc15bc1bb6a7.mid'
path = '/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/short.mid'
#pathDir ='/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/Midi_test'
pathDir = '/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/lmd_full/0'

# Extract features:
def get_features(midi_folder):
	file_paths = []
	files = os.listdir(midi_folder)
	midi_files = []


	for i in range(len(files[0:2])):
		try:
			#print(midi_folder+'/'+files[i])

			midi_files.append(pretty_midi.PrettyMIDI(midi_folder+'/'+files[i]))
		except:
			pass
	
	# ---------- CONSTRUCTION THE NOTES ARRAY: ------------
	#individual_notes_array = []
	notes_array = [0 for i in range(len(midi_files))]
	
	# for all midi files:
	for i in range(len(midi_files)):
		# for all the notes:
		individual_notes_array = [[0 for x in range(3)] for y in range(len(midi_files[i].instruments[0].notes))]
		#print(len(midi_files[i].instruments[0].notes))
		for j in range (len(midi_files[i].instruments[0].notes)):
			individual_notes_array[j][0] = midi_files[i].instruments[0].notes[j].start
			individual_notes_array[j][1] = midi_files[i].instruments[0].notes[j].end
			individual_notes_array[j][2] = midi_files[i].instruments[0].notes[j].pitch
			# at the end of this we would have collected all of the notes values
			# for a single MIDI file inside of the individual_notes_array
			# this array will be overwritten in the next iteration (next MIDI file) so we need to store it
		# store it:
		notes_array[i]=individual_notes_array

	# The final 3D array, all note details, for every not in every MIDI file! 
	#print(notes_array[4][0])

	# ----------- FEATURE EXTRACTION: -----------

	features = []

	# Note lengths and note Averages:
	#lengthsOfNotes = []
	#noteLengthsAdded = 0
	modes = [0 for i in range(len(midi_files))]
	for i in range(len(midi_files)):
		lengthsOfNotes = [0 for x in range(len(midi_files[i].instruments[0].notes))] 
		for j in range (len(midi_files[i].instruments[0].notes)):
			lengthsOfNotes[j]=midi_files[i].instruments[0].notes[j].end - midi_files[i].instruments[0].notes[j].start
		#print('LENGTH')
		#print(lengthsOfNotes)	
		modes[i] = stats.mode(lengthsOfNotes)
	print('mode lengths for midi files:')
	print(modes[0])
	print(modes[1])
	

	

	
	#return features #normalize_features([tempo, num_sig_changes, resolution, ts_1, ts_2])


get_features(pathDir)
