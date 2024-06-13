# Musical Pattern Sequencer

A console program that generates a PDF of melodic exercises based a user inputted scale and pattern. The program relies on the [Lilypond music scripting software](https://lilypond.org/). An online compiler of Lilypond can be found at [Hacklily](https://hacklily.org/). Note that Hacklily uses an older version of Lilypond.

In order to generate PDFs, the folder must be set up with two elements: 
 * Lilypond - just download Lilypond and place its folder the in the same directory as musicalpatternsequencer.py
 * test.ly - set up an empty text file, labeled test.ly, in the same directory

## Technical Details

To output a PDF of a given melody, the program:
* Takes in input from the user for the scale and melodic pattern to be sequenced
* Converts these to integer notation and does some calculations to generate new melodic sequence
* Converts this sequence to a music scripting language called Lilypond
* Writes this to a file so it can be compiled in Lilypond.
* Runs Lilypond from the command shell to generate a PDF.

## Packages used

* Subprocess - to run Lilypond from command shell

## Todo

* Adding modes + additional scales
* Octave displacement issues with Lilypond notation - _user cannot specify which octave they would like each note to appear; it defaults to as close as possible to the previous pitch_
* Changing paper size to better fit on phones
* Adding document metadata

## Further extensions
* Providing user with preview of pattern before generating full PDF
* Extended user input/settings (ascending/descending, choose output type - PDF, PNG, or code, fine-tuning octaves, etc.)
* Patterns repeated over chord progressions instead of scales
* GUI input
* Bundled version that copies to clipboard, then opens browser to [hacklily.org](https://hacklily.org) - _this is especially useful for web application, where command shell integration would be challenging_
