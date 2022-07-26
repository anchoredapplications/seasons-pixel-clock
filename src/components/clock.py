from rgbmatrix import graphics
from PIL import Image
from objects.scene import SCENES
from system.config import config_matrix, config_timezone
from datetime import datetime, timedelta

FONT_TITLE = graphics.Font()
FONT_SUBTITLE = graphics.Font()
FONT_HEADING = graphics.Font()

FONT_TITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-main-24.bdf") 
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 
FONT_HEADING.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-heading-12.bdf") 

COUNT_START = None    
COUNT_END = None
COUNT_DAY = 0
COUNT_MINUTE = 0
COUNT_HOUR = 0

CALENDAR_FORMAT = 0
SELECTED_OPTION = 0
TIMEZONE_OPTION = 0

IMAGE_INDEX = 0
TICK = 1
BLINK = False

def getClockCanvas(cvsClock):
    year, month, day, hour, minute, second, weekday = getTimezone()

    strHour, strColon, strMinute = getTimeString(hour, minute, second)
    strPeriod = getPeriodString(hour)
    scene = getScene()

    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    clrTertiary = graphics.Color(scene.getTertiaryColor().R,scene.getTertiaryColor().G,scene.getTertiaryColor().B) 
    clrQuaternary = graphics.Color(scene.getQuaternaryColor().R,scene.getQuaternaryColor().G,scene.getQuaternaryColor().B) 

    #Draw
    image = getImage(scene, second)
    cvsClock.SetImage(image.convert('RGB')) 

    action = scene.getAction()
    if action != None:
        action(graphics, cvsClock, FONT_HEADING, clrPrimary, clrSecondary, year)

    ##Time
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 17, clrSecondary, strHour)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 18, clrPrimary, strHour)
    graphics.DrawText(cvsClock, FONT_TITLE, 20, 17, clrQuaternary, strColon)
    graphics.DrawText(cvsClock, FONT_TITLE, 20, 18, clrTertiary, strColon)
    graphics.DrawText(cvsClock, FONT_TITLE, 25, 17, clrSecondary, strMinute)
    graphics.DrawText(cvsClock, FONT_TITLE, 25, 18, clrPrimary, strMinute)

    ##Border + Period
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 17, clrSecondary, "___")
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 18, clrTertiary, "___")
    graphics.DrawText(cvsClock, FONT_TITLE, 42, 17, clrQuaternary, strPeriod)

    ##Date
    if CALENDAR_FORMAT == 0:
        strYear, strDay, strMonth = getDateString(year, month, day, weekday)
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 3, 29, clrPrimary, strDay)
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 11, 29, clrQuaternary, ".")
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 14, 29, clrPrimary, strMonth)
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 22, 29, clrQuaternary, ".")
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 25, 29, clrPrimary, strYear)
    elif CALENDAR_FORMAT == 1:
        strDayOfWeek, strDay, strMonth = getDayOfWeekString(year, month, day, weekday)
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 3, 29, clrPrimary, strDayOfWeek)
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 21, 29, clrQuaternary, strMonth)
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 29, 29, clrPrimary, "/")
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 33, 29, clrQuaternary, strDay)
    else:
        strDate = getMonthDayString(year, month, day, weekday)
        graphics.DrawText(cvsClock, FONT_SUBTITLE, 3, 29, clrQuaternary, strDate)

    return cvsClock

def getDateString(year, month, day, weekday):
    yearLabel =  "{year:02}".format(year=year)
    dayLabel =  "{day:02d}".format(day=day)
    monthLabel =  "{month:02d}".format(month=month,)
    
    return yearLabel, dayLabel, monthLabel

def getDayOfWeekString(year, month, day, weekday):
    dayOfWeekLabel =  "{dayOfWeek}".format(dayOfWeek=["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"][weekday])
    dayLabel =  "{day:02d}".format(day=day)
    monthLabel =  "{month:02d}".format(month=month,)
    return dayOfWeekLabel, dayLabel, monthLabel

def getMonthDayString(year, month, day, weekday):
    sup = "th"
    if day == 1:
        sup = "st"
    elif day == 2:
        sup = "nd"
    elif sup == 3:
        sup = "rd"

    dateLabel =  "{month}, {day}{sup}".format(
        month=["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"][month],
        day=day,
        sup=sup
    )
    return dateLabel

def getTimeString(hour, minute, second):
    global BLINK
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour = hour - 12
    hourLabel =  "{hour:02d}".format(hour=hour,)
    minuteLabel =  "{minute:02d}".format(minute=minute,)
    colonLabel =  " " if BLINK else ":"

    return hourLabel, colonLabel,  minuteLabel

def getPeriodString(hours):
    periodLabel = "AM" if hours < 12 else "PM"
    return periodLabel

def handleButtons_Clock(B, C, D):
    global CALENDAR_FORMAT
    global TIMEZONE_OPTION

    if B:
        CALENDAR_FORMAT = CALENDAR_FORMAT+1 if CALENDAR_FORMAT < 2 else 0
    if C:
        TIMEZONE_OPTION = TIMEZONE_OPTION+1 if TIMEZONE_OPTION < len(config_timezone["offsets"])-1 else 0
        
    global IMAGE_INDEX
    #global TESTER

    if D:
        IMAGE_INDEX = 0
        #TESTER = TESTER+1 if TESTER <= 14 else 0

#---------- Countdown ----------#
def getCountdownCanvas(cvsClock):
    year, month, day, hour, minute, second, weekday = getTimezone()

    global BLINK
    #Clock
    strDay, strHour, strMinute = getCountdownString()
    scene = getScene()

    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    clrTertiary = graphics.Color(scene.getTertiaryColor().R,scene.getTertiaryColor().G,scene.getTertiaryColor().B) 
    clrQuaternary = graphics.Color(scene.getQuaternaryColor().R,scene.getQuaternaryColor().G,scene.getQuaternaryColor().B) 
    
    white = graphics.Color(255,255,255)
    
    #Draw
    image = getImage(scene, second)
    cvsClock.SetImage(image.convert('RGB')) 

    action = scene.getAction()
    if action != None:
        action(graphics, cvsClock, FONT_HEADING, clrPrimary, clrSecondary, year)

    graphics.DrawText(cvsClock, FONT_SUBTITLE, 2, 8, clrQuaternary if SELECTED_OPTION != 0 else white, strDay)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 7, clrSecondary, "___")
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 8, clrTertiary, "___")
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 28, clrSecondary if SELECTED_OPTION != 1 else white, strHour)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 29, clrPrimary if SELECTED_OPTION != 1 else white, strHour)
    graphics.DrawText(cvsClock, FONT_TITLE, 20, 28, clrQuaternary, ":" if BLINK else "")
    graphics.DrawText(cvsClock, FONT_TITLE, 20, 29, clrTertiary, ":" if BLINK else "")
    graphics.DrawText(cvsClock, FONT_TITLE, 25, 28, clrSecondary if SELECTED_OPTION != 2 else white, strMinute)
    graphics.DrawText(cvsClock, FONT_TITLE, 25, 29, clrPrimary if SELECTED_OPTION != 2 else white, strMinute)
    
    return cvsClock

def getCountdownString():
    global COUNT_END
    global COUNT_START
    global COUNT_DAY
    global COUNT_HOUR
    global COUNT_MINUTE

    if COUNT_START != None:
        if COUNT_START > COUNT_END:
            return "00 days", "00", "00"

        duration = (COUNT_END- COUNT_START)
        days, s = duration.days, duration.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)

        dayLabel =  "{days:02d} days".format(
            days=days
        )
        hourLabel = '{:02d}'.format(int(hours))
        minuteLabel = '{:02d}'.format(int(minutes))

        return dayLabel, hourLabel, minuteLabel
    else:
        dayLabel =  "{days:02d} days".format(
            days=COUNT_DAY
        )
        hourLabel =  "{hour:02d}".format(
            hour=COUNT_HOUR
        )
        minuteLabel =  "{minute:02d}".format(
            minute=COUNT_MINUTE
        )
        return dayLabel, hourLabel, minuteLabel

def handleButtons_Countdown(B, C, D):
    global SELECTED_OPTION
    global COUNT_END
    global COUNT_START
    global COUNT_DAY
    global COUNT_HOUR
    global COUNT_MINUTE

    if B:
        SELECTED_OPTION = SELECTED_OPTION + 1 if SELECTED_OPTION < 3 else 0

    if SELECTED_OPTION == 0:
        if C:
            COUNT_DAY = COUNT_DAY+1
        if D:
            COUNT_DAY = COUNT_DAY-1 if COUNT_DAY >= 1 else 0
        COUNT_START = None
        COUNT_END = None    
    elif SELECTED_OPTION == 1:
        if C:
            COUNT_HOUR = COUNT_HOUR+1
        if D:
            COUNT_HOUR = COUNT_HOUR-1 if COUNT_HOUR >= 1 else 0
        COUNT_START = None
        COUNT_END = None    
    elif SELECTED_OPTION == 2:
        if C:
            COUNT_MINUTE = COUNT_MINUTE+1
        if D:
            COUNT_MINUTE = COUNT_MINUTE-1 if COUNT_MINUTE >= 1 else 0
        COUNT_START = None
        COUNT_END = None    
    elif SELECTED_OPTION == 3:
        COUNT_START = datetime.now()
        if B or C or D:
            COUNT_END = datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute) + timedelta(days=COUNT_DAY, hours=COUNT_HOUR, minutes=COUNT_MINUTE)

#---------- Shared ----------#
def getTimezone():
    global TIMEZONE_OPTION
    offset = config_timezone["offsets"][TIMEZONE_OPTION]
    now = datetime.utcnow() + timedelta(hours=offset)

    return now.year, now.month, now.day, now.hour, now.minute, now.second, now.weekday()

def getImage(scene, second):
    global IMAGE_INDEX
    global TICK
    global BLINK

    if TICK >= 4:
        TICK = 1 
        BLINK = not BLINK
    else:
        TICK = TICK + 1 
 
    if TICK % scene.getTempo() == 0:
        IMAGE_INDEX = 0 if IMAGE_INDEX >= len(scene.getBMPs()) - 1 else IMAGE_INDEX + 1

    if IMAGE_INDEX > len(scene.getBMPs()) - 1:
        IMAGE_INDEX = 0

    strImagePath = scene.getBMPs()[IMAGE_INDEX] 
    image = Image.open(strImagePath)
    image.thumbnail((config_matrix["width"], config_matrix["height"]), Image.ANTIALIAS)
    LAST_TICK = second
    return image

def getScene(): 
    year, month, day, hour, minute, second, weekday = getTimezone()
    christmas = month == 12 and day == 25
    christmasEve = month == 12 and day == 24
    birthday = month == 10 and day == 3
    halloween = month == 10 and day == 31
    independance = month == 7 and day == 4
    valentines = month == 2 and day == 14
    newYearsEve = month == 12 and day == 31
    newYearsDay = month == 1 and day == 1
    stPatricks = month == 3 and day == 17
    stMartins = month == 11 and day == 11

    thanksgiving = month == 11 and day == 28 - datetime(year, 7, 1).weekday()
    def isEaster(year, month, day):
        a = year % 19
        b = year // 100
        c = year % 100
        d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
        e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
        f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
        m = f // 31
        d = f % 31 + 1 
        return month == m and day == d    
    easter = isEaster(year, month, day)

    today = datetime(year, month, day)
    startOfSpring = datetime(year, 3, 20)
    startOfSummer = datetime(year, 6, 20)
    startOfFall = datetime(year, 9, 20)
    startOfWinter = datetime(year, 12, 20)

    spring = today >= startOfSpring and today < startOfSummer
    summer = today >= startOfSummer and today < startOfFall
    fall = today >= startOfFall and today < startOfWinter
    winter = today >= startOfWinter or today < startOfSpring

    if christmas or christmasEve:
        return SCENES[1]
    elif thanksgiving:
        return SCENES[2]
    elif easter:
        return SCENES[3]
    elif independance:
        return SCENES[4]        
    elif newYearsEve:
        return SCENES[5]        
    elif newYearsDay:
        return SCENES[6]        
    elif valentines:
        return SCENES[7]        
    elif stPatricks:
        return SCENES[8]        
    elif stMartins:
        return SCENES[9]    
    elif halloween:
        return SCENES[10]  
    elif birthday:
        return SCENES[11]    
    elif spring:
        return SCENES[12]
    elif summer:
        return SCENES[13]
    elif fall:
        return SCENES[14]
    elif winter:
        return SCENES[15]
    else:
        return SCENES[0]

#---------- Shared ----------#
# TESTER = 0
# def TEST():
#     global TESTER
#     return SCENES[TESTER]