# Ardavan Bidgoli
# abidgoli
# adapted from Neural Style by Anish Athalye, copyright as below:
# Copyright (c) 2015-2016 Anish Athalye. Released under GPLv3.

import os 
import numpy as np
import scipy.misc
import math
import time
import ast

from stylize import stylize

# from argparse import ArgumentParser
# for copying files
from shutil import copyfile
# to compare files 
import filecmp
# for file save
from PIL import Image 

# inisital settings
# this is the trained network from Anish Athalye
VGG_PATH = 'imagenet-vgg-verydeep-19.mat'
# initial settings for the style transfer
CONTENT_WEIGHT = 5e0
STYLE_WEIGHT = 1e2
TV_WEIGHT = 1e2
LEARNING_RATE = 1e1
STYLE_SCALE = 1.0
ITERATIONS = 1000


class styleTransferClass(object):
    # class to handle style transfer process
    # basic data
    triggerFileName = 'trigger.txt'
    triggerFile = None
    syncFolder = "/Volumes/Ardavan/GoogleDrive/15112"
    destination = "outcome.jpg"

    def __init__(self):
        # nothing special! just start the class! 
        pass

    def run(self):
        sourceTag = "_source.jpg"
        stylizedTag = "_styled.jpg"
        while (True):
            triggerData = self.readTrigger()
            print (triggerData)
            if (triggerData != None):
                if triggerData['start']:
                    if triggerData['generateNew']:
                        # generates name for file
                        sharedName = self.generateSyncedFileName()
                        sourceSyncedName = sharedName+sourceTag
                        # first copies the source image to the sync folder
                        copyfile(triggerData['source'], sourceSyncedName)
                        # then generates a proper name for the stylized image
                        styledSyncName = sharedName+stylizedTag
                        # updates the destination address
                        styleTransferClass.destination = styledSyncName
                        self.startStylize(triggerData)
                        # it finish the process, since it is going to take
                        # a day to finish this part!
                        return
                    else:
                        self.uploadFromLibrary(triggerData)
            # waits between rereadings
            time.sleep(5)

    def uploadFromLibrary(self, triggerData):
        # saves image in the sync folder!
        rawFileList = os.listdir(styleTransferClass.syncFolder)
        fileList = self.cleanDSFiles(rawFileList)
        number = len(fileList)+1
        source = triggerData['source']
        destination = styleTransferClass.syncFolder+("/image%d.jpg"%number)
        for file in fileList:
            fullAddress = styleTransferClass.syncFolder+"/"+file
            # checks to see if the file is already existing in the folder
            if filecmp.cmp(fullAddress, source):
                print ("file is updating!")
                copyfile(source, file)
                self.wipeTriggerFile()
                return
        # makes a new name tag if the filw is new
        copyfile(source, destination)
        print ("%s is copied to %s" %(source, destination))
        self.wipeTriggerFile()
        return

    def generateSyncedFileName(self):
        # checks the filse in destination and find a proper indexed name
        rawFileList = os.listdir(styleTransferClass.syncFolder)
        fileList = self.cleanDSFiles(rawFileList)
        number = len(fileList)+1
        name = styleTransferClass.syncFolder+("/image%d"%number)
        return name


    def cleanDSFiles(self, fileList):
        # just cleans the fileList from .sd files
        # doesn't harm any file on drive!
        result = []
        for file in fileList:
            if (file.endswith(".DS_Store")):
                pass
            else:
                result.append(file)
        return result

    def wipeTriggerFile(self):
        # cleans te trigger.txt file
        # after the job is done!
        print("Wiping the trigger!")
        open(self.triggerFileName, 'w').close()

    def readTrigger(self):
        # reads trigger file
        try:
            # reads the trigger
            triggerFile = open(styleTransferClass.triggerFileName, 'r')
        except:
            print ("No trigger.txt exist yet")
        if (triggerFile != None):
            try:
                fileContent =  triggerFile.read()
                # converts trigger data into a dictionary
                result = ast.literal_eval(fileContent)
                return result
            except:
                return None

    def startStylize(self,triggerData):  
        # check for input data:
        self.checkInputs(triggerData)
        # runs stylizing
        # mostly adapted from Neural Style by Anish Athalye
        sourceImage = self.imageRead(triggerData['source'])
        styleImages = [self.imageRead(triggerData['style'])]
        iterations  = triggerData['quality']
        print ("Number of iterations: ",iterations)

        # the fixed values are adjustments for the style transfer
        # method, NO MAGIC! borrowed from previously mentioned source
        for iteration, image in stylize(
                                network=VGG_PATH,
                                initial=None,
                                content=sourceImage,
                                styles=styleImages,
                                iterations=iterations,
                                content_weight=CONTENT_WEIGHT,
                                style_weight=STYLE_WEIGHT,
                                style_blend_weights=[1],
                                tv_weight=TV_WEIGHT,
                                learning_rate=LEARNING_RATE,
                                print_iterations=True,
                                checkpoint_iterations=True
                                ):
            output_file = None
            output_file = self.destination
            if output_file:
                self.imageSave(output_file, image)

    def checkInputs(self, triggerData):        
        # prepare the list of files and relted messages
        filesToCheck= [VGG_PATH, triggerData['source'], triggerData['style']]
        message = ["Trained network doesn't exist",
                   "Source image cannot be found",
                   "Style image cannot be found"]
        # checks every file
        for i in range (len(filesToCheck)):
            if not os.path.isfile(filesToCheck[i]):
                print (message[i])
                return False
        print ("Everything seems good!")
        return True

    def writeOnTrigger(self, message):
        triggerFile.write(message)

    def imageRead(self,path):
        return scipy.misc.imread(path).astype(np.float)

    def imageSave(self,path, img):
        img = np.clip(img, 0, 255).astype(np.uint8)
        scipy.misc.imsave(path, img)

def main():
    styleTransfer = styleTransferClass()
    styleTransfer.run()

if __name__ == '__main__':
    main()