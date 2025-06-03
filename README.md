# desktop-pet
A simple desktop pet application based on PySide6/Qt.

## Setup
1. Install [Python](https://www.python.org/downloads/)
2. Download the source code.
3. Open <b>Command Prompt/Terminal</b> in the project directory.
4. Install requirements. ```pip install -r ./requirements.txt```
5. Prepare your animation images (a GIF file or sequences of image) and put into <b>frames</b> folder.
6. Config your animation files in <b>app.py</b>.
    - GIF
        ```
        sequenceData = SequenceData(["./frames/my.gif"],"gif")
        ```
    - Sequences of Images
        ```
        sequenceData = SequenceData([
            "./frames/1.png",
            "./frames/2.png",
            "./frames/3.png",
            "./frames/4.png",
            "./frames/5.png",
        ],"image",100)
        ```
## Test
Type ```python app.py``` to run the app.
## Build
Type ```pyinstaller app.py --onefile --windowed --add-data "frames/;frames/"``` to build the app.