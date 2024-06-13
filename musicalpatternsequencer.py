"""
File: musicalpatternsequencer.py
Author: Dan O'Meara
---
A practice tool for musicians. 
Using "digital patterns" like 1235 (in C maj, C D E G),a user can generate PDFs 
in musical notation of the digital pattern repeated across a given scale.

This is still at a prototype stage, and a wishlist of extra features appears in README.

TODO:
-Test for very long patterns and how this affects layout
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
    Returns:
    -user_scale: scale in letter format [list]
    -user_scale_name: name of scale [string]
    -user_pattern: scale degree pattern [list]
    -settings: advanced settings [dict]
    """
    user_scale, user_scale_name = input_scale()
    user_pattern = input_pattern(user_scale)
    settings = advanced_settings()

    print(user_scale_name.capitalize(), "scale:", user_scale)
    print("Pattern:", user_pattern)
    return user_scale, user_scale_name, user_pattern, settings


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
    min_options = "Enter 'natural minor', 'melodic minor', or 'harmonic minor': "

    init_valid_inputs = ALLOWED_SCALES.keys()
    min_valid_inputs = ["natural minor", "melodic minor", "harmonic minor"]
    print("First, let's select a scale.")

    # Checks for valid inputs
    user_scale_string = check_input_valid("What type of scale would you like to use? " +
                      init_options, init_valid_inputs, unkn_scale)

    # Specifies type of minor scale and checks for valid inputs
    if user_scale_string == 'minor':
        user_scale_string = check_input_valid("Which type of minor? " + min_options,
                                              min_valid_inputs, unkn_scale)

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


def advanced_settings():
    """
    User inputs advanced settings.
    Returns settings [dict]
    """
    valid_inputs = ["y", "n"]

    # Sets default settings
    settings = {
        "modes" : False
    }
    enter_settings = check_input_valid("Enter advanced settings (y/n)? ", valid_inputs)
    if enter_settings == "n":
        return settings
    else:
        print("\n" + "---Advanced settings---" + "\n"
            )

        settings["modes"] = check_input_valid("Generate all modes of scale (y/n)? ", valid_inputs)

        # Convert to bools
        for option in settings:
            if settings[option] == "y":
                settings[option] = True
            else:
                settings[option] = False

        print("---") # Section separator for clarity
        return settings


def check_input_valid(prompt, valid_values, error_message = "Invalid input. Try again." + "\n"):
    """
    Checks if user input is within 
    Note that this does not display specific error messages,
    so it is best used for generic cases.
    Parameters:
    -prompt: display message to prompt input [string]
    -valid_values: valid entries [list]
    """
    entry = input(prompt).strip().lower()
    while entry not in valid_values:
        print(error_message)
        entry = input(prompt).strip().lower()
    return entry


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
    Returns:
    -new_sequence in letter notation [list]
    """
    new_sequence = []
    if key_type == "minor":
        for note in sequence:
            new_sequence.append(KEYS_CONVERSION[note])
    else:
        for note in sequence:
            new_sequence.append(FLATS_CONVERSION[note])

    return new_sequence


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


def pattern_on_scale(scale, pattern):
    """
    Applies the scale-degree pattern to the scale.
    Converts pattern to diatonic interval shift list indicating 
    the number of indices to move along the scale for each note in the pattern.
    Parameters:
    -scale: scale in integer notation [list]
    -pattern: pattern in diatonic scale degrees [list]
    Returns:
    -motif: motif/pattern in integer notation applied to the start of the scale [list]
    """

    motif = []
    diatonic_interval_shifts = []

    # Handles case for pattern that does not start on scale degree 1.
    starting_degree_shift = determine_start_deg_shift(pattern)

    # Calculate amount to shift each note by diatonically, relative to the first note of the pattern
    for i in range(len(pattern)):
        diatonic_interval_shift = pattern[i] - pattern[0] + starting_degree_shift
        diatonic_interval_shifts.append(diatonic_interval_shift)

    # Make first iteration of the pattern, applied to the scale
    for i in range(len(pattern)):
        # Finds the index in the scale of the next note to add
        next_note_index = (scale[0] + diatonic_interval_shifts[i]) % len(scale)
        motif.append(scale[next_note_index])
        next_note_index = 0

    return motif


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


def generate_modes(scale):
    """
    Generates modes of a given scale
    Parameter: 
    -scale in integer notation [list]
    Returns:
    -modes in integer notation [list of lists]
    """
    all_modes = []
    next_mode = scale[:] # Makes a copy of list to avoid overwrite
    for note in scale:
        all_modes.append(next_mode)
        next_mode = modal_rotation(next_mode[:]) # Makes a copy of list to avoid overwrite
    return all_modes


def modal_rotation(scale):
    """
    Rotate scale to start on next mode
    Parameters:
    -ly_scale: scale in any format (integer, letter, Lilypond) [list]
    Returns rotated scale on next mode in same format [list]
    """
    first_note = scale.pop(0)
    scale.append(first_note)
    return scale


# ---Lilypond-related conversion functions---
def ly_scale_to_sequence(scale):
    """
    Generates a string in Lilypond format for the main melodic sequence of the program.
    Uses the modal transpose feature in Lilypond.
    Parameter:
    -scale_list: scale as letter names in LY format [list]
    Output: returns melody string in LY format [string]
    """
    from_pitch = 'c'
    lilyp_single_seq = ""

    # Iterating along each note in the scale to repeat the motif
    for note in scale:
        to_pitch = note
        lilyp_single_seq += ('\\modalTranspose ' + str(from_pitch) + " " + str(to_pitch) +
                              ' \\diatonicScale \\motif \n')

    lilyp_single_seq += "\n}" # Final line break for LY legibility

    return lilyp_single_seq


def lett_list_to_ly_list (melody):
    """
    Turns a given melody (in list, letter/LY format) into a list in Lilypond format
    Can be applied repeatedly as a check without changing LY format
    Parameters: melody as letter names in standard/LY letter format [list]
    Output: melody as LY format [list]
    """
    new_melody = []

    for note in melody:
        new_melody.append(lett_to_ly(note))

    return new_melody


def ly_add_slur(melody):
    """
    Adds LY slur notation to a given list
    Parameter:
    -melody: a melody in LY notation [list]
    Returns:
    -melody in LY notation with slurs [list]  
    """
    new_melody = melody
    new_melody.insert(1, "(")
    new_melody.append(")")
    return new_melody


def ly_to_lett(note):
    """
    Converts a given note from Lilypond letter format to standard letter format
    E.g., "bf" -> "Bb"
    Can be repeatedly applied without issues.
    Parameter: note in LY format ("bf") [string]
    Returns converted note in standard letter ("Bb") [string]
    """
    note = note.capitalize()
    note = note.replace("f", "b")
    note = note.replace("s", "#")
    return note


def lett_to_ly(note):
    """
    Converts a given note from standard letter format to Lilypond letter format
    E.g., "Bb" -> "bf"
    Parameter: note in standard or LY letter format ("Bb") [string]
    Returns converted note in LY format ("bf") [string]
    """
    note = note.capitalize() # Added element to handle LY input
    if note.endswith("b") and note != "b":
        note = note.replace("b", "f")
    note = note.replace("#", "s")
    note = note.lower()
    return note


def ly_note_to_ly_text(note):
    """
    Converts ly format to ly markup text format
    Parameter: note in ly note format [string]
    Returns: text in ly text format[string]
    """
    note = note.capitalize() # Safeguard for LY input
    if note.endswith("s"):
        new_text = "\\concat{" + note.replace("s","") + "\\super\\sharp}"
    elif note.endswith("f"):
        new_text = "\\concat{" + note.replace("f","") + "\\super\\flat}"
    else:
        new_text = note
    return new_text


#---Functions for compiling Lilypond string---
def ly_list_to_melody(rhythm_val, melody):
    """
    Converts list in LY notation to Lilypond (LY) melody notation string
    Parameters:
    -rhythm_val list with 4 elements at different indices (see comments for related function) [list]
    -melody given in LY letter name notation (e.g., ['c', 'ef', 'fs']) [list]
    Returns:
    -melody as a string in Lilypond format, including rhythm headers [string]
    """

    # Initialize string
    melody_string = ""

    # Add octave and rhythm value notation to first pitch (plus tuplet header if appl.)
    melody_string = (str(rhythm_val[2]) +
                     melody_string.join(melody[0] + "'" + str(rhythm_val[0])))

    # Add subsequent pitches (and tuplet header if appl.)
    melody_string = melody_string + " " + " ".join(melody[1:]) + str(rhythm_val[3])

    return melody_string


def make_ly_script(scale_let_seq, motif_let_seq, rhythm_val, key_sig_qual, name_of_scale, settings):
    """
    Converts melodic motif to a sequence over a given scale.
    Parameters:
    -scale: scale given in standard letter name notation e.g., ['C', 'Eb', 'F#'] [list]
    -motif: melodic motif in standard letter name notation [list]
    -rhythm_val: 4-parameter list with rhythm value information for motif [list]
    -name_of_scale: the full name of the scale (e.g., "natural minor") [string]
    -key_sig_qual: a string with the key signature quality (major, minor or custom) [string]
    Output: writes changes to file test.ly
    """

    # Convert scale and motif to lilypond format (as lists)
    motif_ly_list = lett_list_to_ly_list(motif_let_seq)
    scale_ly_list = lett_list_to_ly_list(scale_let_seq)
    ly_add_slur(motif_ly_list)

    # Convert ly lists to melody strings
    motif_lilyp_string = ly_list_to_melody(rhythm_val, motif_ly_list)
    scale_lilyp_string = ly_list_to_melody(rhythm_val, scale_ly_list)

    lilyp_header = '\\version "2.24.3" \n\n\\language "english"\n\n#(set-global-staff-size 20)'
    lilyp_scale_pre = "diatonicScale = \\relative {"
    lilyp_motif_pre = "motif = \\relative {"

    # Generate main melodic sequence string in LY format
    lilyp_staff_melody = ly_scale_to_sequence(scale_ly_list)

    # Initialize staff string (for all melodic components)
    lilyp_staff_body = ""

    # Generating keys to transpose over
    keys = lett_list_to_ly_list(int_seq_to_letters(ALLOWED_PROGRESSIONS["circle of fifths"],
                           key_sig_qual))
    from_pitch = 'c' 

    # Transpose to all 12 keys
    for key in keys:

        # Checks whether to print modes
        if settings["modes"]:

            # Generate modes of scale
            modes_ly_list = generate_modes(scale_ly_list)

            # Repeating sequence across all modes of scale
            for i, mode in enumerate(modes_ly_list):
                # Generate melody string
                mode_lilyp_string = ly_list_to_melody(rhythm_val, mode)
                lilyp_mode_melody = ly_scale_to_sequence(mode)

                # Add text, key sig, and melody to body string
                lilyp_staff_body += ("\\markup {" + str(ly_note_to_ly_text(key)) + " " +
                                     str(name_of_scale) + "}\n" +
                                     "\\markup \\italic {" + "Mode " + str(i + 1) + "}\n" +
                                     lilyp_scale_pre + mode_lilyp_string + "}" +
                                     "\n\\new Staff{\n\\key " + str(key) +
                                     " \\" + str(key_sig_qual) +
                                     "\n\\transpose " + str(from_pitch) + " " + str(key) + " {\n" +
                                     lilyp_mode_melody + "}\n")

            lilyp_staff_body += "\\pageBreak\n\n" # Page break between keys

        # If modes is not True, just prints in all keys
        else:
            lilyp_staff_body += ("\\markup {" + ly_note_to_ly_text(key) + " " +
                                 str(name_of_scale) + "}\n" +
                                 lilyp_scale_pre + scale_lilyp_string + "}" +
                                "\n\\new Staff{\n\\key " + str(key) + " \\" + str(key_sig_qual) +
                                "\n\\transpose " + str(from_pitch) + " " + str(key) + " {\n" +
                                lilyp_staff_melody + "}")

    # Compiles final string with all elements
    lilyp_full_text = "\n".join([lilyp_header,
                                 lilyp_motif_pre, motif_lilyp_string, "}",
                                 lilyp_staff_body])

    return lilyp_full_text


#---Functions to produce PDF---
def write_to_ly_file(lilypond_script, filename = 'test.ly'):
    """
    Writes text to file in the directory. 
    Defaults to filename test.ly
    """
    try:
        f = open(filename, "w", encoding="utf-8")
        try:
            f.write(lilypond_script)
            f.close()
            print("Successfully written to " + filename + ".\n")
        except (IOError, OSError):
            print ("Error writing to " + filename + ".")
    except (FileNotFoundError, NameError, PermissionError, OSError):
        return "Error opening " + filename + "."


def run_lilypond(filename = 'test.ly'):
    """
    Opens Lilypond with a shell command. 
    Lilypond is required, and needs to be placed in the same directory as the main program.
    It can be downloaded here (https://lilypond.org/doc/v2.25/Documentation/web/index)

    """
    subprocess.run(["lilypond-2.24.3/bin/lilypond " + filename], shell=True, check=False)

#---Main function---
def main():
    """
    Main function.
    Includes default parameters at the top for testing.
    """

    # Default parameters for testing
    # scale = ALLOWED_SCALES["major"]
    # pattern = [1, 2, 4, 5]
    # rhythm_val = [8, 4, "", ""]

    # User input
    welcome_message()
    scale, name_of_scale, pattern, settings = basic_input()
    wait_to_proceed()

    # Generating basic sequence and related details
    rhythm_val = determine_rhyth_val(pattern)
    key_sig_qual = get_key(name_of_scale)
    motif_int_seq = pattern_on_scale(scale, pattern)

    # Converting relevant melodies in integer notation to letter names
    motif_let_seq = int_seq_to_letters(motif_int_seq, key_sig_qual)
    scale_let_seq = int_seq_to_letters(scale, key_sig_qual)

    # Generating Lilypond script in test.ly

    lilypond_script = make_ly_script(scale_let_seq, motif_let_seq, rhythm_val,
                                     key_sig_qual, name_of_scale, settings)
    write_to_ly_file(lilypond_script)

    # Launching Lilypond and generating PDF as test.pdf
    run_lilypond()


if __name__ == '__main__':
    main()
