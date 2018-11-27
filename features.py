import numpy as numpy
#import pandas as pd 
import pretty_midi
import music21 # http://web.mit.edu/music21/ 
import warnings
import os

# Now load the output MIDI file into a PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI('/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/out.mid')
midi_path = '/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/Scales/CMajor.mid'
midi_path = '/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/out.mid'


# Get the MIDI data as a sequence of chroma vectors.
# And Compute the relative amount of each semitone across the entire song,
# we can use this data to calculate probable keys later
total_velocity = sum(sum(midi_data.get_chroma()))
print [sum(semitone)/total_velocity for semitone in midi_data.get_chroma()]

# Using music21 library, obtain the key:
score = music21.converter.parse(midi_path )
key = score.analyze('key')
print(key.tonic.name, key.mode)

# Obtain the length of notes
print('ONSETS :')
print(midi_data.get_onsets())

# Piano roll
print(len(midi_data.instruments[0].notes))

# Note lengths:
lengthsOfNotes = []
print('note lengths:')
for i in range (len(midi_data.instruments[0].notes)):
	print(midi_data.instruments[0].notes[i].end - midi_data.instruments[0].notes[i].start)
	lengthsOfNotes.append(midi_data.instruments[0].notes[i].end - midi_data.instruments[0].notes[i].start)
print(lengthsOfNotes)


# FEATURE EXTRACTION:
#path = '/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/lmd_full/0/0a5e534d640455415ca1fc15bc1bb6a7.mid'
path = '/Users/default/Documents/goldsmiths_year_3/creative_ml/scikit_test/short.mid'

# Extract features:
def get_features(path):

	file = pretty_midi.PrettyMIDI(path)
	print(file)

	tempo = file.get_beats()
	n = pretty_midi.note_number_to_name(96);
	roll = file.get_piano_roll(100);
	
	features = [tempo]
			#print(features)
	print(n)
	print(len(roll))
	print(roll[0])
	return features #normalize_features([tempo, num_sig_changes, resolution, ts_1, ts_2])


#get_features(path)