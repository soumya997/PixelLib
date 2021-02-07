# Inference with a custom model

We have trained and evaluated the model, the next step is to see the performance of the model on unknown images. 
We are going to test the model on the classes we have trained it on. If you are yet to download the nature's model trained on Nature dataset download it from [here](https://github.com/ayoolaolafenwa/PixelLib/releases/download/1.0.0/Nature_model_resnet101.h5)

*sample1.jpg*

![alt_but1](Images/butterfly.jpg)

```python

   import pixellib
   from pixellib.instance import custom_segmentation

   segment_image = custom_segmentation()
   segment_image.inferConfig(num_classes= 2, class_names= ["BG", "butterfly", "squirrel"])
   segment_image.load_model("mask_rcnn_model/Nature_model_resnet101.h5")
   segment_image.segmentImage("sample1.jpg", show_bboxes=True, output_image_name="sample_out.jpg")
```

```python

   import pixellib
   from pixellib.instance import custom_segmentation 
   segment_image =custom_segmentation()
   segment_image.inferConfig(num_classes= 2, class_names= ["BG", "butterfly", "squirrel"])
```

We imported the class custom_segmentation, the class for performing inference and created an instance of the class. We called the model configuration and introduced an extra parameter class_names.

```
class_names= ["BG", "butterfly", "squirrel"])
```
**class_names:** It is a list containing  the names of classes the model is trained with. "BG", it refers to the background of the image, it is the first class and must be available along the names of the classes.

**Note:** If you have multiple classes and you are confused of how to arrange the classes's names according to their class ids, in your test.json in the dataset's folder check the categories' list.

```
{
"images": [
{
"height": 205,
"width": 246,
"id": 1,
"file_name": "C:\\Users\\olafe\\Documents\\Ayoola\\PIXELLIB\\Final\\Nature\\test\\butterfly (1).png"
},
],
"categories": [
{
"supercategory": "butterfly",
"id": 1,
"name": "butterfly"
},
{
"supercategory": "squirrel",
"id": 2,
"name": "squirrel"
}
],

```


You can observe from the sample of the directory of test.json above, after the images's  list in your test.json is object categories's list, the classes's names are there with their corresponding class ids. Butterfly has the class id 1 and squirrel has the class id 2.Remember the first id "0" is kept in reserve for the background.

```python
  
  segment_image.load_model("mask_rcnn_model/Nature_model_resnet101.h5)

  segment_image.segmentImage("sample1.jpg", show_bboxes=True, output_image_name="sample_out.jpg")
```
The custom model is loaded and we called the function to segment the image.

![alt_but_seg](Images/butterfly_seg.jpg)



*sample2.jpg*
![alt_sq](Images/squirrel.jpg)

```python
  test_maskrcnn.segmentImage("sample2.jpg",show_bboxes = True, output_image_name="sample_out.jpg")
```


![alt_sq_seg](Images/squirrel_seg.jpg)


*WOW! We have successfully trained a custom model for performing instance segmentation and object detection on butterflies and squirrels.*



Video segmentation with a custom model.

*sample_video1*

We want to perform segmentation on the butterflies in this video.

[![alt_vid1](Images/vid.png)](https://www.youtube.com/watch?v=5-QWJH0U4cA)

```python
  
  import pixellib
  from pixellib.instance import custom_segmentation

  test_video = custom_segmentation()
  test_video.inferConfig(num_classes=  2, class_names=["BG", "butterfly", "squirrel"])
  test_video.load_model("Nature_model_resnet101")
  test_video.process_video("sample_video1.mp4", show_bboxes = True,  output_video_name="video_out.mp4", frames_per_second=15)
```

```python

  test_video.process_video("video.mp4", show_bboxes = True,  output_video_name="video_out.mp4", frames_per_second=15)
```
The function process_video is called to perform segmentation on objects in a video. 

It takes the following parameters:-

*video_path:* this is the path to the video file we want to segment.

*frames_per_second:*  this is the parameter used to set the number of frames per second for the saved video file. In this case it is set to 15 i.e the saved video file will have 15 frames per second.

*output_video_name:* this is the name of the saved segmented video. The output video will be saved in your current working directory.

*Output_video*

[![alt_vid2](Images/but_vid.png)](https://www.youtube.com/watch?v=bWQGxaZIPOo)



A sample of another segmented video with our custom model.

[![alt_vid3](Images/sq_vid.png)](https://www.youtube.com/watch?v=VUnI9hefAQQ&t=2s)



You can perform live camera segmentation with your custom model making use of this code:

```python

  import pixellib
  from pixellib.instance import custom_segmentation
  import cv2


  capture = cv2.VideoCapture(0)

  segment_camera = custom_segmentation()
  segment_camera.inferConfig(num_classes=2, class_names=["BG", "butterfly", "squirrel"])
  segment_camera.load_model("Nature_model_resnet101.h5")
  segment_camera.process_camera(capture, frames_per_second= 10, output_video_name="output_video.mp4", show_frames= True,
  frame_name= "frame")
```

You will replace the process_video funtion with process_camera function.In the function, we replaced the video's filepath to capture i.e we are processing a stream of frames captured by the camera instead of a video file. We added extra parameters for the purpose of showing the camera frames:

**show_frames:** this parameter handles the showing of segmented camera's frames.

**frame_name:** this is the name given to the shown camera's frame.



# Process opencv's frames 

```python

  import pixellib
  from pixellib.instance import custom_segmentation
  import cv2

  segment_frame = custom_segmentation()
  segment_frame.inferConfig(network_backbone="resnet101", num_classes=2, class_names=["BG", "butterfly", "squirrel"])
  segment_frame.load_model("Nature_model_resnet101.h5")

  capture = cv2.VideoCapture(0)
   while True:
     ret, frame = capture.read()
     segment_frame.segmentFrame(frame)
     cv2.imshow("frame", frame)
     if  cv2.waitKey(25) & 0xff == ord('q'):
        break  
```