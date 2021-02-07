# Semantic segmentation of videos with PixelLib using Pascalvoc model

PixelLib is implemented with Deeplabv3+ framework to perform semantic segmentation. Xception model trained on pascalvoc dataset is used for semantic segmentation.

Download the xception model from [here](https://github.com/ayoolaolafenwa/PixelLib/releases/download/1.1/deeplabv3_xception_tf_dim_ordering_tf_kernels.h5)

**Code to implement semantic segmentation of a video with pascalvoc model**:

```python

  import pixellib
  from pixellib.semantic import semantic_segmentation

  segment_video = semantic_segmentation()
  segment_video.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
  segment_video.process_video_pascalvoc("video_path",  overlay = True, frames_per_second= 15, output_video_name="path_to_output_video")
```
We shall take a look into each line of code.


```python

  import pixellib
  from pixellib.semantic import semantic_segmentation

  #created an instance of semantic segmentation class
  segment_image = semantic_segmentation()
```
The class for performing semantic segmentation is imported from pixellib and we created an instance of the class.

```python

  segment_image.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5") 
```
We called the function to load the xception model trained on pascal voc. 

```python

  segment_video.process_video_pascalvoc("video_path",  overlay = True, frames_per_second= 15, output_video_name="path_to_output_video")
```
This is the line of code that performs segmentation on an image and the segmentation is done in the pascalvoc's color format. This function takes in two parameters:

**video_path:** the path to the video file we want to perform segmentation on.

**frames_per_second:** this is parameter to set the number of frames per second for the output video file. In this case it is set to 15 i.e the saved video file will have 15 frames per second.

**output_video_name:** the saved segmented video. The output video will be saved in your current working directory.

**Sample video**

[![alt_vid1](Images/save_vid3.jpg)](https://www.youtube.com/watch?v=8fkthbwqmB0)

```python

  import pixellib
  from pixellib.semantic import semantic_segmentation

  segment_video = semantic_segmentation()
  segment_video.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
  segment_video.process_video_pascalvoc("sample_video1.mp4",  overlay = True, frames_per_second= 15, output_video_name="output_video.mp4")
```  

**Output video**

[![alt_vid2](Images/vide_pascal.png)](https://www.youtube.com/watch?v=l9WMqT2znJE)

This is the saved segmented video using pascal voc model.

# Segmentation of live camera**


We can use the same model to perform semantic segmentation on camera. This can be done by few modifications to the code to process video file.

``` python

  import pixellib
  from pixellib.semantic import semantic_segmentation
  import cv2


  capture = cv2.VideoCapture(0)

  segment_video = semantic_segmentation()
  segment_video.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
  segment_video.process_camera_pascalvoc(capture,  overlay = True, frames_per_second= 10, output_video_name="output_video.mp4", show_frames= True,frame_name= "frame")
```

We imported cv2 and included the code to capture camera's frames.

```python

  segment_video.process_camera_pascalvoc(capture,  overlay = True, frames_per_second= 15, output_video_name="output_video.mp4", show_frames= True,frame_name= "video_display")  
```

In the code for performing segmentation, we replaced the video's filepath to capture i.e we are going to process a stream camera's frames instead of a video file.We added extra parameters for the purpose of showing the camera frames:

**show_frames:** this parameter handles showing of segmented camera frames and press q to exist.
**frame_name:** this is the name given to the shown camera's frames.




A demo by me showing the output of pixelLib's semantic segmentation on camera's feeds using pascalvoc model.

[![alt_vid3](Images/cam_pascal.png)](https://www.youtube.com/watch?v=8oSRYf9Ow2E)