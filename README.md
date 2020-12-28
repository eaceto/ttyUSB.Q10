# ttyUSB.Q10
An USB Interface for BlackBerry's Q10 keyboard and BlackBerry's trackball

# Hardware

BlackBerry devices has (IMHO) the best-in-class hardware keyboard. Also the trackball it's a nice replacement for a mouse in a portable device. I found a board created by [@arturo192](https://twitter.com/arturo182) which exposes a BB Q10 Keyboard over an I2C protocol. I decided to create this small project in order to use this keyboard, and a trackball, but over USB. 

Creating an USB interface is a step I have to in order to interface this keyboard with a Raspberry Pi Zero W, which will be the main board of my Palmtop device. Eventhought the Pi Zero W has an I2C port, I will use of the available ports for a hi resolution display.

# Software

This application is not just a replacement of the I2C interface of the BB Q10 PMOD because introduce some features that are not available in the standard BlackBerry's Keyboard interface, for example:

* Controlling the backlight brightness
* Emulating keyboard arrows
* Adding cut, copy and paste shortcuts.

Among other features that I will be implementing during the development of this project.

# Reference board

The reference board used in this project is the Adafruit Trinket M0 which uses an ATSAMD21E18 32-bit Cortex M0+ CPU.

## Connection

| Keyboard PMOD | Trinket M0 |
|---------------|------------|
| 3V3           | 3V3        |
| GND           | GND        |
| SDA           | SDA        |
| SCL           | SCL        |
| INT           | A0         |


# Implemented Features

- [X] Controlling the backlight brightness
- [X] Function keys (F1 to F9 and F12)
- [X] Act as Apple Keyboard
- [X] Emulating keyboard arrows
- [X] Undu, cut, copy and paste.
- [_] Handle keys repeat
- [_] [Complete Documentation](https://eaceto.github.io/ttyUSB.Q10)

## Controlling the backlight brightness

The following combination of keys will increase or decrease the brightness of the backlight keyboard. The brightness goes from 0 to 100% in 20% steps. 

Press and hold **Shift** then **Sym**

* Press and release **A** to decrease the brightness

* Press and release **Q** to increase the brightness

## Function keys (F1 to F9 and F12)

Function keys are very useful, from asking for help (F1) to closing a windows (Alt + F4), but also when booting a computer in order to access BIOS / EFI, or boot disk menu (F2, F9, F12...).

The mapping that I have deviced for this keyboard implemented only F1 to F9 and F12. All this function keys can be press by:

Press and hold **Shift** then **Sym** 

* Press and release **1** to **9** for F1 to F9 (keys: w, e, r, s, d, f, z, x, c)

* Press and release **0** for F12 (the mic Key)

## Act as Apple Keyboard

Setting **_act_as_apple_keyboard** to **True** replaces Control Key with Command Key for **cut, copy and paste** actions. This feature should be translated to a hardware configuration (pin in low or high state).

## Emulating keyboard arrows

As the BlackBerry Q10 keyboard does not have built-in arrows key, the emulation of these keys is done by using the **Sym** key plus **a** (left), **s** (down), **d** (right), **w** (up). This four keys are widely used in video games.

This combination of keys supports repeat. So holding down **Sym** plus any of the arrow keys, while result in a repetition of the key pressed.

## Undo, cut, copy and paste

Undo, cut, copy and paste is implemented by holding the **Sym** key and pressing:

* **z** for Undo
* **x** for Cut
* **c** for Copy
* **v** for Paste

# Links to components

- [@arturo182 BlackBerry Q10 Keyboard PMOD](https://www.tindie.com/products/arturo182/bb-q10-keyboard-pmod/)
- [Pimoroni Trackball Brakeout](https://shop.pimoroni.com/products/trackball-breakout)

# Support and Contact

- [Blog](https://eaceto.dev)
- [Linkedin](https://www.linkedin.com/in/ezequielaceto/)
- [E-mail](mailto:eaceto@pm.me) 
