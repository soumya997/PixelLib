import cv2
import numpy as np
import pandas as pd
import random
import os
import sys
import math
from PixelLib.pixellib.mask_rcnn import MaskRCNN
from PixelLib.pixellib.config import Config
import colorsys
import time
from datetime import datetime
import imantics
from imantics import Polygons, Mask


class configuration(Config):
    NAME = "configuration"

coco_config = configuration(BACKBONE = "resnet101",  NUM_CLASSES =  81,  class_names = ["BG"], IMAGES_PER_GPU = 1, 
DETECTION_MIN_CONFIDENCE = 0.7,IMAGE_MAX_DIM = 1024, IMAGE_MIN_DIM = 800,IMAGE_RESIZE_MODE ="square",  GPU_COUNT = 1) 


class instance_segmentation():
    def __init__(self, infer_speed = None):
        if infer_speed == "average":
            coco_config.IMAGE_MAX_DIM = 512
            coco_config.IMAGE_MIN_DIM = 512
            coco_config.DETECTION_MIN_CONFIDENCE = 0.45

        elif infer_speed == "fast":
            coco_config.IMAGE_MAX_DIM = 384
            coco_config.IMAGE_MIN_DIM = 384
            coco_config.DETECTION_MIN_CONFIDENCE = 0.25

        elif infer_speed == "rapid":
            coco_config.IMAGE_MAX_DIM = 256
            coco_config.IMAGE_MIN_DIM = 256
            coco_config.DETECTION_MIN_CONFIDENCE = 0.20   
            

        self.model_dir = os.getcwd()

    def load_model(self, model_path):
        self.model = MaskRCNN(mode = "inference", model_dir = self.model_dir, config = coco_config)
        self.model.load_weights(model_path, by_name= True)


    def segmentImage(self, image_path, show_bboxes = False,process_frame = False, mask_points_values = False,  output_image_name = None, verbose = None):
        if process_frame ==False:
            image = cv2.imread(image_path)

        else:
            image = image_path

        new_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Run detection
        if verbose is not None:
            print("Processing image...")
        results = self.model.detect([new_img])    

        coco_config.class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']
        r = results[0]       
        if show_bboxes == False:
            ## By default displays the boolean pixel values of the masks 
            if mask_points_values == False:
              #apply segmentation mask
              output = display_instances(image, r['rois'], r['masks'], r['class_ids'], coco_config.class_names)

              if output_image_name is not None:
               cv2.imwrite(output_image_name, output)
               print("Processed image saved successfully in your current working directory.") 

              return r, output
            
            ##Displays the polygon points' values of the masks
            elif mask_points_values == True:
               mask = r['masks']
               contain_val = []
               for a in range(mask.shape[2]):
                m = mask[:,:,a]
                mask_values = Mask(m).polygons()
                val = mask_values.points
                contain_val.append(val)


               output = display_instances(image, r['rois'], mask, r['class_ids'], coco_config.class_names) 
                
               if output_image_name is not None:
                cv2.imwrite(output_image_name, output)
                print("Processed image saved successfully in your current working directory.") 

               r['masks'] = contain_val  
              
               return r, output
            

        else:
            ## By default displays the boolean pixel values of the masks 
            if mask_points_values == False:
              #apply segmentation mask with bounding boxes
              output = display_box_instances(image, r['rois'], r['masks'], r['class_ids'], coco_config.class_names, r['scores'])
            
              if output_image_name is not None:
               cv2.imwrite(output_image_name, output)
               print("Processed Image saved successfully in your current working directory.")

              return r, output


            ##Displays the polygon points' values of the masks
            elif mask_points_values == True:
               mask = r['masks']
               contain_val = []
               for a in range(mask.shape[2]):
                m = mask[:,:,a]
                mask_values = Mask(m).polygons()
                val = mask_values.points
                contain_val.append(val)


               output = display_box_instances(image, r['rois'], mask, r['class_ids'], coco_config.class_names, r['scores']) 
                
               if output_image_name is not None:
                cv2.imwrite(output_image_name, output)
                print("Processed image saved successfully in your current working directory.") 

               r['masks'] = contain_val  
              
               return r, output



    def segmentFrame(self, frame, show_bboxes = False, mask_points_values = False, output_image_name = None, verbose = None):
        if show_bboxes == False:
            ## By default displays the boolean pixel vlaues of the mask 
            if mask_points_values == False:
             #apply segmentation mask
             segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values, output_image_name=output_image_name)
            
             if output_image_name is not None:
              cv2.imwrite(output_image_name, output)
              print("Processed image saved successfully in your current working directory.")

             return segmask, output
            
            elif mask_points_values == True:
               segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values, output_image_name=output_image_name)

               if output_image_name is not None:
                cv2.imwrite(output_image_name, output)
                print("Processed image saved successfully in your current working directory.") 
              
               return segmask, output
        else:
            #apply segmentation mask with bounding boxes
            ## By default displays the boolean pixel vlaues of the mask 
            if mask_points_values == False:
             #apply segmentation mask
             segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values, output_image_name=output_image_name)
            
             if output_image_name is not None:
              cv2.imwrite(output_image_name, output)
              print("Processed image saved successfully in your current working directory.")

             return segmask, output
            
            ##Displays the polygon points' values of the masks
            elif mask_points_values == True:
               segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values, output_image_name=output_image_name)

               if output_image_name is not None:
                cv2.imwrite(output_image_name, output)
                print("Processed image saved successfully in your current working directory.") 
              
               return segmask, output
            
            

    def process_video(self, video_path, show_bboxes = False, mask_points_values = False, output_video_name = None, frames_per_second = None):
        capture = cv2.VideoCapture(video_path)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        codec = cv2.VideoWriter_fourcc(*'DIVX')
        
        if frames_per_second is not None:
            save_video = cv2.VideoWriter(output_video_name, codec, frames_per_second, (width, height))
        counter = 0
        start = time.time()     
           
        if show_bboxes == False:
            while True:
                counter +=1
                ret, frame = capture.read()
                if ret:
                    
                    
                    #apply segmentation mask
                    
                    if mask_points_values == False:
                        segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values)
                        print("No. of frames:", counter)
                    
                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if output_video_name is not None:
                          save_video.write(output)

                        

                    elif mask_points_values == True:
                        segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values)
                        print("No. of frames:", counter)
                       
                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if output_video_name is not None:
                          save_video.write(output)

                        

                else:
                    break 
                  
            end = time.time() 
            print(f"Processed {counter} frames in {end-start:.1f} seconds")  
            
           
            capture.release()
            if frames_per_second is not None:
                save_video.release()   

            return segmask, output     
 
        else:
            while True:
                counter +=1
                ret, frame = capture.read()
                if ret:
                    # Run detection
                    
                    
                       
                    #apply segmentation mask with bounding boxes
                    if mask_points_values == False:
                        segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values)
                        print("No. of frames:", counter)  
                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if output_video_name is not None:
                          save_video.write(output)

                        

                    elif mask_points_values == True:
                        segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values)
                        print("No. of frames:", counter)
                    
                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if output_video_name is not None:
                          save_video.write(output)

                          
                      
                else:
                    break
            
            capture.release()

            end = time.time()
            print(f"Processed {counter} frames in {end-start:.1f} seconds")  
        
            
            if frames_per_second is not None:
                save_video.release()
                 
            return segmask, output     
 

    def process_camera(self, cam, show_bboxes = False, mask_points_values = False, output_video_name = None, frames_per_second = None, show_frames = None, frame_name = None, verbose = None, check_fps = False):
        capture = cam
        if output_video_name is not None:
          width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
          height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
          save_video = cv2.VideoWriter(output_video_name, cv2.VideoWriter_fourcc(*'DIVX'), frames_per_second, (width, height))
        
        counter = 0
          
        start = datetime.now()       

        
           
        if show_bboxes == False:
            while True:
                
                ret, frame = capture.read()
                if ret:
                    if mask_points_values == False:
                        segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values)

                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if show_frames == True:
                            if frame_name is not None:
                              cv2.imshow(frame_name, output)
                            
                              if cv2.waitKey(25) & 0xFF == ord('q'):
                                break  

                        if output_video_name is not None:
                          save_video.write(output)

                        

                    elif mask_points_values == True:
                        segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values)

                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)
                        if show_frames == True:
                            if frame_name is not None:
                              cv2.imshow(frame_name, output)
                            
                              if cv2.waitKey(25) & 0xFF == ord('q'):
                                break  

                        if output_video_name is not None:
                          output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)
                          save_video.write(output)

                           

                   
                elif counter == 30:
                    break  
                 
            
            end = datetime.now()
            if check_fps == True:
                timetaken = (end-start).total_seconds()
                
                out = counter / timetaken
                print(f"{out:.3f} frames per second")   

            if verbose is not None: 
                print(f"Processed {counter} frames in {timetaken:.1f} seconds")     
           
            capture.release()

            if output_video_name is not None:
                save_video.release()  

            return segmask, output   

        else:
            while True:
               
                ret, frame = capture.read()
                if ret:
                    if mask_points_values == False:
                        segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values)

                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)
                        if show_frames == True:
                            if frame_name is not None:
                              cv2.imshow(frame_name, output)
                            
                              if cv2.waitKey(25) & 0xFF == ord('q'):
                                break  

                        if output_video_name is not None:
                          save_video.write(output)

                        

                    elif mask_points_values == True:
                        segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values)

                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)
                        if show_frames == True:
                            if frame_name is not None:
                              cv2.imshow(frame_name, output)
                            
                              if cv2.waitKey(25) & 0xFF == ord('q'):
                                break  

                        if output_video_name is not None:
                          output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)
                          save_video.write(output)

                        

                elif counter == 30:
                    break

            end = datetime.now()
            if check_fps == True:
                timetaken = (end-start).total_seconds()
                fps = counter / timetaken
                print(f"{fps:.3f} frames per second") 

            if verbose is not None:
                print(f"Processed {counter} frames in {timetaken:.1f} seconds") 
                    
                 
            capture.release()

            if output_video_name is not None:
                save_video.release() 

            return segmask, output   






#############################################################
#############################################################
""" CLASS FOR PERFORMING INFERENCE WITH A CUSTOM MODEL """
#############################################################
#############################################################




class custom_segmentation:
    def __init__(self):
       self.model_dir = os.getcwd()

    def inferConfig(self,name = None, network_backbone = "resnet101",  num_classes =  1,  class_names = ["BG"], batch_size = 1, detection_threshold = 0.7, 
    image_max_dim = 512, image_min_dim = 512, image_resize_mode ="square", gpu_count = 1):
        self.config = Config(BACKBONE = network_backbone, NUM_CLASSES = 1 +  num_classes,  class_names = class_names, 
        IMAGES_PER_GPU = batch_size, IMAGE_MAX_DIM = image_max_dim, IMAGE_MIN_DIM = image_min_dim, DETECTION_MIN_CONFIDENCE = detection_threshold,
        IMAGE_RESIZE_MODE = image_resize_mode,GPU_COUNT = gpu_count)
        
    def load_model(self, model_path):
        #load the weights for COCO
        self.model = MaskRCNN(mode="inference", model_dir = self.model_dir, config=self.config)
        self.model.load_weights(model_path, by_name=True)
    
    def segmentImage(self, image_path, show_bboxes = False,mask_points_values = False, process_frame = False, output_image_name = None, verbose = None):
        if process_frame ==False:
            image = cv2.imread(image_path)

        else:
            image = image_path

        new_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Run detection
        if verbose is not None:
            print("Processing image...")
        
        results = self.model.detect([new_img])

    
        r = results[0]       
        if show_bboxes == False:
            #By default it returns the boolean pixel values of the mask
            if mask_points_values == False:
                #apply segmentation mask
                output = display_instances(image, r['rois'], r['masks'], r['class_ids'],self.config.class_names)
            
                if output_image_name is not None:
                 cv2.imwrite(output_image_name, output)
                 print("22222222222222222222222222222222222222222222222222")
                 print("Processed image saved successfully in your current working directory.")

                return r, output

            ##Return the polygon points' values of the masks
            elif mask_points_values == True:
               mask = r['masks']
               contain_val = []
               for a in range(mask.shape[2]):
                m = mask[:,:,a]
                mask_values = Mask(m).polygons()
                val = mask_values.points
                contain_val.append(val)


               output = display_instances(image, r['rois'], mask, r['class_ids'], self.config.class_names) 
                
               if output_image_name is not None:
                cv2.imwrite(output_image_name, output)
                print("333333333333333333333333333333333333333333333333333333333")
                print("Processed image saved successfully in your current working directory.") 

               r['masks'] = contain_val  
              
               return r, output
            



        else:
            #apply segmentation mask with bounding boxes
            #By default it returns the boolean values of the mask
            if mask_points_values == False:
              output = display_box_instances(image, r['rois'], r['masks'], r['class_ids'], self.config.class_names, r['scores'])

              if output_image_name is not None:
               cv2.imwrite(output_image_name, output)
               print("44444444444444444444444444444444444444444444444444444444444")
               print("Processed Image saved successfully in your current working directory.")
    
              return r, output   
            
            ##Return the polygon points' values of the masks
            elif mask_points_values == True:
               mask = r['masks']
               contain_val = []
               for a in range(mask.shape[2]):
                m = mask[:,:,a]
                mask_values = Mask(m).polygons()
                val = mask_values.points
                contain_val.append(val)


               output = display_box_instances(image, r['rois'], mask, r['class_ids'], self.config.class_names, r['scores']) 
                
               if output_image_name is not None:
                cv2.imwrite(output_image_name, output)
                print("555555555555555555555555555555555555555555555555555")
                print("Processed image saved successfully in your current working directory.") 

               r['masks'] = contain_val  
              
               return r, output
            
 


    def segmentFrame(self, frame, show_bboxes = False, mask_points_values = False, output_image_name = None, verbose= None):
        if show_bboxes == False:
            if mask_points_values == False:
                #apply segmentation mask

                segmask, output = self.segmentImage(frame, show_bboxes=False, process_frame=True, mask_points_values=mask_points_values)
            
                if output_image_name is not None:
                 cv2.imwrite(output_image_name, output)
                 print("Processed image saved successfully in your current working directory.")

                return segmask, output

            elif mask_points_values == True:
                segmask, output = self.segmentImage(frame, show_bboxes=False, process_frame=True, mask_points_values=mask_points_values)
            
                if output_image_name is not None:
                 cv2.imwrite(output_image_name, output)
                 print("Processed image saved successfully in your current working directory.")

                return segmask, output    

        else:
            if mask_points_values == False:
                #apply segmentation mask with bounding boxes
                segmask, output = self.segmentImage(frame, show_bboxes=True, process_frame=True, mask_points_values=mask_points_values)
              
                if output_image_name is not None:
                 cv2.imwrite(output_image_name, output)
                 print("Processed Image saved successfully in your current working directory.")

                return segmask, output

            elif mask_points_values == True:
                segmask, output = self.segmentImage(frame, show_bboxes=True, process_frame=True, mask_points_values=mask_points_values)
            
                if output_image_name is not None:
                 cv2.imwrite(output_image_name, output)
                 print("Processed image saved successfully in your current working directory.")

                return segmask, output   

        
    def process_video(self, video_path, show_bboxes = False, mask_points_values = False, output_video_name = None, frames_per_second = None):
        capture = cv2.VideoCapture(video_path)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        codec = cv2.VideoWriter_fourcc(*'DIVX')
        if frames_per_second is not None:
            save_video = cv2.VideoWriter(output_video_name, codec, frames_per_second, (width, height))
        counter = 0
        start = time.time()     
           
        if show_bboxes == False:
            while True:
                counter +=1
                ret, frame = capture.read()
                if ret:
                    #apply segmentation mask
                    
                    if mask_points_values == False:
                        segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values)
                        print("No. of frames:", counter)
                    
                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if output_video_name is not None:
                          save_video.write(output)

                        

                    elif mask_points_values == True:
                        segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values)
                        print("No. of frames:", counter)
                       
                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if output_video_name is not None:
                          save_video.write(output)
                   
                else:
                    break 
                  
            end = time.time() 
            print(f"Processed {counter} frames in {end-start:.1f} seconds")  
            
           
            capture.release()
            if frames_per_second is not None:
                save_video.release()    
            return segmask, output   

        else:
            while True:
                counter +=1
                ret, frame = capture.read()
                if ret:
                    #apply segmentation mask
                    
                    if mask_points_values == False:
                        segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values)
                        print("No. of frames:", counter)
                    
                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if output_video_name is not None:
                          save_video.write(output)

                        

                    elif mask_points_values == True:
                        segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values)
                        print("No. of frames:", counter)
                       
                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if output_video_name is not None:
                          save_video.write(output)
                else:
                    break
            
            capture.release()

            end = time.time()
            print(f"Processed {counter} frames in {end-start:.1f} seconds")  
        
            
            if frames_per_second is not None:
                save_video.release()
                 
            return segmask, output   
            
                  
    def process_camera(self, cam, show_bboxes = False,  mask_points_values = False, output_video_name = None, frames_per_second = None, show_frames = None, frame_name = None, verbose = None, check_fps = False):
        capture = cam
        
        if output_video_name is not None:
            width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            codec = cv2.VideoWriter_fourcc(*'DIVX')
            save_video = cv2.VideoWriter(output_video_name, codec, frames_per_second, (width, height))

        counter = 0
        start = datetime.now()     

        if show_bboxes == False:
            while True:
                
                ret, frame = capture.read()
                if ret:
                    if mask_points_values == False:
                        segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values)

                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if show_frames == True:
                            if frame_name is not None:
                              cv2.imshow(frame_name, output)
                            
                              if cv2.waitKey(25) & 0xFF == ord('q'):
                                break  

                        if output_video_name is not None:
                          save_video.write(output)

                    elif mask_points_values == True:
                        segmask, output = self.segmentImage(frame, show_bboxes=False,process_frame=True, mask_points_values=mask_points_values)

                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)
                        if show_frames == True:
                            if frame_name is not None:
                              cv2.imshow(frame_name, output)
                            
                              if cv2.waitKey(25) & 0xFF == ord('q'):
                                break  

                        if output_video_name is not None:
                          output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)
                          save_video.write(output)    
                   
                elif counter == 30:
                    break  
                 
            end = datetime.now() 
            
            
            if check_fps == True:
                timetaken = (end-start).total_seconds()
                fps = counter/timetaken
                print(f"{fps} frames per seconds")   

            if verbose is not None:
                print(f"Processed {counter} frames in {timetaken:.1f} seconds") 
                        
           
            capture.release()

            if output_video_name is not None:
                save_video.release()  

             

            return segmask, output     

        else:
            while True:
                
                ret, frame = capture.read()
                if ret:
                    if mask_points_values == False:
                        segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values)

                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)

                        if show_frames == True:
                            if frame_name is not None:
                              cv2.imshow(frame_name, output)
                            
                              if cv2.waitKey(25) & 0xFF == ord('q'):
                                break  

                        if output_video_name is not None:
                          save_video.write(output)
                    

                    elif mask_points_values == True:
                        segmask, output = self.segmentImage(frame, show_bboxes=True,process_frame=True, mask_points_values=mask_points_values)

                        
                        output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)
                        if show_frames == True:
                            if frame_name is not None:
                              cv2.imshow(frame_name, output)
                            
                              if cv2.waitKey(25) & 0xFF == ord('q'):
                                break  

                        if output_video_name is not None:
                          output = cv2.resize(output, (width,height), interpolation=cv2.INTER_AREA)
                          save_video.write(output)    


                elif counter == 30:
                    break

            end = datetime.now()
            

            if check_fps == True:
                timetaken = (end-start).total_seconds()
                fps = counter/timetaken
                print(f"{fps} frames per seconds")

            if verbose is not None:
                print(f"Processed {counter} frames in {timetaken:.1f} seconds")     
        
            capture.release()

            if output_video_name is not None:
                save_video.release() 

            return segmask, output          





################VISUALIZATION CODE ##################




def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors


def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image

def color_class(class_ids):
    color_range = [(0.8705, 0.3568, 0.3568),( 0.2235, 0.4, 0.9803),(0.4704, 0.8588, 0.3529)]
    color_list = []
    
    for i in class_ids:
        if i==1:
            color_list.append(color_range[0])
        elif i==2:
            color_list.append(color_range[1])
        else:
            color_list.append(color_range[2])
    print("done here :D")
    return color_list
def color_class_gray(class_ids):
    color_range = [(1/255,1/255,1/255),(2/255,2/255,2/255),(3/255,3/255,3/255)]
    color_list = []
    
    for i in class_ids:
        if i==1:
            color_list.append(color_range[0])
        elif i==2:
            color_list.append(color_range[1])
        else:
            color_list.append(color_range[2])
    print("done here :D")
    return color_list
    


def display_instances(image, boxes, masks, class_ids,  class_name):
    
    n_instances = boxes.shape[0]
    colors = color_class_gray(class_ids)

    
    assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

    for i, color in enumerate(colors):
        mask = masks[:, :, i]

        image = apply_mask(image, mask, color)

        df = pd.DataFrame(mask)
        df.to_csv("/content/"+str(i)+".csv")
        print("666666666666666666666666666666666666666666666666666666")
    return image





def display_box_instances(image, boxes, masks, class_ids, class_name, scores):
    
    n_instances = boxes.shape[0]
    colors = random_colors(n_instances)

    
    assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

    for i, color in enumerate(colors):
        if not np.any(boxes[i]):
            continue

        y1, x1, y2, x2 = boxes[i]
        label = class_name[class_ids[i]]
        score = scores[i] if scores is not None else None
        caption = '{} {:.2f}'.format(label, score) if score else label
        mask = masks[:, :, i]

        image = apply_mask(image, mask, color)
        color_rec = [int(c) for c in np.array(colors[i]) * 255]
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color_rec, 2)
        image = cv2.putText(
            image, caption, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, color = (255, 255, 255))

    return image



