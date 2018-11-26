import numpy as numpy
#import pandas as pd 
import pretty_midi
import warnings
import os

# for plotting
import mir_eval.display
import librosa.display
import matplotlib.pyplot as plt


# IAC STUFF:
import time 
import rtmidi
import time

#midiout = rtmidi.MidiOut()

midiin = rtmidi.MidiIn()
available_ports = midiin.get_ports()
print(available_ports[0])
midiin.open_port(0)

#midiin.get_message()
done = False
pattern = []

counter = 0

# Bring in the rtMidi readings:
while counter < 50:
	#print(midiin.get_message())
	time.sleep(0.1)
	counter +=1

	pattern.append(midiin.get_message())

	# Observations:
	# 64 seems to mean note-off 
	# I was wondering what the minimum time.sleep() value
	# I could have before the program started missing out notes
	# turns out that it still catches 1/16th notes at time.sleep(0.2)

	# 0 was categorised C-1, when it should have been C-2
	# 127 was categorised as G9, when should have been G8.
	#get_message() consists of : # channel number, note value, velocity 

print('----')
print('OUTPUT:')
print(pattern)

# Remove instance of None:
midiVals = []

for val in pattern:
	if val is not None:
		midiVals.append(val)

# to access whole first index:
#print(midiVals[0])
# to access time:
#print(midiVals[0][1])
# to access the channel, note value and velocity:
#print(midiVals[0][0])
# to access velocity:
#print(midiVals[0][0][2])




# Get the total length, but also save the incrementing time values in an array for later reference:
timesArray = []
timeCount = 0.0
for i in range (0, len(midiVals)):
	timeCount += midiVals[i][1]
	timesArray.append(timeCount)
print('TIME COUNT:')
print(timeCount)
print('Time Array')
print(timesArray)



# if the first value is an end-note, delete it:
if midiVals[0][0][2] == 64:
	print('BAD Start')
	print(midiVals[0])
	del midiVals[0]

# if the last value is not an end-note, delete it:
if midiVals[len(midiVals)-1][0][2] is not 64:
	print('BAD Ending')
	print(midiVals[len(midiVals)-1])
	del midiVals[0]

print('----')
print('CLEANED OUTPUT:')
print(midiVals)

# Reconstruct the MIDI pattern using pretty_midi:
pm = pretty_midi.PrettyMIDI(initial_tempo=120)
testPattern = pretty_midi.PrettyMIDI()
inst = pretty_midi.Instrument(program=42, is_drum=False, name='pattern')
pm.instruments.append(inst)

#for val in midiVals:
#for val in midiVals[0::2]:
for i in range(0, len(midiVals)):
	if i%2==0:
		print(i)
		print(midiVals[i])
		startT = timesArray[i]
		endT = timesArray[i+1]
		print('start: ')
		print(startT)
		print('end: ')
		print(endT)
		note = pretty_midi.Note(velocity = midiVals[i][0][2], pitch=midiVals[i][0][1], start=startT, end= endT  )
		inst.notes.append(note)
		print(note)

print("results")
print(pm)

testPattern.instruments.append(inst)
testPattern.write('out.mid')

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