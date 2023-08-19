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

Here's an example of what the text file may look like, having "Display Name", "Description", "Additional", and "Greeting" as text source names:
```
<Display Name>
CodeYan

<Description>
This is a Python script that automates updating multiple text source files using
only one file.

Source names should be enclosed in angle brackets (e.g. <My Text Source>) on a line without any other characters.
As you can see, even if I put <My Text Source> in the contents, it will not be
detected as a source name. It is space-sensitive, so if your source has spaces at the start or end, be sure to include them.

If I put 3 blank lines before the next source, only 2 blank lines will be included.



<Additional>
It is also fine to not have blank lines before the next source name if you prefer.
<Greeting>
Thank you!

```

# Contact Me
Although there is a discussion tab in these forums, I would see your message
faster if you ping me (@CodeYan) in the [OBS Discord server](https://discord.gg/obsproject),
in #plugins-and-tools. Please do report bugs or if there are features you'd like
to be added.
