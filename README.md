# Handwritten-Character-Recognition
Offline handwritten character recognition using deep convolutional neural networks. It can recognize both handwritten digits (0 -9) and
handwritten letters (upper-case and lower-case).

Currently image name can be input using the command line through the command
  "python textprep.py <imageName.extension>"
The neural network confuses the letter "O" and the digit "0" when shown to it as a standalone image. Currently no known solution exists to fix this issue
other than to look at the context because both symbols look similar.
Ongoing work involves building a GUI and optimizing the neural network and the pre-processor module.

Installation

Python  
  Windows command line:  
    cd file_directory  
    
    pip install pandas
    pip install tensorflow
    pip install opencv-python
    pip install numpy
  
Npm  
  download and install npm v10.8.0 form here https://nodejs.org/en/  
  Windows command line:  
    cd file_directory  
    
    npm install

Executing the file:  
  Windows command line:  
    cd file_directory  
    electron .
    
    
