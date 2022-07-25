import RPi.GPIO as GPIO

SHOW_DAY_OF_WEEK = False

BUTTON_A_PIN = 9 #MISO
BUTTON_B_PIN = 10 #MOSI
BUTTON_C_PIN = 11 #SCLK
BUTTON_D_PIN = 18
BUTTON_E_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_C_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_D_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_E_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def getInputOptions():
    global SHOW_DAY_OF_WEEK
    
    def handleButton(isPressed, thenDo):
        if isPressed:
            thenDo()

    def btnAHandler():
        print("Button A Pressed")
        SHOW_DAY_OF_WEEK = not SHOW_DAY_OF_WEEK
    def btnBHandler():
        print("Button B Pressed")
    def btnCHandler():
        print("Button C Pressed")
    def btnDHandler():
        print("Button D Pressed")
    def btnEHandler():
        print("Button E Pressed")
        
    handleButton(not GPIO.input(BUTTON_A_PIN), btnAHandler)
    handleButton(not GPIO.input(BUTTON_B_PIN), btnBHandler)
    handleButton(not GPIO.input(BUTTON_C_PIN), btnCHandler)
    handleButton(not GPIO.input(BUTTON_D_PIN), btnDHandler)
    handleButton(not GPIO.input(BUTTON_E_PIN), btnEHandler)

    return SHOW_DAY_OF_WEEK