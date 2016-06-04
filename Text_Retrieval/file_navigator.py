import os
import sys

# function to navigate all the files in a folder
# returns the list of the files

# ChaLearn Cultural Events Dataset
#mainPath = '/Users/andreapilzer/Documents/Scuola_Magistrale/Masterarbeit/ChaLearn2015/'

# All the 100 Events
def list_events(path):
  dir_list = []
  for dir in os.listdir(path):
    if not dir.startswith('.'):
      dir_list.append(dir)
  return dir_list

# all the images event 0
# SOMEHOW IS NOT WORKING
def list_images(path):
  img_list = []
  for img in os.listdir(path):
    if not img.startswith('.'):
      img_list.append(img)
  return os.listdir(path)
