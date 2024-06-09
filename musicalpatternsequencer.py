"""
File: musicalpatternsequencer.py
Author: Dan O'Meara
---
A practice tool for musicians. 
Using "digital patterns" like 1235 (in C maj, C D E G),
a user can generate PDFs in musical notation of the 
digital pattern repeated across a given scale.

This is still at a prototype stage

TODO:
-Basic input (pattern, scale, tonic)
-Octave displacement issues with Lilypond notation
-Enharmonic fixes for flats/sharps
-Extention: User preview of pattern before generating full PDF
-Extended user input (fine-tuning, etc.)
-Extension: patterns repeated over chord progressions
"""

import subprocess

MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10] # natural minor
MEL_MINOR_SCALE = [0, 2, 3, 5, 7, 9, 11] # melodic minor
HARM_MINOR_SCALE = [0, 2, 3, 5, 7, 8, 11] # harmonic minor



def determine_rhyth_val(pattern):
    """
    Determines rhythmic value and holds the following information
    as elements in a list at the following index positions:
    0: the rhythmic value to use in the sequence
    1: the length of the pattern
    2:(if there is a triplet), displays the opening elements for the melody string
    3: (if there is a triplet), displays the closing elements for the melody string
    """
    rhythm_val = [8, 4, "", ""]
    rhythm_val[1] = len(pattern)

    if len(pattern) % 3 == 0:
        rhythm_val[2] = r"\tuplet 3/2 { "
        rhythm_val[3] = r" }"
    elif len(pattern) % 5 == 0:
        rhythm_val[2] = r"\tuplet 5/4 { "
        rhythm_val[3] = r" }"
    elif len(pattern) % 7 == 0:
        rhythm_val[2] = r"\tuplet 7/4 { "
        rhythm_val[3] = r" }"

    return rhythm_val


def diat_pattern_across_scale(scale, pattern):
    # Generates a melodic sequence across the scale diatonically
    new_sequence = []
    
    # Convert pattern to diatonic interval shift list indicating the 
    diatonic_interval_shifts = []

    # Calculate amount to shift each note by diatonically, relative to the first note of the pattern
    for i in range(len(pattern)):
        diatonic_interval_shift = pattern[i] - pattern[0]
        diatonic_interval_shifts.append(diatonic_interval_shift)
    
    # Make new sequence iterating the pattern on each scale degree
    for note in scale:
        for i in range(len(pattern)):
            # Finds the index in the scale of the next note to add
            next_note_index = (scale.index(note) + diatonic_interval_shifts[i]) % len(scale)
            new_sequence.append(scale[next_note_index])
        next_note_index = 0
        
    return new_sequence


def chrom_pattern_across_scale(scale, pattern):
    # Generates a chromatic sequence repeating a pattern across the scale chromatically
    # starting on each scale degree
    new_sequence = []
    for degree in scale:
        for element in pattern:
            new_sequence.append((degree + element) % 12)
        
    return new_sequence


def scale_in_key(tonic, scale):
    # Transposes scale to relevant key, starting on the tonic
    for i in range(len(scale)):
        scale[i] = (scale[i] + tonic) % 12
    return scale


def int_to_letters(sequence):
    # Converts integer notation to letter names (C, D, Eb, etc.). Defaults to flats per jazz convention.
    flats_conversion = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
    for i in range(len(sequence)):
        sequence[i] = flats_conversion[sequence[i]]
    return sequence


def make_lilypond_file(notes):
    # TODO build template with editable components for melody
    
    lilyp_header = '''\
\\version "2.24.3"

#(set-global-staff-size 17)
global = {
    \\time 4/4
    \\key c \major
    \\numericTimeSignature
}
melody = \\relative {
  \\global
\
'''

    lilyp_footer = '''\
}

\\score {
  <<
    \\new Staff  {
      \\context Voice = "vocal" { \melody }
    }
  >>
}
'''
    
    notes = "\n".join([lilyp_header, notes, lilyp_footer])

    
    
    # Writing to file
    try:
        f = open("test.ly", "w")
        f.write(notes)
        f.close()
    except:
        return False
    
    # Test: reading from the file
    f = open("test.ly", "r")
    print(f.read())
    

def run_lilypond():
    """
    Opens Lilypond with a shell command. 
    Lilypond is required, and needs to be placed in the same directory as the main program.
    It can be downloaded here (https://lilypond.org/doc/v2.25/Documentation/web/index)

    """
    filename = "test.ly"
    result = subprocess.run(["lilypond-2.24.3/bin/lilypond test.ly"], shell=True)

def notes_to_lilypond(sequence, rhythm_val):
    # Converts letters to Lilypond (LY) melody notation
    new_sequence = []
    print("Sequence to convert to Lilypond:", sequence)
    for i in range (len(sequence)):
        # Convert accidentals to "is"/"es" LY notation
        if sequence[i].endswith("b"):
            new_sequence.append(sequence[i].replace("b", "es"))
        elif sequence[i].endswith("#"):
            new_sequence.append(sequence[i].replace("#", "is"))
        else:
            new_sequence.append(sequence[i])
    
    # Convert all letters to lowercase
    new_sequence = [x.lower() for x in new_sequence]

    # Convert to a string
    sequence_string = ""

    # Add octave and rhythm value notation to first pitch
    sequence_string = str(rhythm_val[2]) + sequence_string.join(new_sequence[0] + "'" + str(rhythm_val[0]))
    print(sequence_string)

    # Add subsequent pitches
    sequence_string = sequence_string + " " + " ".join(new_sequence[1:]) + str(rhythm_val[3])

    return sequence_string

"""
Main function
"""
# TBD parameters set by user
scale = MAJOR_SCALE
tonic = 0
chrom_pattern = [0,2,4,7] # TODO: setup conversion from 1235 to this.
diat_pattern = [1, 2, 3, 6, 5]
rhythm_val = [8, 4, "", ""]

print("Tonic:", tonic)
print("Scale:", scale)
print("Pattern:", diat_pattern)

rhythm_val = determine_rhyth_val(diat_pattern)
scale = scale_in_key(tonic, scale)
sequence = diat_pattern_across_scale(scale,diat_pattern)
# sequence = chrom_pattern_across_scale(scale, chrom_pattern)
print(int_to_letters(sequence))
lilyp_string = notes_to_lilypond(sequence, rhythm_val)
print (lilyp_string)
print(make_lilypond_file(lilyp_string))
run_lilypond()