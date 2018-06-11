# Handwritten-Character-Recognition
Offline handwritten character recognition using deep convolutional neural networks. It can recognize both handwritten digits (0 -9) and
handwritten letters (upper-case and lower-case).

Currently image name can be input using the command line through the command
  "python textprep.py <imageName.extension>"
The neural network confuses the letter "O" and the digit "0" when shown to it as a standalone image. Currently no known solution exists to fix this issue
other than to look at the context because both symbols look similar.
