"""
File: musicalpatternsequencer.py
Author: Dan O'Meara
---
A practice tool for musicians. 
Using "digital patterns" like 1235 (in C maj, C D E G),
a user can generate PDFs in musical notation of the 
digital pattern repeated across a given scale.

This is still at a prototype stage, and a wishlist of extra features appears below.

TODO:
-Adding modes
-Octave displacement issues with Lilypond notation
-Minor key signatures
-(Backend) Add default values to functions
-Enharmonic fixes for flats/sharps
-Extention: User preview of pattern before generating full PDF
-Extended user input/settings (ascending/descending, 
choose output type - PDF, PNG, or code, fine-tuning, etc.)
-Extension: patterns repeated over chord progressions
-Extension: GUI input
-Extension: bundled version that copies to clipboard, then opens browser to hacklily.org
"""
import subprocess

ALLOWED_SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "natural minor": [0, 2, 3, 5, 7, 8, 10],
    "melodic minor": [0, 2, 3, 5, 7, 9, 11],
    "harmonic minor": [0, 2, 3, 5, 7, 8, 11],
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

ALLOWED_PROGRESSIONS = {
    "circle of fifths":[0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]
}

MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10] # natural minor
MEL_MINOR_SCALE = [0, 2, 3, 5, 7, 9, 11] # melodic minor
HARM_MINOR_SCALE = [0, 2, 3, 5, 7, 8, 11] # harmonic minor
OCTATONIC_01_SCALE = [0, 1, 3, 4, 6, 7, 9, 10] # octatonic / half-whole diminished scale
OCTATONIC_02_SCALE = [0, 2, 3, 5, 6, 8, 9, 10] # octatonic / whole-half diminished scale
WHOLE_TONE_SCALE = [0, 2, 4, 6, 8, 10]

FLATS_CONVERSION = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
SHARPS_CONVERSION = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

def basic_input():
    """
    User inputs core elements (scale and pattern) to be sequenced 
    and returns these to the main function
    """
    user_scale = input_scale()
    user_pattern = input_pattern(user_scale)
    print("Press enter to continue.")
    input("")
    return user_scale, user_pattern
    

def welcome_message():
    # Displays an opening message:
    welcome_text = """
    ---------------------
    - MUSICAL SEQUENCER -
    ---------------------
    This program repeats a pattern of scale degrees (e.g., 1-2-3-5) starting on each note of a scale.
    This will be transposed through all twelve keys around the circle of fifths.
    """
    print(welcome_text)
    


def input_scale():
    # User inputs a scale
    valid_inputs = ALLOWED_SCALES.keys()
    user_scale_string = input("First, let's select a scale. What type of scale would you like to use? Enter 'major' or 'minor': ").lower().strip()
    
    # Checks for valid inputs
    while user_scale_string not in valid_inputs:
        user_scale_string = input("Hmm, I don't know that scale. Enter 'major' or 'minor': ").lower()
    
    # Specifies type of minor scale
    if user_scale_string == 'minor':
        user_scale_string = input("Which type of minor? Enter 'natural minor', 'melodic minor', or 'harmonic minor: ")
        while user_scale_string not in valid_inputs:
            user_scale_string = input("Hmm, I don't know that scale. Enter 'natural minor', 'melodic minor', or 'harmonic minor: ").lower()
    
    # TBD Enable custom scale entry; use if-else structure with allowable list code below
    # elif user_scale_string == 'custom':
    #     print("Not yet implemented. Defaulting to major scale.")
    #     user_scale = ALLOWED_SCALES["major"]

    # Determine scale setup from allowable list
    user_scale = ALLOWED_SCALES[user_scale_string]
    print("\nOK, a " + str(user_scale_string) + " scale (" + str(user_scale) + ").\n")
    return user_scale


def input_pattern(scale):
    """
    User enters a pattern
    """
    input_message = "Enter a series of scale degrees (e.g., 1 2 3 5) with spaces in-between: "
    print("Next, let's set up a pattern to be repeated across the scale.")
    print("Note that your scale has " + str(len(scale)) + " scale degrees.")
    user_input_pattern = []
    
    # Verify user input for three cases: non-int, negative int, and # greater than # in scale
    user_input_pattern = [try_int(item) for item in input(input_message).split()]
    while user_input_pattern.count(None) != 0 or max(user_input_pattern) > len(scale) or min(user_input_pattern) <= 0:
        if max(user_input_pattern) > len(scale):
            print("Hmm, you've included a scale degree bigger than your scale. Try again.")
        elif min(user_input_pattern) <= 0:
            print("Hmm, scale degrees have to be positive numbers. Try again.")
        user_input_pattern = [try_int(item) for item in input(input_message).split()]
    
    # Display pattern back to user
    print("\nOK, your pattern is " + str(user_input_pattern) + ".\n")
    return user_input_pattern


def try_int(value):
    # Tries to convert to int; if it fails, displays error and returns None as value.
    try:
        int(value)
        return int(value)
    except ValueError:
        print ("Hmm, that's not a number. Try again.")


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


def pattern_across_scale(scale, pattern):
    """
    Generates a melodic motif played across a given scale
    Parameters:
    -scale: scale in integer notation [list]
    -pattern: pattern in diatonic scale degrees [list]
    Returns:
    -motif: motif/pattern in integer notation applied to the start of the scale [list]
    -starting_degree_shift: number of diatonic scale degrees to shift first note with respect to root of scale [int]
    """
    
    motif = []

    # Convert pattern to diatonic interval shift list indicating the number of indices to move along the scale
    # with each note in the pattern
    diatonic_interval_shifts = []

    # Edge case for pattern that does not start on 1.
    starting_degree_shift = determine_start_deg_shift(pattern)

    # Calculate amount to shift each note by diatonically, relative to the first note of the pattern
    for i in range(len(pattern)):
        diatonic_interval_shift = pattern[i] - pattern[0] + starting_degree_shift
        diatonic_interval_shifts.append(diatonic_interval_shift)
    
    # For debugging, check correct (comment out if not needed)
    # print("pattern_across_scale / diatonic_interval_shifts = ", diatonic_interval_shifts)

    # Make first iteration of the pattern, applied to the scale
    for i in range(len(pattern)):
        # Finds the index in the scale of the next note to add
        next_note_index = (scale[0] + diatonic_interval_shifts[i]) % len(scale)
        motif.append(scale[next_note_index])
        next_note_index = 0

    return motif, starting_degree_shift


def determine_start_deg_shift(pattern):
    """
    Determines how much to shift the start of the pattern from the root of the scale.
    Handles cases where the pattern does not start on the first scale degree.
    Input parameter = pattern as list in diatonic intervals, e.g., [1, 2, 3, 5]
    Returns = starting degree shift as an integer, reflected as a diatonic interval
    """
    starting_degree_shift = 0
    if pattern[0] != 0:
        starting_degree_shift = pattern[0] - 1
    
    return starting_degree_shift
    

def diat_pattern_across_scale(scale, pattern):
    # Generates a melodic sequence across the scale diatonically
    new_sequence = []
    
    # Convert pattern to diatonic interval shift list indicating the 
    diatonic_interval_shifts = []

    # Edge case for pattern that does not start on 1.
    starting_degree_shift = 0
    if pattern[0] != 0:
        starting_degree_shift = pattern[0] - 1

    # Calculate amount to shift each note by diatonically, relative to the first note of the pattern
    for i in range(len(pattern)):
        diatonic_interval_shift = pattern[i] - pattern[0] + starting_degree_shift
        diatonic_interval_shifts.append(diatonic_interval_shift)
    
    # For debugging, check correct (comment out if not needed)
    # print("diat_pattern_across_scale / diatonic_interval_shifts = ", diatonic_interval_shifts)

    # Make new sequence iterating the pattern on each scale degree
    for note in scale:
        for i in range(len(pattern)):
            # Finds the index in the scale of the next note to add
            next_note_index = (scale.index(note) + diatonic_interval_shifts[i]) % len(scale)
            new_sequence.append(scale[next_note_index])
        next_note_index = 0

    # For debugging, check correct (comment out if not needed)
    # print("diat_pattern_across_scale / diatonic_interval_shifts = ", diatonic_interval_shifts)
    return new_sequence


def chrom_pattern_across_scale(scale, pattern):
    # Generates a chromatic sequence repeating a pattern across the scale chromatically
    # starting on each scale degree
    new_sequence = []
    for degree in scale:
        for element in pattern:
            new_sequence.append((degree + element) % 12)
        
    return new_sequence


def int_seq_to_letters(sequence):
    # Converts integer notation to letter names (C, D, Eb, etc.). Defaults to flats per jazz convention.
    for i in range(len(sequence)):
        sequence[i] = FLATS_CONVERSION[sequence[i]]
    return sequence


def letter_to_int(note_as_letter):
    """
    Converts an individual note, given in letter format (C, Eb, F#, etc.) to integer notation.
    Returns non-valid notes (e.g., ".", "R", "?") as None.
    """
    note_as_letter = note_as_letter.capitalize()
    try:
        if note_as_letter.endswith("#"):
            note_as_int = SHARPS_CONVERSION.index(note_as_letter)
        else:
            note_as_int = FLATS_CONVERSION.index(note_as_letter)
        return note_as_int
    except ValueError:
        return None


def letter_seq_to_int(sequence_as_letters):
    # Converts a sequence of letters to integer notation
    sequence_as_ints = []
    for i in range(len(sequence_as_letters)):
       sequence_as_ints.append(letter_to_int(sequence_as_letters[i]))
    return sequence_as_ints

    # for i in range(len(sequence_as_letters)):
    #     if sequence_as_letters[i].endswith("#"):
    #         sequence_as_ints.append(SHARPS_CONVERSION.index(sequence_as_letters[i]))
    #     else:
    #         sequence_as_ints.append(FLATS_CONVERSION.index(sequence_as_letters[i]))
            

def make_lilypond_script(scale, motif, motif_start_shift, rhythm_val):
    """
    Converts melodic motif to a sequence over a given scale.
    Parameters:
    -scale: scale given in standard letter name notation e.g., ['C', 'Eb', 'F#'] [list]
    -motif: melodic motif in standard letter name notation [list]
    -motif_start_shift: for motifs starting not on 1, specifies how far to shift motif along scale
    -rhythm_val: 4-parameter list with rhythm value information for motif
    Output: writes changes to file test.ly
    """

    # Convert scale and motif to lilypond format
    motif_lilyp_string, motif_list = notes_to_lilypond(rhythm_val, motif_let_seq, True)
    scale_lilyp_string, scale_list = notes_to_lilypond(rhythm_val, scale_let_seq, False)

    lilyp_header = '\\version "2.24.3" \n\n\\language "english"\n\n#(set-global-staff-size 20)'
    lilyp_scale_pre = "diatonicScale = \\relative {"
    lilyp_motif_pre = "motif = \\relative {"

    # Generate melody string in LY format
    lilyp_staff_melody = make_seq_lilypond_string(motif_list, motif_start_shift, scale_list)

    # Generate series of transposed melodies as string in LY format
    key_qual = "major" # Placeholder; will be determined functionally
    keys = convert_to_ly_accid(int_seq_to_letters(ALLOWED_PROGRESSIONS["circle of fifths"]), False)
    from_pitch = 'c'
    
    lilyp_staff_body = ""
    for key in keys:
        lilyp_staff_body += "\n\\new Staff{\n\key " + str(key) + " \\" + str(key_qual) + "\n\\transpose " + str(from_pitch) + " " + str(key) + " {\n" + lilyp_staff_melody + "}"
    
    lilyp_full_text = "\n".join([lilyp_header, lilyp_scale_pre, scale_lilyp_string, "}", lilyp_motif_pre, motif_lilyp_string, "}", lilyp_staff_body])
    return lilyp_full_text

def write_to_ly_file(lilypond_script, filename = 'test.ly'):
    """
    Writes text to file in the directory. 
    Defaults to filename test.ly
    """
    try:
        f = open(filename, "w")
        f.write(lilypond_script)
        f.close()
        return "Successfully written to " + filename + "."
    except:
        return "Error writing to " + filename + "."
    
    # Test: reading from the file
    # f = open("test.ly", "r")
    # print(f.read())

def make_seq_lilypond_string(motif_list, motif_start_shift, scale_list):
    """
    Generates a string in Lilypond format for the main melodic sequence of the program.
    Uses the modal transpose feature in Lilypond
    Parameters:
    -motif_string: melodic motif as string of letter names in LY format
    -motif_list: melodic motif as a list of letter names in LY format
    -motif_start_shift: for motifs starting not on 1, specifies how far to shift motif along scale diatonically
    -scale_string: scale as a string of letter names in LY format
    -scale_list: scale as a list of letter names in LY format
    Output: returns melody string in LY format
    """
    from_pitch = 'c'
    lilyp_staff_body = ""

    # Iterating along each note in the scale to repeat the motif
    for i in range(1, len(scale_list)):
        to_pitch = scale_list[(i - 1)]
        lilyp_staff_body += '\\modalTranspose ' + str(from_pitch) + " " + str(to_pitch) + ' \\diatonicScale \\motif \n'
    
    lilyp_staff_body += "\n}" # Final line break for LY legibility

    return lilyp_staff_body
    

def run_lilypond(filename = 'test.ly'):
    """
    Opens Lilypond with a shell command. 
    Lilypond is required, and needs to be placed in the same directory as the main program.
    It can be downloaded here (https://lilypond.org/doc/v2.25/Documentation/web/index)

    """
    result = subprocess.run(["lilypond-2.24.3/bin/lilypond " + filename], shell=True)


def notes_to_lilypond(rhythm_val, melody, add_slur = False):
    """
    Converts melody in letter notation to Lilypond (LY) melody notation
    Parameters:
    -rhythm_val list with 4 elements at different indices (see comments for related function)
    -melody given in list in standard letter name notation (e.g., ['C', 'Eb', 'F#'])
    -add_slur Boolean, which will be True if the melody should be grouped together in a slur
    (this defaults to False)
    Returns:
    -melody as a string in Lilypond format, including rhythm headers
    -melody as a list, with entries in Lilypond format
    """

    new_melody = []
    
    new_melody = convert_to_ly_accid(melody, add_slur)

    # Convert to a string
    melody_string = ""

    # Add octave and rhythm value notation to first pitch
    melody_string = str(rhythm_val[2]) + melody_string.join(new_melody[0] + "'" + str(rhythm_val[0]) )

    # Add subsequent pitches
    melody_string = melody_string + " " + " ".join(new_melody[1:]) + str(rhythm_val[3])

    return melody_string, new_melody


def convert_to_ly_accid(melody, add_slur = False):
    """
    Input: melody as list of letter names in standard format
    Output: melody as list of letter names in LY format
    """
    new_melody = []

    for i in range (len(melody)):
        # Convert accidentals to "f"/"s" LY notation
        # Note that this requires LY language to be set to "english"
        if melody[i].endswith("b"):
            new_melody.append(melody[i].replace("b", "f"))
        elif melody[i].endswith("#"):
            new_melody.append(melody[i].replace("#", "s"))
        else:
            new_melody.append(melody[i])

        # Add parentheses for slurs
        # TODO convert this to an index insert instead of append to make it its own module
        if add_slur == True:
            if (i == 0): # if first note in pattern
                new_melody.append("(")
            elif i == (len(pattern) - 1):
                new_melody.append(")")
        
    # Convert all letters to lowercase
    new_melody = [x.lower() for x in new_melody]
    return new_melody


# --- Main function ---

# Default parameters for testing
# scale = ALLOWED_SCALES["major"]
# tonic = 0
# pattern = [1, 2, 4, 5]
# rhythm_val = [8, 4, "", ""]

# User input
welcome_message()
scale, pattern = basic_input()

# Transposing scale
print("Scale:", scale)
print("Pattern:", pattern)

# Generating basic sequence and related details
rhythm_val = determine_rhyth_val(pattern)
motif_int_seq, motif_start_shift = pattern_across_scale(scale, pattern)

# Converting relevant melodies in integer notation to letter names
motif_let_seq = int_seq_to_letters(motif_int_seq)
scale_let_seq = int_seq_to_letters(scale)

# Generating Lilypond script in test.ly
lilypond_script = make_lilypond_script(scale_let_seq, motif_let_seq, motif_start_shift, rhythm_val)
write_to_ly_file(lilypond_script)

# Launching Lilypond and generating PDF as test.pdf
run_lilypond()