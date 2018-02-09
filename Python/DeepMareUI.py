# Ardavan Bidgoli
# abidgoli 
# 15-112 Term Project
# adopted from:
# http://www.newthinktank.com/2016/10/kivy-tutorial-5/
# https://github.com/inclement/kivycrashcourse/blob/\n
# master/video14-using_a_screenmanager/after.py

from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from shutil import copyfile
import time
import random
from random import randint
import urllib
import urllib.request
import os
from os.path import join, dirname

from kivy.network.urlrequest import UrlRequest
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.loader import Loader
from kivy.config import Config
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.core.image import Image
##########################
from glob import glob

from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.core.window import Window

########################################################################
# App screens
########################################################################
# These classes are screens of the Kivy interface
class MainMenu(Screen):
    def resetProgram(self):
        MyScreenManager.resetData()

# Method selection page
class SelectionMenu(Screen):
    def SetHelp(self):
        # defines the returning page after viewing help page
        self.manager.get_screen('Help').returnPage = "SelectionMenu"
        # updating the help message
        MyScreenManager.setLabelText(self, 'Help', MyScreenManager.helpSelectionMenu)

# these three pages are three methods of file selection
class URLSelect(Screen):
    # check to see if any file is read
    imageSelected = False
    # check the number of inputs
    def checkURL (self):
        status = True
        for url in MyScreenManager.imageURLs:
            if url == "":  status = False
            if url.startswith("https"): status = False
        if status:
            text = MyScreenManager.passMessage
            MyScreenManager.setLabelText(self, 'CheckView', text)
        else:
            text = MyScreenManager.badURL
            MyScreenManager.setLabelText(self, 'CheckView', text)            

    # generates error or success message
    def checkSelection(self):
        if (self.imageSelected):
            text = MyScreenManager.passMessage
            MyScreenManager.setLabelText(self, 'CheckView', text)
        else:
            text = MyScreenManager.notEnoughImageSel
            MyScreenManager.setLabelText(self, 'CheckView', text)

    def SetText(self):
        # after downloading updates the message
        text = MyScreenManager.imagesDownloaded
        MyScreenManager.setLabelText(self, 'Process', text)
        print ("updating")
        # updates the file names in the checkview window
        self.manager.get_screen('CheckView').sourceImageAddress = "source.jpg"
        self.manager.get_screen('CheckView').styleImageAddress = "style.jpg"
    
    def SetHelp(self):
        # set the necessary data for the help page
        self.manager.get_screen('Help').returnPage = "URLSelect"
        MyScreenManager.setLabelText(self, 'Help', MyScreenManager.helpURLSelect)

# file selection
class SelectFiles(Screen):
    # check to see if any file is read
    imageSelected = False
    # check the number of inputs
    def checkVal (self,val):
        if (len(val) == 2 ):
            self.imageSelected = True

    # generates error or success message
    def checkSelection(self):
        if (self.imageSelected):
            text = MyScreenManager.passMessage
            MyScreenManager.setLabelText(self, 'CheckView', text)
        else:
            text = MyScreenManager.notEnoughImageSel
            MyScreenManager.setLabelText(self, 'CheckView', text)
    
    def SetText(self):
        text = MyScreenManager.imagesSelected
        MyScreenManager.setLabelText(self, 'Process', text)
        self.manager.get_screen('CheckView').sourceImageAddress = "source.jpg"
        self.manager.get_screen('CheckView').styleImageAddress = "style.jpg"
    
    def SetHelp(self):
        self.manager.get_screen('Help').returnPage = "SelectFiles"
        MyScreenManager.setLabelText(self, 'Help', MyScreenManager.helpSelectFiles)


# select ready file from a library
class SelectFromLibrary(Screen):
    imageSelected = False
    def checkVal (self,val):
        if (len(val) == 1 ):
            self.imageSelected = True

    def checkSelection(self):
        if (self.imageSelected):
            print ("Success message")
            text = MyScreenManager.passMessage
            MyScreenManager.setLabelText(self, 'CheckViewLibrary', text)
        else:
            print ("Error message")
            text = MyScreenManager.noImageSelected
            MyScreenManager.setLabelText(self, 'CheckViewLibrary', text)

    def SetText(self):
        text = MyScreenManager.imageReadFromLibrary
        self.manager.get_screen('CheckViewLibrary').sourceImageAddress = "placeholder.jpg"
        
    def updateImage(self):
        print ("updating the file!")
        self.manager.get_screen('CheckViewLibrary').sourceImageAddress = "source.jpg"

    def SetHelp(self):
        self.manager.get_screen('Help').returnPage = "SelectFromLibrary"
        MyScreenManager.setLabelText(self, 'Help', MyScreenManager.helpSelectFromLibrary)
    
# shows images for review
class CheckView(Screen):
    labelText = StringProperty("")
    # placeholder for image empy space
    sourceImageAddress = StringProperty("placeholder.jpg")
    styleImageAddress  = StringProperty("placeholder.jpg")
    def SetHelp(self):
        self.manager.get_screen('Help').returnPage = "CheckView"
        MyScreenManager.setLabelText(self, 'Help', MyScreenManager.helpCheckView)
    def resetProgram(self):
        MyScreenManager.resetData()

# show ready image from library
class CheckViewLibrary(Screen):
    # place holder message for 
    labelText = StringProperty('Fine!')
    sourceImageAddress = StringProperty("placeholder.jpg")
    
    def SetText(self):
        text = "Your scene is ready, please put on the HMD!"
        MyScreenManager.setLabelText(self, 'Finish', text)
    
    def SetHelp(self):
        self.manager.get_screen('Help').returnPage = "CheckViewLibrary"
        MyScreenManager.setLabelText(self, 'Help', MyScreenManager.helpCheckViewLibrary)

    def resetProgram(self):
        MyScreenManager.resetData()

# data about me and project!
class credits(Screen):
    pass

# obvious!
class Settings(Screen):
       def SetHelp(self):
        self.manager.get_screen('Help').returnPage = "Settings"
        MyScreenManager.setLabelText(self, 'Help', MyScreenManager.helpSettings)

# process page, 
class Process(Screen):
    # place holder message for 
    labelText = StringProperty('Well...wait')

# help screen
class Help(Screen):
    # change it later!
    returnPage = "Finish"
    labelText = StringProperty('Stay strong! Find it yourself...')

class Finish(Screen):
    # a placeholder message
    labelText = StringProperty("Done! Please wait for the process")

########################################################################
# Screen manager and its methods
########################################################################

class MyScreenManager(ScreenManager):
    # Trigger file settings
    triggerName = "trigger.txt"
    trigger = open(triggerName, "w")

    # place holder for message values
    url1 = ""
    url2 = ""
    restart = False
    generateNew = True
    imageURLs = ["", ""]
    names = ["source.jpg", "style.jpg"]
    sourceImage = "placeholder.jpg"
    processMessage = "This is awesome!"
    iterations = 1000
    # message to be written on trigger file
    message = dict()


    # UI values
    mainText = "DeepMare"

    # error messages
    httpsSupport        = "https is not supported yet!"
    downLoadError       = "Image can not be downloaded, please try again"
    noImageSelected     = "No image"
    notEnoughImageSel   = "Needs two images"
    badURL              = "Bad url(s)"
    # success messages
    imagesSelected      = "Images have succefully been selected"
    imagesDownloaded    = "Images have succefully been downloaded"
    imageReadFromLibrary= "Image has been read from library"
    passMessage         = "Loaded!!"

    # helpMessages
    helpSelectionMenu   = "You can define your method to create a new scene"
    helpURLSelect       = """Download your images from the web using their urls.
                           Please only use http protocl."""
    helpSelectFiles     = """Select two images, as the source and style.
                           Please remember that the order matters!"""
    helpSelectFromLibrary= "Select one image from your library to view"
    helpCheckView       = "Please review your images"
    helpCheckViewLibrary= "Please review your image"
    helpSettings        = "Adjust the iterations and let it go!"

    # Button sizes and setup
    fontSizeSmall   = 14
    fontSizeBig     = 28
    sizeHintSmallX  = (.15, 1 )
    sizeHintBigX    = (.3,1)
    sizeHintBiggerX    = (.5,1)
    sizeHintHorizontal = (1., .2)
    sizeHintY       = 1
    transDur        = 1 
    transDirL       = 'left'
    transDirR       = 'right' 
    transDirU       = 'up' 
    transDirD       = 'down' 
    
    iterationsMax   = 2000
    iterationsDef   = 1000

    def resetData():
        # cleans up the folder
        nameList = MyScreenManager.names
        nameList.append(MyScreenManager.triggerName)
        for name in nameList :
            try:
                print ("deleting %s" % name )
                open(name, 'w').close()
                #os.remove("source.jpg")
            except:
                print ("%s not deleted" % name)

    def setLabelText(self, screen, message):
        self.manager.get_screen(screen).labelText = message

    def saveFromURL(self):
        # save an image from an url to the disk
        # it doesn't read from https urls yet!
        # reads data from urls and saves them
        for i in range (len(MyScreenManager.names)):
            try:
                urlImageRetrive(MyScreenManager.imageURLs[i]
                                    ,MyScreenManager.names[i], i)
            except:
                print (MyScreenManager.names[i])
                print("can not downoad image")
        # defines the trigger value for generating a new 
        # stylizing
        MyScreenManager.generateNew = True

    def saveImageFromDrive(self,rawPath):
        # recieves a path from kivy file browser
        # and saves file in the code's folder
        path = []
        path.extend(rawPath)
        # for reviewing from library
        if len(path)  == 1 : MyScreenManager.generateNew = False
        # for generating a new one
        else: MyScreenManager.generateNew = True
        # saves or rewrite files on the drive 
        for i in range(len(path)):
            copyfile(path[i], MyScreenManager.names[i])


    def saveURLfromButton(self, url, index):
        # saves the url string from the interface into the class property
        cleanUrl = url.strip()
        if cleanUrl.startswith("https"):
            text =  MyScreenManager.httpsSupport 
            self.manager.get_screen('Process').labelText = text
        else:
            MyScreenManager.imageURLs[index] = cleanUrl

    def generateMessage(self, reset= False, start = False):
        # generating a new message for the trigger file
        if (reset) : MyScreenManager.message = dict() 
        # setting the values
        message = dict()
        message['start'] = start
        message['generateNew'] = MyScreenManager.generateNew
        message['source'] = MyScreenManager.names[0]
        message['style'] = MyScreenManager.names[1]
        message['iterations'] = MyScreenManager.iterations
        # wrting values to the class property
        MyScreenManager.message = message

    def setIteration(self, iterations = 1000):
        # iteration is set in the last screen, updated here
        print("Setting iterations!")
        MyScreenManager.message['iterations'] = int(iterations)

    def editTrigger(self):
        # writes on the trigger file to activate stylizer script
        print ("writing!")
        newTrigger = Trigger()
        newTrigger.writeOnFile(MyScreenManager.message)


########################################################################
# Some extra functions! (I may later move them to screenmanager class)
########################################################################
def urlImageRetrive(url, name, index):
    # tries to retrive an image from a URL
    if (url != "" and name != ""):
        try:
            urllib.request.urlopen(url)
            return urllib.request.urlretrieve(url,name)
        except:
           MyScreenManager.processMessage = \
                        MyScreenManager.downLoadError
           return None

def writeOnFile(file, message):
    # writes data over the file on the disk
    file.write(message)
    file.close()
    pass

class Trigger (object):
    # creates a trigger file to communicate with other components
    def __init__(self):
        self.name = "trigger.txt"
        self.triggerFile = open (self.name , "w")

    def writeOnFile(self, message):
        # writes on the file
        if (type(message) != str): message = str(message)
        self.triggerFile.write(message)
        self.triggerFile.close()
########################################################################
# Kivy file
########################################################################

root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import Clipboard kivy.core.clipboard.Clipboard

# all the screen class instances
MyScreenManager:
    MainMenu:
    SelectionMenu:
    URLSelect:
    CheckView:
    SelectFiles:
    SelectFromLibrary:
    CheckViewLibrary:
    Finish:
    credits:
    Process:
    Help:

# custom button
<helpButton@Button>:
    text: "Help"
    font_size: 14
    size_hint: .15, 1

# every screen is adjusted here
# most of the code is shared among screens 
# only the first appearance will be commented
<MainMenu>:
    # name of the screen
    name: 'MainMenu'
    color: 0, 0, 0, 1
    # main layout of the screen
    BoxLayout:
        Button:
            text: root.manager.mainText
            font_size: root.manager.fontSizeBig
            # Set the behavior of the button on press
            on_press:
                # wipes the files in the folder
                root.resetProgram()
                # transision direction
                root.manager.transition.direction = root.manager.transDirL
                # speed
                root.manager.transition.duration = root.manager.transDur
                # target page
                root.manager.current = 'SelectionMenu'


<SelectionMenu>:
    name: 'SelectionMenu'
    BoxLayout:
        Button:
            text: "Back"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.transition.direction = root.manager.transDirR
                root.manager.current = 'MainMenu'
        helpButton:
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.SetHelp()
                root.manager.transition.direction = root.manager.transDirU
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'Help'
        
        BoxLayout:
            orientation: 'vertical'
            Button:
                id: fromLibrary
                size_hint: root.manager.sizeHintHorizontal
                text: "Select from the available library"
                on_release:
                    root.manager.transition.direction = root.manager.transDirL
                    root.manager.transition.duration = root.manager.transDur
                    root.manager.current = 'SelectFromLibrary'
            Button:
                id: newFromDrive
                size_hint: root.manager.sizeHintHorizontal
                text: "Generate new from existing files"
                on_release:
                    root.manager.transition.direction = root.manager.transDirL
                    root.manager.transition.duration = root.manager.transDur
                    root.manager.current = 'SelectFiles'
            Button:
                id: newFromURL
                size_hint: root.manager.sizeHintHorizontal
                text: "Generate new by downloading files"
                on_release:
                    root.manager.transition.direction = root.manager.transDirL
                    root.manager.transition.duration = root.manager.transDur
                    root.manager.current = 'URLSelect'

<URLSelect>:
    name: 'URLSelect'
    BoxLayout:
        Button:
            text: "Back"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.transition.direction = root.manager.transDirR
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'SelectionMenu'
        helpButton:
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.SetHelp()
                root.manager.transition.direction = root.manager.transDirU
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'Help'

        BoxLayout:
            orientation: 'vertical'
            Button:
            # reads first url
                id: url1
                size_hint: root.manager.sizeHintHorizontal
                text: "Click to paste source image url"
                on_release:
                    app.root.saveURLfromButton(Clipboard.paste(),0)

            Button:
            # reads the other url
                id: url2
                size_hint: root.manager.sizeHintHorizontal
                text: "Click to paste style image url"
                on_release:
                    app.root.saveURLfromButton(Clipboard.paste(),1)

        Button:
            id: process
            size_hint: root.manager.sizeHintBigX
            text: 'Download'
            on_release: 
                # saves URLs
                app.root.saveFromURL()
                # updates message for generating a new image
                root.manager.generateMessage(reset = True, start = True)
                # updates the source and style names
                root.SetText()
                root.checkURL()
                root.checkSelection()
                root.manager.transition.direction = root.manager.transDirL
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'CheckView'


<SelectFiles>:
    name: 'SelectFiles'
    BoxLayout:
        Button:
            text: "Back"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.transition.direction = root.manager.transDirR
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'SelectionMenu'
        
        helpButton:
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.SetHelp()
                root.manager.transition.direction = root.manager.transDirU
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'Help'

        BoxLayout:
            # shows the icon menu to select two images
            FileChooserIconView:
                id: icon_view_tab
                show_hidden: False
                multiselect: True
                # starts from desktop
                path: "~/desktop"

        Button:
            id: process
            size_hint: root.manager.sizeHintBigX
            text: 'Load'
            on_release: 
                val = icon_view_tab.selection
                root.manager.saveImageFromDrive(val)
                root.manager.generateMessage(reset = True, start = True)
                root.SetText()
                root.checkVal(val)
                root.checkSelection()
                root.manager.transition.direction = root.manager.transDirL
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'CheckView'

<CheckView>:
    name: 'CheckView'
    BoxLayout:
        Button:
            text: "Back"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.resetProgram()
                root.manager.transition.direction = 'right'
                root.manager.current = 'SelectionMenu'
        helpButton:
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.SetHelp()
                root.manager.transition.direction = 'up'
                root.manager.transition.duration = 1
                root.manager.current = 'Help'

        Button:
        # shows the status of selection
            size_hint: root.manager.sizeHintBiggerX
            id: main
            text: root.labelText

        Image:
        # preview of the first iamge
            id: sourcePreview
            source: root.sourceImageAddress

        Image:
        # preview of the second iamge
            id: stylePreview
            source: root.styleImageAddress

        Button:
            id: process
            size_hint: root.manager.sizeHintBigX
            text: 'Process'
            on_release: 
                root.manager.transition.direction = root.manager.transDirL
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'Process'

<SelectFromLibrary>:
    name: 'SelectFromLibrary'
    BoxLayout:
        Button:
            text: "Back"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.transition.direction = root.manager.transDirR
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'SelectionMenu'
        helpButton:
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.SetHelp()
                root.manager.transition.direction = root.manager.transDirU
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'Help'
        
        BoxLayout:
            FileChooserListView:
                id: list_view_tab
                show_hidden: False
                path: "~/desktop"
        
        Button:
            id: process
            size_hint: root.manager.sizeHintBigX
            text: 'Load'
            on_release: 
                val = list_view_tab.selection
                root.manager.saveImageFromDrive(val)
                root.manager.generateMessage(reset = True, start = True)
                root.checkVal(val)
                root.SetText()
                root.updateImage()
                root.checkSelection()
                root.manager.transition.direction = root.manager.transDirL
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'CheckViewLibrary'

<CheckViewLibrary>:
    name: 'CheckViewLibrary'
    BoxLayout:
        Button:
            text: "Back"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.SetText()
                root.resetProgram()
                root.manager.transition.direction = root.manager.transDirR
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'SelectionMenu'
        Button:
            size_hint: root.manager.sizeHintSmallX
            id: main
            text: root.labelText

        Image:
            id: libraryImage
            source: root.sourceImageAddress

        Button:
            id: process
            size_hint: root.manager.sizeHintBigX
            text: 'Process'
            on_release: 
                root.manager.transition.direction = root.manager.transDirL
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'Finish'

<Process>:
    name: 'Process'
    BoxLayout:
        Button:
            text: "Back"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.transition.direction = root.manager.transDirR
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'SelectionMenu'
        helpButton:
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.transition.direction = root.manager.transDirU
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'Help'

        BoxLayout:
            orientation: 'vertical'
            Button:
                id: main
                text: root.labelText
            Button:
                id: sliderValue
                text: "Quality: " + str(int(slider.value))
            Slider:
                id: slider
                max: root.manager.iterationsMax
                value: root.manager.iterationsDef
                on_value: 
                    slider.value = self.value
        
        Button:
            text: 'Send'
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.iterations = slider.value
                root.manager.setIteration(slider.value)
                root.manager.editTrigger()
                root.manager.transition.direction = root.manager.transDirL
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'Finish'

<Finish>:
    name:'Finish'
    BoxLayout:
        Button:
            text: root.labelText
        Button:
            text: "Main menu"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.transition.direction = root.manager.transDirR
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'MainMenu'
        Button:
            text: "Credits"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.transition.direction = root.manager.transDirL
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'Credits'

<Credits>:
    name: 'Credits'
    BoxLayout:
        text: 'Credits'
        RstDocument:
            text:
                '\\n'.join(("DeepMare", "-----------",
                "By Ardavan Bidgoli, with the help of many people!",
                "There will be many references here some day!",
                "Some parts of the code adopted from these projects:",
                "http://www.newthinktank.com/2016/10/kivy-tutorial-5/",
                "https://github.com/inclement/kivycrashcourse/blob/",
                "master/video14-using_a_screenmanager/after.py"))
        Button:
            text: "Carpe diem!"
            size_hint: root.manager.sizeHintBigX
            on_press:
                root.manager.transition.direction = root.manager.transDirL
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = 'MainMenu'

<Help>:
    name:'Help'
    BoxLayout:
        Button:
            text: "Back"
            size_hint: root.manager.sizeHintSmallX
            on_press:
                root.manager.transition.direction = root.manager.transDirD
                root.manager.transition.duration = root.manager.transDur
                root.manager.current = root.returnPage
        Button:
            text: root.labelText
''')

# keep the window size constant
Config.set('graphics','resizable',0)
Window.size = (1000, 150)

# Well! Finally running the app!
class DeepMareApp(App):
    def build(self):
        return root_widget

DeepMareApp().run()