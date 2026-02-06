## Taichi practice

This is a repo that contains daily shader rendering practices with Taichi framwork. All the example is from some random thought or learning from some great shader writers.

https://thebookofshaders.com

### How to run
Any machine should be fine, just make sure you have GPU.

`pip install taichi`

Then you can do:

`python <each python file>`

A window should pop up and draw the result.

### Menu

00_Helloworld.py: a begning try to draw something on the screen.

01_HSB.py: conversion from hsb to rgb for a clearer display of color and intensicy.

02_DistanceField.py: Learn how to use fract to limit the data in range. Also try single channel image to display.

03_Shape.py: How to do color based on pixel location.

04_patternMove.py: Try to create pattern with fract function. Add time to move. This looks cooler and I learned some trick.

05_dfLine.py: Take mouse input and test to use distance field to draw AA lines.

06_imagenoise.py: An interesting practice on how to adjust UV to create noise effect. Notice the way to reduce the shift of uv by a 0.02 scale factor.

07_nosieSphere.py: This is the first part of the parctice, try to create our own noise function and apply to a sphere boundary.


#####

101_DRCourse1.py This is the implmentation of the first class.
