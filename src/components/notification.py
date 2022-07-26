import requests
from datetime import datetime
from rgbmatrix import graphics
from PIL import Image
from objects.scene import SCENES
from system.config import config_matrix, config_notification, secrets
from system.logger import logger

NOTIFICATION_IS_NEW = False
CURRENT_NOTIFICATION = None

FONT_TITLE = graphics.Font()
FONT_SUBTITLE = graphics.Font()

FONT_TITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-main-24.bdf") 
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 

class Notification:    
    def __init__(self, id, content, date):      
        self.id = id            
        self.content = content            
        self.date = date             
    def setId(self, id):
        self.id = id
    def getId(self):    
        return self.id
    def setContent(self, content):
        self.content = content
    def getContent(self):    
        return self.content
    def setDate(self, date):
        self.date = date
    def getDate(self):    
        return self.date

def markNotificationRead():
    global NOTIFICATION_IS_NEW
    NOTIFICATION_IS_NEW = False
    
def fetchNotification():
    global CURRENT_NOTIFICATION
    global NOTIFICATION_IS_NEW

    try:
        url = secrets["api_read-unread"]
        r = requests.post(url, data={}, headers={})
        data = r.json()
        r.close()

        messages = data['messages']
        if len(messages) > 0:
            for message in messages:
                notification = Notification(message["id"], message["content"], message["date"])

                # Only store the newest message.
                if CURRENT_NOTIFICATION == None or notification.getDate() > CURRENT_NOTIFICATION.getDate():
                    CURRENT_NOTIFICATION = notification
                    NOTIFICATION_IS_NEW = True
    except Exception as error:
        logger(error=error)
    
    return NOTIFICATION_IS_NEW

def getNotificationCanvas(cvsNotification):
    arrContent = getContentString()

    #Scene
    scene = SCENES[0]
    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    strImagePath = scene.getBMPs()[0]

    #Draw
    image = Image.open(strImagePath)
    image.thumbnail((config_matrix["width"], config_matrix["height"]), Image.ANTIALIAS)
    cvsNotification.SetImage(image.convert('RGB'))  

    i = 0
    for line in arrContent:
        i+=1
        graphics.DrawText(cvsNotification, FONT_SUBTITLE, 1, 0 + i*6, clrPrimary, line)

    return cvsNotification

def getContentString():
    contentArr = []

    def getBitWidth(char):
        if char in ["M", "W", "^"]:
            return 6
        elif char in ["N"]:
            return 5
        elif char in ["[", "]", "(", ")", "'"]:
            return 3        
        elif char in ["!", ",", "."]:
            return 2
        else:
            return 4

    #If there is a notification message that is unread. 
    if CURRENT_NOTIFICATION != None:        
        bitCount = 0
        result = ""
        for char in CURRENT_NOTIFICATION.getContent():
            if (bitCount + getBitWidth(char)) < 64:
                bitCount += getBitWidth(char)
                result += char
            else:
                contentArr.append(result)
                bitCount = 0
                result = char
        contentArr.append(result.strip())
    else:
        contentArr = ["No messages, or", "messages are", "loading..."]

    return contentArr

def getAlertCanvas(cvsAlert):
    #Scene
    scene = SCENES[0]
    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 

    graphics.DrawText(cvsAlert, FONT_TITLE, 56, 16, clrPrimary, config_notification["alert_icon"])

    return cvsAlert
