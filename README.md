# FlipDigitClockPython
![wiring](https://raw.githubusercontent.com/lucblender/FlipDigitClockPython/main/ressources/clock.png)
## Description

This library has for goal to control the FlipDigit clock composed of 6 [Small 7-segment displays](https://flipdots.com/en/products-services/small-7-segment-displays/) by alfazeta with a Raspberry Pi.

The clock was designed to be used with Particle Electron. This library although is designed to control the clock with a Raspberry Pi which is more common and more accessible than the Particle.

## Install

The module is available on pip:
```
pip install flipdigitclock
```

## Requirement

If you install the library with pip, the required package are installed automatically. If you use the library from sources, the only library needed for this to work is RPi.GPIO. Basic installation can be made like so:

```pip3 install RPi.GPIO```

or by using the provided requirments.txt file:

```pip3 install -r requirments.txt```


## Wiring

You will need to connect GPIOs of the Raspberry Pi to the Particle Electron Slot. The default wiring is the following:

![wiring](https://raw.githubusercontent.com/lucblender/FlipDigitClockPython/main/ressources/wiring.png)

This wiring can be change in the constructor of the FlipDigitClock object which is the following:

``` clock =  FlipDigitClock(A_DIG = 25, B_DIG = 5, C_DIG = 6, SET_DIG_EN = 12, RES_DIG_EN = 13, A_SEG = 19, B_SEG = 16, C_SEG = 26, SET_SEG_EN = 20, RES_SEG_EN = 21)```

## How to use

### Drive segment

### Drive digit

### More examples

## License

Under MIT license. Please see [License File](https://github.com/lucblender/FlipDigitClockPython/blob/main/LICENSE) for more information.