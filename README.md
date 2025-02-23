# quick-cropper
For cropping pictures to a new aspect ratio, one after the other, real fast.
The intended use case is quite simple: taking pictures on your phone will not have the traditional 4x6 or 5x7 aspect ratio expected when you place a print order.
It's easy enough to crop a couple of pictures, but if you want to decide exactly where to trim the edges off for many images, this will help you speed up the process.

## Dependencies
This tool depends on `PIL`, `tkinter`, `numpy`, `argparse`, and is written in python3.
Nothing crazy.

## Installing
I don't have a fancy install script because this is really a very small program. The `quick-crop.py` file itself has a `main` call, so you can just do `python3 quick-crop.py <args>`.

Personally, I like to clone the repo somewhere on my computer, e.g. `$HOME/repos/serial-cropper`. Then I create a bash script called `serial-crop`:
```
#!/bin/bash

python3 $HOME/repos/serial-cropper/quick-crop.py $@
```
and place it in my `PATH` (don't forget to `chmod +x` it).
Now I just run `serial-crop <args>` from anywhere.

## Usage
`serial-crop` takes only two parameters: the crop ratio specified with `-r`, and a list of `jpg` files specified with `-j`.
The ratio parameter is a string in the form "WxH", so if you want a 4x6 crop, you would call
```
serial-crop -r 4x6 -j my_image.jpg
```

This will launch a window with the first image of your list.
`serial-crop` will make the crop as large as possible while still maintaining the specified ratio.
In order to change the crop region, move the mouse across the image.
Sections that will be removed appear grayed out, so you can get a good idea of what the final image will look like.

In order to commit the crop, click the mouse.
The cropped image is now saved, and the next image appears on screen for you to crop.
Cropped images will be saved alognside the originals (`serial-crop` will never modify or destroy the original).
You will find the cropped version of an image has the same name as the original prefixed with "sc-rWxH-".

### Special moves
While the GUI is active and you are changing the crop region, there are two additional commands you can use:

* Space bar will flip the crop region around
* Entering a number N (usually 3) will superimpose an NxN grid over the crop region to help you balance subjects in the image
