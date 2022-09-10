A Python script for OBS to control the text contents of multiple text sources
using only one text file. See #Protocol for details about the text file.

# Installation
1. Make sure that you have at least Python 3+ (for OBS versions older than v28,
only Python 3.6.x is supported).
2. In OBS, go to Tools > Scripts.
3. In the Python Settings tab, set your python installation path.
4. In the Scripts tab, add the master_text_source_file.py.

# Usage
1. Set the file path for the text file that will be read.
2. Make sure that you have sources that have the same name as those declared in your text file
3. You may check the Script Log if some sources are not found or if there are other errors.

# Protocol
The text file should contain a source name (case-sensitive and whitespace-sensitive)
enclosed in angle brackets in a line followed by a line break. The following lines up to the next
declaration of a scene name will be used as the text for the source. A blank line
before the next source name is allowed, but extra blank lines will not be removed.
It is also fine if you do not want to put a blank line before the next source.
Source names that are used should be text sources.

An example.txt is provided.

# Contact Me
Although there is a discussion tab in these forums, I would see your message
faster if you ping me (@CodeYan) in the [OBS Discord server](https://discord.gg/obsproject),
in #plugins-and-tools. Please do report bugs or if there are features you'd like
to be added.
