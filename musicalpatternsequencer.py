"""
File: musicalpatternsequencer.py
Author: Dan O'Meara
---
A practice tool for musicians. 
Using "digital patterns" like 1235 (in C maj, C D E G),
a user can generate PDFs in musical notation of the 
digital pattern repeated across a given scale.

This is still at a prototype stage, and a wishlist of extra features appears in README.

TODO:
-Adding modes
-Octave displacement issues with Lilypond notation
-Extension: User preview of pattern before generating full PDF
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

FLATS_CONVERSION = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
SHARPS_CONVERSION = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
KEYS_CONVERSION = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")


# ---User input-related functions---
def welcome_message():
    """
    Displays an opening message.
    """
    welcome_text = """
    ---------------------
    - MUSICAL SEQUENCER -
    ---------------------
    This program repeats a pattern of scale degrees (e.g., 1-2-3-5) starting on each note of a scale.
    This will be transposed through all twelve keys around the circle of fifths.
    """
    print(welcome_text)


def basic_input():
    """
    User inputs core elements (scale and pattern) to be sequenced 
    and returns these to the main function
    """
    user_scale, user_scale_string = input_scale()
    user_pattern = input_pattern(user_scale)

    print(user_scale_string.capitalize(), "scale:", user_scale)
    print("Pattern:", user_pattern)
    return user_scale, user_scale_string, user_pattern


def input_scale():
    """
    User inputs a scale
    Checks for valid inputs
    Returns:
    -user_scale as integer notation [list]
    -user_scale_string [string]
    """
    unkn_scale = "Hmm, I don't know that scale. "
    init_options = "Enter 'major' or 'minor': "
    min_options = "Enter 'natural minor', 'melodic minor', or 'harmonic minor: "

    valid_inputs = ALLOWED_SCALES.keys()
    print("First, let's select a scale.")
    user_scale_string = input("What type of scale would you like to use? " +
                              init_options).lower().strip()

    # Checks for valid inputs
    while user_scale_string not in valid_inputs:
        user_scale_string = input(unkn_scale + init_options).lower().strip()

    # Specifies type of minor scale and checks for valid inputs
    if user_scale_string == 'minor':
        user_scale_string = input("Which type of minor? " + min_options).lower().strip()
        while user_scale_string not in valid_inputs:
            user_scale_string = input(unkn_scale + min_options).lower().strip()

    # TBD Enable custom scale entry; use if-else structure with allowable list code below
    # elif user_scale_string == 'custom':
    #     print("Not yet implemented. Defaulting to major scale.")
    #     user_scale = ALLOWED_SCALES["major"]

    # Determine scale setup from allowable list
    user_scale = ALLOWED_SCALES[user_scale_string]
    print("\nOK, a " + str(user_scale_string) + " scale (" + str(user_scale) + ").\n")
    return user_scale, user_scale_string


def input_pattern(scale):
    """
    User enters a pattern and checks validity of entry
    Parameter: scale as integer notation [list]
    Returns: pattern as integer notation [list]
    """
    input_message = "Enter a series of scale degrees (e.g., 1 2 3 5) with spaces in-between: "
    print("Next, let's set up a pattern to be repeated across the scale.")
    print("Note that your scale has " + str(len(scale)) + " scale degrees.")
    user_input_pattern = []

    # Verify user input for 4 cases: no entry, non-int, negative int, and # greater than # in scale
    user_input_pattern = [try_int(item) for item in input(input_message).split()]
    print(user_input_pattern)
    while (not user_input_pattern or
            user_input_pattern.count(None) != 0 or
            max(user_input_pattern) > len(scale) or
            min(user_input_pattern) <= 0 or
            len(user_input_pattern) == 1):
        if not user_input_pattern: # Checks if list is empty; aka user did not input anything
            print("You haven't entered anything. Try again.")
        elif user_input_pattern.count(None) != 0: # Checks if non-int
            print ("Hmm, that's not a number. Try again.")
        elif max(user_input_pattern) > len(scale):
            print("Hmm, you've included a scale degree bigger than your scale. Try again.")
        elif min(user_input_pattern) <= 0:
            print("Hmm, scale degrees have to be positive numbers. Try again.")
        elif len(user_input_pattern) == 1:
            print("Your pattern needs more than one note. Try again.")
        user_input_pattern = [try_int(item) for item in input(input_message).split()]

    # Display pattern back to user
    print("\nOK, your pattern is " + str(user_input_pattern) + ".\n")
    return user_input_pattern


def wait_to_proceed():
    """
    Prompts the user to continue.
    Used to pause program before generating more messages.
    """
    print("Press enter to continue.")
    input("")
    print("") # Line break to aid console readability


# ---Functions for converting between formats (integer and letter)---
def try_int(value):
    """
    Tries to convert to int, and returns value as int
    If it fails, returns None as value.
    """
    try:
        int(value)
        return int(value)
    except ValueError:
        return None


def int_seq_to_letters(sequence, key_type):
    """
    Converts integer notation to letter names (C, D, Eb, etc.). 
    Defaults to flats per jazz convention, but avoids double-flat signatures
    (therefore Db and Gb are spelled as C# and F#, to avoid double flats
    in minor key signatures)
    """
    if key_type == "minor":
        for i in range(len(sequence)):
            sequence[i] = KEYS_CONVERSION[sequence[i]]
    else: 
        for i in range(len(sequence)):
            sequence[i] = FLATS_CONVERSION[sequence[i]]
    
    return sequence


# ---Functions for generating melodic sequence---
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


def get_key(name_of_scale):
    """
    Determines the type of key signature.
    Returns: key type ("major" or "minor") [string]
    """
    if name_of_scale == "major":
        return "major"
    elif "minor" in name_of_scale:
        return "minor"
    else:
        # for custom scales or added non-diatonic scales
        return "custom" # default to major


def pattern_across_scale(scale, pattern):
    """
    Generates a melodic motif played across a given scale.
    Converts pattern to diatonic interval shift list indicating 
    the number of indices to move along the scale for each note in the pattern
    Parameters:
    -scale: scale in integer notation [list]
    -pattern: pattern in diatonic scale degrees [list]
    Returns:
    -motif: motif/pattern in integer notation applied to the start of the scale [list]
    -starting_degree_shift: number of diatonic scale degrees to shift first note 
    with respect to root of scale [int]
    """

    motif = []
    diatonic_interval_shifts = []

    # Handles case for pattern that does not start on scale degree 1.
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


# ---Lilypond-related functions---
def make_seq_lilypond_string(scale_list):
    """
    Generates a string in Lilypond format for the main melodic sequence of the program.
    Uses the modal transpose feature in Lilypond
    Parameter:
    -scale_list: scale as a list of letter names in LY format
    Output: returns melody string in LY format
    """
    from_pitch = 'c'
    lilyp_staff_body = ""

    # Iterating along each note in the scale to repeat the motif
    for i in range(len(scale_list)):
        to_pitch = scale_list[i]
        lilyp_staff_body += ('\\modalTranspose ' + str(from_pitch) + " " + str(to_pitch) +
                              ' \\diatonicScale \\motif \n')

    lilyp_staff_body += "\n}" # Final line break for LY legibility

    return lilyp_staff_body


def lett_to_ly_list(melody, add_slur = False):
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
            if i == 0: # if first note in pattern
                new_melody.append("(")
            elif i == (len(pattern) - 1):
                new_melody.append(")")

    # Convert all letters to lowercase
    new_melody = [x.lower() for x in new_melody]
    return new_melody


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

    new_melody = lett_to_ly_list(melody, add_slur)

    # Convert to a string
    melody_string = ""

    # Add octave and rhythm value notation to first pitch
    melody_string = (str(rhythm_val[2]) + # tuplet header
                     melody_string.join(new_melody[0] + "'" + str(rhythm_val[0])))

    # Add subsequent pitches
    melody_string = melody_string + " " + " ".join(new_melody[1:]) + str(rhythm_val[3])

    return melody_string, new_melody


def make_lilypond_script(scale_let_seq, motif_let_seq, rhythm_val, key_qual):
    """
    Converts melodic motif to a sequence over a given scale.
    Parameters:
    -scale: scale given in standard letter name notation e.g., ['C', 'Eb', 'F#'] [list]
    -motif: melodic motif in standard letter name notation [list]
    -rhythm_val: 4-parameter list with rhythm value information for motif [list]
    -key_qual: a string with the key quality (major, minor or custom) [string]
    Output: writes changes to file test.ly
    """

    # Convert scale and motif to lilypond format
    motif_lilyp_string = notes_to_lilypond(rhythm_val, motif_let_seq, True)[0]
    scale_lilyp_string, scale_list = notes_to_lilypond(rhythm_val, scale_let_seq, False)

    lilyp_header = '\\version "2.24.3" \n\n\\language "english"\n\n#(set-global-staff-size 20)'
    lilyp_scale_pre = "diatonicScale = \\relative {"
    lilyp_motif_pre = "motif = \\relative {"

    # Generate main melody string in LY format
    lilyp_staff_melody = make_seq_lilypond_string(scale_list)

    # Generate series of transposed melodies as string in LY format
    keys = lett_to_ly_list(int_seq_to_letters(ALLOWED_PROGRESSIONS["circle of fifths"], key_qual))
    from_pitch = 'c'

    lilyp_staff_body = ""
    for key in keys:
        lilyp_staff_body += ("\n\\new Staff{\n\\key " + str(key) + " \\" + str(key_qual) +
                             "\n\\transpose " + str(from_pitch) + " " + str(key) + " {\n" +
                             lilyp_staff_melody + "}")

    lilyp_full_text = "\n".join([lilyp_header,
                                 lilyp_scale_pre, scale_lilyp_string, "}",
                                 lilyp_motif_pre, motif_lilyp_string, "}",
                                 lilyp_staff_body])
    return lilyp_full_text


def write_to_ly_file(lilypond_script, filename = 'test.ly'):
    """
    Writes text to file in the directory. 
    Defaults to filename test.ly
    """
    try:
        f = open(filename, "w", encoding="utf-8")
        f.write(lilypond_script)
        f.close()
        return "Successfully written to " + filename + "."
    except:
        return "Error writing to " + filename + "."

    # Test: reading from the file
    # f = open("test.ly", "r")
    # print(f.read())


def run_lilypond(filename = 'test.ly'):
    """
    Opens Lilypond with a shell command. 
    Lilypond is required, and needs to be placed in the same directory as the main program.
    It can be downloaded here (https://lilypond.org/doc/v2.25/Documentation/web/index)

    """
    subprocess.run(["lilypond-2.24.3/bin/lilypond " + filename], shell=True, check=False)


"""
--- Main function ---
"""

# Default parameters for testing
# scale = ALLOWED_SCALES["major"]
# tonic = 0
# pattern = [1, 2, 4, 5]
# rhythm_val = [8, 4, "", ""]

# User input
welcome_message()
scale, scale_string, pattern = basic_input()
wait_to_proceed()

# Generating basic sequence and related details
rhythm_val = determine_rhyth_val(pattern)
key_string = get_key(scale_string)
motif_int_seq, motif_start_shift = pattern_across_scale(scale, pattern)

# Converting relevant melodies in integer notation to letter names
motif_let_seq = int_seq_to_letters(motif_int_seq, key_string)
scale_let_seq = int_seq_to_letters(scale, key_string)

# Generating Lilypond script in test.ly
lilypond_script = make_lilypond_script(scale_let_seq, motif_let_seq, rhythm_val, key_string)
write_to_ly_file(lilypond_script)

# Launching Lilypond and generating PDF as test.pdf
run_lilypond()