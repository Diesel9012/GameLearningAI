import ctypes
import time

SendInput = ctypes.windll.user32.SendInput
#Hex Keycode
DictionaryofKeys = {
'KEY_LEFT' : 0x25,
'KEY_UP' : 0x26,
'KEY_DOWN' : 0x27,
'KEY_RIGHT' : 0x28,
'KEY_0' : 0x30,
'KEY_1' : 0x31,
'KEY_2' : 0x32,
'KEY_3' : 0x33,
'KEY_4' : 0x34,
'KEY_5' : 0x35,
'KEY_6' : 0x36,
'KEY_7' : 0x37,
'KEY_8' : 0x38,
'KEY_9' : 0x39,
'KEY_A' : 0x41,
'KEY_B' : 0x42,
'KEY_C' : 0x43,
'KEY_D' : 0x44,
'KEY_E' : 0x45,
'KEY_F' : 0x46,
'KEY_G' : 0x47,
'KEY_H' : 0x48,
'KEY_I' : 0x49,
'KEY_J' : 0x4A,
'KEY_K' : 0x4B,
'KEY_L' : 0x4C,
'KEY_M' : 0x4D,
'KEY_N' : 0x4E,
'KEY_O' : 0x4F,
'KEY_P' : 0x50,
'KEY_Q' : 0x51,
'KEY_R' : 0x52,
'KEY_S' : 0x53,
'KEY_T' : 0x54,
'KEY_U' : 0x55,
'KEY_V' : 0x56,
'KEY_W' : 0x57,
'KEY_X' : 0x58,
'KEY_Y': 0x59,
'KEY_Z' : 0x5A
}

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def getKeyforOutput(char):
    keycode = 'KEY_'+char
    PressKey(DictionaryofKeys[keycode])

def getKeyforRelease(char):
    keycode = 'KEY_'+char
    ReleaseKey(DictionaryofKeys[keycode])	