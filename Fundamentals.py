# import ultralytics
# from ultralytics import YOLO
# import numpy as np
# from PIL import Image
# import cv2
# import pandas as pd

model_path = "/best_pothole.pt"
video_path = "/temp_video.mp4"

def format_number(num):
  """
  Convert an int number to a string expressed with three digits
  ES:  10 -> 010
        1 -> 001
      100 -> 100
  """
  if num < 10:
      return f'00{num}'
  elif num < 100:
      return f'0{num}'
  else:
      return str(num)

def bbox_to_y_center(bbox):
  """Given bbox coord, returns y coord of the center"""
  y_center = bbox[1] + (bbox[3] - bbox[1])/2
  return y_center


def video_to_frames(video_path):
  """Starting from the video path, returns a frame list (each frame in numpy)"""
  frames_list = []
  cap = cv2.VideoCapture(video_path)

  # Loop through the video frames
  while cap.isOpened():
      # Read a frame from the video
      success, frame = cap.read()

      if success:
        frames_list.append(frame)

      else:
          # Break the loop if the end of the video is reached
          break

  # Release the video capture object and close the display window
  cap.release()
  cv2.destroyAllWindows()
  return frames_list

def bboxes_coords_list_creator(frames_list,model):
  """Creates bboxes list from frames_list"""
  bboxes_coords_list = []

  for frame in frames_list:
    results = model(frame, verbose = False)
    bboxes_coord = results[0].boxes.xyxy.numpy()
    bboxes_coords_list.append(bboxes_coord)
  return bboxes_coords_list

def results_elaboration(model_path, video_path):
  # Load the model
  model = ultralytics.YOLO(model_path)
  # Create frames_list
  frames_list = video_to_frames(video_path)
  # Bboxes coords list creation
  bboxes_coords_list = bboxes_coords_list_creator(frames_list,model)
  
  # os.makedirs("/content/frame/") #CREA CARTELLA FRAME SE NECESSARIO
  
  
  #RESULTS CREATION
  
  y_center_coord_list = []
  frame_number_list = []
  paths_list = []
  image_area_list = []
  
  for frame_number in range(len(frames_list)):  #PER OGNI FRAME
    frame = frames_list[frame_number]           #FRAME ATTUALE
    frame_as_image = Image.fromarray(frame)     #FRAME ATTUALE IN FORMATO IMMAGINE
    bboxes = bboxes_coords_list[frame_number]   #BBOXES RILEVATE SUL FRAME ATTUALE
    for pothole_number, bbox in enumerate(bboxes): # PER OGNI BBOX RILEVATA NEL FRAME
      cropped_image = frame_as_image.crop(bbox)    #RITAGLIA
      path = "/content/frame/" + format_number(frame_number) +"_" + str(pothole_number) + ".jpg"
      cropped_image.save(path) #SALVA
  
      y_center_coord_list.append(bbox_to_y_center(bbox))
      frame_number_list.append(frame_number)
      paths_list.append(path)
      width, height = cropped_image.size
      image_area_list.append(width*height)
  
  results = pd.DataFrame({"path":paths_list,
                "y_center_coord": y_center_coord_list,
                "frame_number":frame_number_list,
                "image_area":image_area_list})
  
  
  # RESULTS FILTERING
  
  sup_lim = max(results["y_center_coord"])
  inf_lim = max(results["y_center_coord"]) - ((max(results["y_center_coord"]) - min(results["y_center_coord"]))*0.33)
  results = results[results["y_center_coord"]>inf_lim]
  results.reset_index(drop = True, inplace = True)
  
  
  #calcolo min e max di y_center_coord frame by frame con groupby
  
  min_dict = results.groupby("frame_number").min()["y_center_coord"].to_dict()
  max_dict = results.groupby("frame_number").max()["y_center_coord"].to_dict()
  min_image_area_dict = results.groupby("frame_number").max()["image_area"].to_dict()
  
  results["min_y_prev_frame"] = results["frame_number"].apply(lambda x: min_dict.get(x-1, None))
  results["max_y_prev_frame"] = results["frame_number"].apply(lambda x: max_dict.get(x-1, None))
  results["min_area_prev_frame"] = results["frame_number"].apply(lambda x: min_image_area_dict.get(x-1, None))
  
  
  no_previous = []
  for i in range(len(results["frame_number"])):
    frame_number = results["frame_number"][i]
    if (frame_number - 1) in results["frame_number"].to_list():
      no_previous.append(False)
    else:
      no_previous.append(True)
  
  results["no_previous"] = no_previous
  
  image_validity = []
  for i in range(len(results)):
    if results["no_previous"][i]:
      image_validity.append(True)
    elif results["y_center_coord"][i]<results["min_y_prev_frame"][i]:
      image_validity.append(True)
    elif results["y_center_coord"][i]>results["max_y_prev_frame"][i] and results["image_area"][i]<results["min_area_prev_frame"][i]:
      image_validity.append(True)
    else:
      image_validity.append(False)
  
  results["image_validity"] = image_validity
  
  
  results = results[results["image_validity"]==True]
  
  results = results.sort_values(by = "image_area", ascending=False)
  return results
