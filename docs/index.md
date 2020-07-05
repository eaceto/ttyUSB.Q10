---
layout: default
---

An USB Interface for BlackBerry's Q10 keyboard and BlackBerry's trackball.

# Purpose

It was the summer of 1998 (I was 13 years old) when I first owned a Psion Series 5 PDA, and since then, I have been thinking about creating my own PDA. The first version was developed using an ATMega1284p, a 4x4 keypad with a T9-like text input, and a small screen. Since then I have been looking for displays, SoCs and keyboards in order to create a more powerful and portable version.

And here I am, in 2020, during a quarentine, with a positive test of COVID 19, and the idea of creating a linux-powered paltop device.

# Hardware

BlackBerry devices has (IMHO) the best-in-class hardware keyboard. Also the trackball it's a nice replacement for a mouse in a portable device. I found a board created by [@arturo192](https://twitter.com/arturo182) which exposes a BB Q10 Keyboard over an I2C protocol. I decided to create this small project in order to use this keyboard, and a trackball, but over USB. 

Creating an USB interface is a step I have to in order to interface this keyboard with a Raspberry Pi Zero W, which will be the main board of my Palmtop device. Eventhought the Pi Zero W has an I2C port, I will use of the available ports for a hi resolution display.

# Software

This application is not just a replacement of the I2C interface of the BB Q10 PMOD because introduce some features that are not available in the standard BlackBerry's Keyboard interface, for example:

* Controlling the backlight brightness
* Emulating keyboard arrows
* Adding cut, copy and paste shortcuts.

Among other features that I will be implementing during the development of this project.

# Links to components

- [@arturo182 BlackBerry Q10 Keyboard PMOD](https://www.tindie.com/products/arturo182/bb-q10-keyboard-pmod/)
- [Pimoroni Trackball Brakeout](https://shop.pimoroni.com/products/trackball-breakout)


# Support and Contact

- [Blog](https://eaceto.dev)
- [Linkedin](https://www.linkedin.com/in/ezequielaceto/)
- [E-mail](mailto:eaceto@pm.me) 
