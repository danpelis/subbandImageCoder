# subbandImageCoder
CPE 462 Final Project


### Goal:

   Implement a subband image coder in a python

### Tasks:
- encoder.py: 
  - Perform subband decomposition
  - Perform scalar quantization
  - Perform entropy encoding
  - Produce a coded bit stream stored as a data file
- decoder.py:
  -Read in this coded file
  - Perform entropy decoding
  - Perform subband reconstruction
  - Produce a reconstructed image in the same format of the input image
- performance.py:
  - Calculate the Peak-Signal-to-Noise ratio of the reconstructed image
- additional:
  - The image coder should be able to accept an input parameter which specifies the quantization step size
    - This parameter will ultimately be used to control the size of the coded data file
    
### Target:

   Typical input image

