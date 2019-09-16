# Gesture Recognition

**_Problem Statement_**

Develop a feature in the smart-TV that can recognise five different gestures performed by the user which will help users control the TV without using a remote.

The gestures are continuously monitored by the webcam mounted on the TV. Each gesture corresponds to a specific command:

- Thumbs up:  Increase the volume
- Thumbs down: Decrease the volume
- Left swipe: 'Jump' backwards 10 seconds
- Right swipe: 'Jump' forward 10 seconds  
- Stop: Pause the movie

**_DataSet_**
[Link](https://drive.google.com/uc?id=1ehyrYBQ5rbQQe6yL4XbLWe3FMvuVUGiL)

The training data consists of a few hundred videos categorised into one of the five classes. Each video (typically 2-3 seconds long) is divided into a sequence of 30 frames(images). These videos have been recorded by various people performing one of the five gestures in front of a webcam - similar to what the smart TV will use. 

The data is in a zip file. The zip file contains a 'train' and a 'val' folder with two CSV files for the two folders. These folders are in turn divided into subfolders where each subfolder represents a video of a particular gesture. Each subfolder, i.e. a video, contains 30 frames (or images). Note that all images in a particular video subfolder have the same dimensions but different videos may have different dimensions. Specifically, videos have two types of dimensions - either 360x360 or 120x160 (depending on the webcam used to record the videos). We should preprocess the images to streamline the same.

Each row of the CSV file represents one video and contains three main pieces of information - the name of the subfolder containing the 30 images of the video, the name of the gesture and the numeric label (between 0-4) of the video.


**_Solution_**

The solution consists of two types of architecture commonly used for analysing videos, both explained below.

- Convolutions + RNN
The conv2D network will extract a feature vector for each image, and a sequence of these feature vectors is then fed to an RNN-based network. The output of the RNN is a regular softmax (for a classification problem)

- 3D Convolutional Network, or Conv3D
3D convolutions are a natural extension to the 2D convolutions. Just like in 2D conv, we move the filter in two directions (x and y), in 3D conv, we move the filter in three directions (x, y and z). In this case, the input to a 3D conv is a video (which is a sequence of 30 RGB images). If we assume that the shape of each image is 100x100x3, for example, the video becomes a 4-D tensor of shape 100x100x3x30 which can be written as (100x100x30)x3 where 3 is the number of channels.

_The below mentioned experiments have been tried out throughout the case study_

|Experiment Number|Model|Result/ Accuracy|Decision + Explanation
|:---|:---|:---|:---|
|Model 1 - variation 1|Using Conv3D and MaxPooling3D|0.67|Run the model with 3 Conv3D and one Dense and Flatten layer with 28 batches and 50 epochs|
|Model 2 - variation 1|Using Conv3D and MaxPooling3D|0.71|Increased the no of Conv3D layers to 5 with same preprocessing as the previous model. Lowered the model learning rate as well.|
|Model 2 - variation 2|Using Conv3D and MaxPooling3D|0.68|Changed Cropping ratio of the Image and trained with higher batch size and lower learning rate. Kept the model parameters same.|
|Model 2 - variation 3|Using Conv3D and MaxPooling3D|0.72|Changed Cropping ratio further for the Image, keeping the rest same|
|Model 2 - variation 4|Using Conv3D and MaxPooling3D|0.74|Changed Cropping ratio to 20:140 with the same model parameters.|
|Model 3|Using LSTM and Dense|0.46|After Conv3D, tried LSTM and Dense with ‘softmax’ at end. For LSTM, needed a new Generator method to output batch data in 3-dimensional form for LSTM.|
|Model 4 - variation 1|Using TimeDistributed Conv2D and MaxPooling2D followed by LSTM and Dense|0.21|Using TimeDistributed Conv2D and MaxPooling2D followed by LSTM and Dense.|
|Model 4 - variation 2|Using TimeDistributed Conv2D and MaxPooling2D followed by LSTM and Dense. Using both edge and affine image transformation in Generator.|0.27|This is same as above however used image transformation. For this, created new generator method with affine and edge transformation flags.|
|Model 4 - variation 3|TimeDistributed Conv2D and MaxPooling2D followed by LSTM and Dense. With only edge transformation|0.25|This is same as above but with only edge transformation.|
|Model 1 - variation 2|Using Conv3D and MaxPooling3D. Doing both affine and edge transformation|0.52|Using Conv3D and MaxPooling3D. Doing both affine and edge transformation|
|Model 1 - variation 3|Using Conv3D and MaxPooling3D. Doing only edge transformation|0.50|Using Conv3D and MaxPooling3D. Doing only edge transformation|
||||
||||
||||
|**Final Model**|Model 2 - variation 4|0.74|Choose this is the final model as it gives the highest validation accuracy. 
||||

_[Final Download Model Link](https://drive.google.com/file/d/1qLZ182xZHgtAwdVAuRyTiITvHVmpGuL_/view?usp=sharing)_
