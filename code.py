"""
`ttyUSB.Q10`
================================================================================

CircuitPython program for interfacing a BBQ10 keyboard and trackball as HID Keyboard / Mouse over USB.

* Author(s): Ezequiel L. Aceto [eaceto@pm.me / @eaceto]

Implementation Notes
--------------------

**Hardware:**

* `BlackBerry Q10 Keyboard PMOD <https://www.tindie.com/products/17986/>`_
* `BlackBerry Trackball Breakout <https://shop.pimoroni.com/products/trackball-breakout>`_

**Software and Dependencies:**

* Arturo's BlackBerry Q10 Keyboard CircutPython library: https://github.com/arturo182/arturo182_CircuitPython_bbq10keyboard"

* Adafruit CircuitPython firmware for the supported boards: https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""


import time
import busio
import board
import digitalio
import usb_hid

from lib.adafruit_hid.keyboard import Keyboard as USBKeyboard
from lib.adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as USBKeyboardLayoutUS
from lib.adafruit_hid.keycode import Keycode as USBKeycode

from lib.eaceto_blackberry import BBQ10KeyboardConsts
from lib.eaceto_blackberry import BBQ10Keyboard

_usb_kbd = USBKeyboard(usb_hid.devices)  # Setup USB Keyboard
_usb_kbd_layout = USBKeyboardLayoutUS(_usb_kbd)  # With US Layout

_i2c = busio.I2C(board.SCL, board.SDA)  # Setup I2C Port
_q10_kbd = BBQ10Keyboard(_i2c)  # Setup Q10 keyboard I2C interface.
_q10_kbd.backlight = 0.5  # 50% backlight intensity at statup
_q10_kbd_int = digitalio.DigitalInOut(board.A0)  # Module interrupt pin
_q10_kbd_int.direction = digitalio.Direction.INPUT
_q10_kbd_int.pull = digitalio.Pull.UP

# BB Q10 keyboard should report Alt, Sym and the Shift keys pressed.
_q10_kbd.config = 0b11011111

time.sleep(0.2)  # Keyboard init time

_act_as_apple_keyboard = True


def blinkKeyboard():
    for i in range(3):
        _q10_kbd.backlight = 1.0
        time.sleep(0.15)
        _q10_kbd.backlight = 0.0
        time.sleep(0.15)


def isLetter(val):
    return (val >= 65 and val <= 90) or (val >= 97 and val <= 122)


def isNumber(val):
    return (val >= 48 and val <= 57)


def handleASCIIKey(letter, state):
    if state == BBQ10KeyboardConsts.STATE_PRESS:
        _usb_kbd_layout.write(letter)
    elif state == BBQ10KeyboardConsts.STATE_LONG_PRESS:
        pass
    elif state == BBQ10KeyboardConsts.STATE_RELEASE:
        pass
    elif state == BBQ10KeyboardConsts.STATE_IDLE:
        pass


def handleArrowKey(key, keyState):
    if keyState == BBQ10KeyboardConsts.STATE_RELEASE or keyState == BBQ10KeyboardConsts.STATE_IDLE:
        _usb_kbd.release(key)
    else:
        _usb_kbd.press(key)


def processKey(key, altOn, shiftOn, symOn):
    keyState = key[0]
    keyChar = key[1]
    keyVal = key[2]

    currentAltOn = altOn
    currentShiftOn = shiftOn
    currentSymOn = symOn

    keyPressed = (keyState == BBQ10KeyboardConsts.STATE_PRESS or keyState ==
                  BBQ10KeyboardConsts.STATE_LONG_PRESS)

    if keyVal == BBQ10KeyboardConsts.KEY_VAL_ALT:
        currentAltOn = keyPressed
    elif keyVal == BBQ10KeyboardConsts.KEY_VAL_SHIFT:
        currentShiftOn = keyPressed
    elif keyVal == BBQ10KeyboardConsts.KEY_VAL_SYM:
        currentSymOn = keyPressed

    fnKey = currentAltOn or currentShiftOn or currentSymOn

    print("Fn: ", bool(fnKey), " Sym: ", bool(currentSymOn), " Shift: ", bool(
        currentShiftOn), " Alt: ", bool(currentAltOn), keyChar, keyVal)

    if currentShiftOn == True and currentSymOn == True:
        # Special functions on key press
        if keyState == BBQ10KeyboardConsts.STATE_PRESS:
            if keyChar == 'A':  # Decrement backlight
                newValue = _q10_kbd.backlight - 0.10
                if newValue < 0:
                    newValue = 0.0
                _q10_kbd.backlight = newValue
            elif keyChar == 'Q':  # Increment backlight
                newValue = _q10_kbd.backlight + 0.10
                if newValue > 1.0:
                    newValue = 1.0
                _q10_kbd.backlight = newValue
            else:  # F1 to F10
                fnSwitcher = {
                    'W': USBKeycode.F1,
                    'E': USBKeycode.F2,
                    'R': USBKeycode.F3,
                    'S': USBKeycode.F4,
                    'D': USBKeycode.F5,
                    'F': USBKeycode.F6,
                    'Z': USBKeycode.F7,
                    'X': USBKeycode.F8,
                    'C': USBKeycode.F9,
                    '~': USBKeycode.F12,
                }
                fnKey = fnSwitcher.get(keyChar, None)
                if fnKey != None:
                    print("Fn", int(fnKey))
                    _usb_kbd.send(fnKey)

    elif currentSymOn == True:
        if keyChar == 'a':  # left
            handleArrowKey(USBKeycode.LEFT_ARROW, keyState)
        if keyChar == 's':  # down
            handleArrowKey(USBKeycode.DOWN_ARROW, keyState)
        if keyChar == 'd':  # right
            handleArrowKey(USBKeycode.RIGHT_ARROW, keyState)
        if keyChar == 'w':  # up
            handleArrowKey(USBKeycode.UP_ARROW, keyState)
        if keyState == BBQ10KeyboardConsts.STATE_PRESS:
            if keyChar == 'z':  # undo
                if _act_as_apple_keyboard == True:
                    _usb_kbd.send(USBKeycode.COMMAND, USBKeycode.Z)
                else:
                    _usb_kbd.send(USBKeycode.CONTROL, USBKeycode.Z)
            if keyChar == 'x':  # cut
                if _act_as_apple_keyboard == True:
                    _usb_kbd.send(USBKeycode.COMMAND, USBKeycode.X)
                else:
                    _usb_kbd.send(USBKeycode.CONTROL, USBKeycode.X)
            if keyChar == 'c':  # copy
                if _act_as_apple_keyboard == True:
                    _usb_kbd.send(USBKeycode.COMMAND, USBKeycode.C)
                else:
                    _usb_kbd.send(USBKeycode.CONTROL, USBKeycode.C)
            if keyChar == 'v':  # past
                if _act_as_apple_keyboard == True:
                    _usb_kbd.send(USBKeycode.COMMAND, USBKeycode.V)
                else:
                    _usb_kbd.send(USBKeycode.CONTROL, USBKeycode.V)
    elif isLetter(keyVal) or isNumber(keyVal):
        handleASCIIKey(keyChar, keyState)
    else:
        pass

    return (currentAltOn, currentShiftOn, currentSymOn)

    print("---")


# Function keys
_fnShiftOn = False
_fnAltOn = False
_fnSymOn = False

while True:
    if _q10_kbd_int.value == True:
        continue

    try:
        key_count = _q10_kbd.key_count
        if key_count > 0:
            for i in range(key_count):
                key = _q10_kbd.keys[i]
                fnState = processKey(key, _fnAltOn, _fnShiftOn, _fnSymOn)

                _fnAltOn = fnState[0]
                _fnShiftOn = fnState[1]
                _fnSymOn = fnState[2]

    except Exception as e:
        print("exception", e)

        _value = _q10_kbd.backlight
        blinkKeyboard()
        _q10_kbd.backlight = _value

        _usb_kbd.release_all()
        _fnAltOn = False
        _fnShiftOn = False
        _fnSymOn = False
