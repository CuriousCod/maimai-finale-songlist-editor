# Otohime - maimai FiNALE songlist editor
Editor for maimai songlist table files

## Features ##
Allows the decryption/encryption and editing of the following files:
- mmMusic.bin
- mmScore.bin
- mmTextout_ex.bin
- mmTextout_jp.bin
- SoundBGM.txt

The application decrypts the bin files and converts the data contained within the files into a sqlite database file. This allows easier editing of the songlist either by using this application directy or any sqlite database tool (Db Browser for example).
New maimai table files can be generated from the database.
Importing data from older maimai versions is also possible (current only Murasaki is supported)

## Installation ##

- Application has been developed and tested using Python 3.9.1
- Install the required modules listed in the requirements.txt
- File decryption requires key.txt containing the maimai FiNALE AES key to be placed next to the __main__.py file.
- Start the application by running __main__.py

## Usage ##

- Add maimai FiNALE folder to the application using the **Select maimai files** window
    -  Run **Decrypt Files** & **Create Database From Files** commands from the same window
    -  This will generate a sqlite database that can be edited using the application or by external sqlite tools
-  Use the **Edit maimai FiNALE data** window to browse different tracks. 
    -  By changing the Track ID, the application will automatically look for any data contained under that track ID in the database
    -  **mmMusic** tab contains the basic track information
    -  **mmScore** tab contains the track's difficulty levels, note that the actual track notechart data is not contained here
    -  **soundBGM** tab links the track id to the sound file
    -  **Artist, track name and designer name** tabs allow editing the artist's, track's and notechart designer's display name
-  To generate new maimai table files, use the **Generate Maimai Files** window
    -  Files need to be also encrypted in order for them to work with FiNALE (except soundBGM.txt)
    -  Any files contained in the /input folder will be encrypted, (excluding soundBGM.txt)
    -  Files will be generated into the /output folder and the encrypted files into /output/encrypted
    -  Copy the files into their respective locations in the maimai game folder
-  To import data from Murasaki add the murasaki files using the **Select Maimai Files** window
    -  After adding the files to the application, importing the tracks using the **Import Maimai Data From Older Versions** window

## Preview ##

<img src="https://www.dropbox.com/s/hg5vd9senzlq95h/Otohime.png?raw=1" alt="preview" width="1080" height="520"/>

### Credits ###

- donmai-me for making the encryption/decryption script for maimai files (https://github.com/donmai-me/MaiConverter)
- DearPyGui developers for making the GUI framework (https://github.com/hoffstadt/DearPyGui)
