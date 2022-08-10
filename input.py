import RPi.GPIO as GPIO

BUTTON_A_PIN = 9 #MOSI
BUTTON_B_PIN = 10 #MISO
BUTTON_C_PIN = 11 #SCLK
BUTTON_E_PIN = 7 #CE0   
BUTTON_D_PIN = 8 #CE1

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_C_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_D_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_E_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def getInputOptions():
    btn_a_pressed = False
    btn_b_pressed = False
    btn_c_pressed = False
    btn_d_pressed = False
    btn_e_pressed = False

    def handleButton(isPressed, thenDo):
        if isPressed:
            thenDo()
    def btnAHandler():
        nonlocal btn_a_pressed
        btn_a_pressed = True
        print("Button A Pressed")
    def btnBHandler():
        nonlocal btn_b_pressed
        btn_b_pressed = True
        print("Button B Pressed")
    def btnCHandler():
        nonlocal btn_c_pressed
        btn_c_pressed = True
        print("Button C Pressed")
    def btnDHandler():
        nonlocal btn_d_pressed
        btn_d_pressed = True
        print("Button D Pressed")
    def btnEHandler():
        nonlocal btn_e_pressed
        btn_e_pressed = True
        print("Button E Pressed")
        
    handleButton(not GPIO.input(BUTTON_A_PIN), btnAHandler)
    handleButton(not GPIO.input(BUTTON_B_PIN), btnBHandler)
    handleButton(not GPIO.input(BUTTON_C_PIN), btnCHandler)
    handleButton(not GPIO.input(BUTTON_D_PIN), btnDHandler)
    handleButton(not GPIO.input(BUTTON_E_PIN), btnEHandler)

    return btn_a_pressed, btn_b_pressed, btn_c_pressed, btn_d_pressed, btn_e_pressed