# Information-Visualiser

#### Description.

A self-made QR code program that turns information into visual pattern, and back again. Note that this was built before I properly learnt to design software using OOP (and other practices), so the implementation may look a bit odd. For insight into the program's functionality, visit the **Documentation** directory.

#### Terminology.

* VISREP: "visual representation", used to describe the visual representation of some text in the form of an image.
* Identity blocks: the four corners of any given VISREP are unique, and are used to identify the location of each corner of the VISREP by the program, as well as estimate the block sizes.

#### Capabilities.

This program has an interactive user interface built in. It has been tested on Windows and MacOS. The user interface looks best on Windows, however functionality is the same between operating systems. It can do the following:

* Generate VISREP images that are previewed to the user.
* Save generated VISREP images to a directory selected by the user.
* Read saved VISREP images, and display the translated output to the user.
* Recieve video stream from the device's front camera, and translate and display any detected VISREP image shown. This can vary in success with lighting, movement and image quality.

Limitations:

* Emojis are not supported.
* Some Windows machines (for some reason) cannot access the webcam.

#### Demos

Generating a VISREP.

![](Demos/demo_generate_visrep.gif)

Reading a VISREP.

![](Demos/demo_read_visrep.gif)

Reading a VISREP and previewing the computer's vision. The red in the corners are the computer identifying the 'identity blocks', the red squares are where the computer calculates the next block to be, the green squares are the computer's adjustment to the centre of the block, the blue squares are where the computer calculates the first block of the next row are, and the purple is where the computer calculates the edge of the VISREP to be.

![](Demos/demo_dev_read_visrep.gif)

#### Requirements.

Built in modules used:

* tkinter
* sys
* os
* threading
* math

Installed modules used:

* cv2
* numpy
* PIL (pillow)

#### Directory breakdown.

* **run.py** executes the program.
* **constants.py** contains magic numbers, constants and directories. Allows for quick and accessible tweaking of magic numbers, aesthetic properties and directories.
* **gen_visrep_matrix.py** generates a VISREP matrix from text input.
* **gen_visrep_photo.py** generates an VISREP image file from a VISREP matrix.
* **read_visrep_matrix** translates a VISREP matrix to text.
* **read_visrep_photo.py** translates a VISREP image file to a visrep matrix.
* **read_visrep_video.py** translates video feed of a VISREP image to a VISREP matrix.
* **unit_tests.py** translates all image files inside the folder **EXAMPLES TO TRY** and outputs the result to the terminal.
* **developer_build** contains a duplicate of the program, however produces output useful to the developer, such as a visual preview to what the computer "sees", and measurements made about the image that are printed to the terminal.
* **Documentation** contains documentation for the project, providing insight into the purpose of many of the functions.
* **EXAMPLES TO TRY** includes images that the user can try scanning to test out the program.
* **resources** contains other non-python files that the program requires to operate, for functional and non-functional purposes.