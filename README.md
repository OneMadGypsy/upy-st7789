# upy-st7789


A simple st7789 driver for 240x240 pixel IPS displays, written in micropython. This driver should be compatible with any micropython device. This repo is still under development. The driver works, but is limited in features. This driver should work with displays whether they have a `chip select` pin or not. Numerous decisions are made based on the pins that are supplied to the `ST7789` constructor.

### Community:

_To officially file a bug report or feature request you can use these templates:_   [bug report](https://github.com/OneMadGypsy/pupy-st7789/blob/main/.github/ISSUE_TEMPLATE/bug_report.md) | [feature request](https://github.com/OneMadGypsy/upy-st7789/blob/main/.github/ISSUE_TEMPLATE/feature_request.md)

_To discus features, bugs or share your own project that utilize code in this repo:_   [join the discussion](https://github.com/OneMadGypsy/upy-st7789/discussions/1)

<br />

-------

<br />

## Docs:


**ST7789(`spi`, `dc`, `cs`, `rst`, `bl`, `te`, `baud`, `bright`, `rot`, `buff`)**
> Main ST7789 interface

 Arg       | Type       | Description                      | Default
-----------|------------|----------------------------------|--------------
**spi**    | SPI        | A reference to the desired SPI   | **REQUIRED**
**dc**     | Pin        | data/command Pin                 | **REQUIRED**
**cs**     | Pin        | chip select Pin                  | None
**rst**    | Pin        | reset Pin                        | None
**bl**     | Pin        | backlight Pin                    | None
**te**     | Pin        | tearing Pin                      | None
**baud**   | int        | desired baudrate                 | 31_250_000
**bright** | int        | brightness value (0 to 255)      | 255
**rot**    | int        | rotation value (0, 90, 180, 270) | 0
**buff**   | memoryview | to be used as internal buffer    | None

<br />

### Properties

<br />

**.buffer:memoryview**
>Reference to the buffer that was supplied to the constructor or `None` if no buffer was supplied.

<br />

### Methods

<br />

**.display_en(`enable`)**

 Arg       | Type  | Description                          | Default
-----------|-------|--------------------------------------|--------------
**enable** | bool  | enable/disable display         | True

<br />

**.sleep_en(`enable`)**

 Arg       | Type  | Description                                         | Default
-----------|-------|-----------------------------------------------------|--------------
**enable** | bool  | sleep on/sleep off                          | True

<br />

**.tear_en(`enable`)**
>only operable if a tearing pin is defined

 Arg       | Type  | Description                                  | Default
-----------|-------|----------------------------------------------|--------------
**enable** | bool  | enable/disable tearing pin               | True

<br />

**.rotation(`rot`)**

 Arg       | Type  | Description                                  | Default
-----------|-------|----------------------------------------------|--------------
**rot**    | int   | rotation value (0, 90, 180, 270)        | 0

<br />

**.reset(`wait`)**
>only operable if a reset pin is defined

 Arg       | Type  | Description                                 | Default
-----------|-------|---------------------------------------------|--------------
**wait**   | int   | ms to wait between toggling display      | 10

<br />

**.backlight(`bright`)**
>only operable if a backlight pin is defined

 Arg       | Type  | Description                              | Default
-----------|-------|------------------------------------------|--------------
**bright** | int   | brightness value (0 to 255)        | 255

<br />

**.clear_buff(`col`)**
>only operable if a buffer was supplied to the constructor

 Arg       | Type  | Description                                 | Default
-----------|-------|---------------------------------------------|--------------
**col**    | int   | color to fill the buffer with         | **REQUIRED**

<br />

**.update_buff()**
>Only operable if a buffer was supplied to the constructor. This will update the display RAM with the contents of the internal buffer

<br />

**.clear(`col`, `rows`)**
>Clear the display

 Arg       | Type  | Description                                 | Default
-----------|-------|---------------------------------------------|--------------
**col**    | int   | color to fill the buffer with         | 0
**rows**   | int   | amount of rows to write at a time      | 8

<br />

**.update(`buff`, `x`, `y`, `w`, `h`)**
>update a designated portion of the display RAM with the contents of the supplied buffer

 Arg     | Type       | Description                             | Default
---------|------------|-----------------------------------------|--------------
**buff** | memoryview | contents to write to the display RAM    | **REQUIRED**
**x**    | int        | x location to begin the write           | **REQUIRED**
**y**    | int        | y location to begin the write           | **REQUIRED**
**w**    | int        | width to write                          | **REQUIRED**
**h**    | int        | height to write                         | **REQUIRED**

<br />

-------

<br />

## Usage:

<br />

**Pimoroni Pico Explorer**
>If you have a Pimoroni Pico Explorer you can instance the display as below.

```python
from machine import Pin, SPI
from st7789 import ST7789

display = ST7789(
    spi     = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT)),
    dc      = Pin(16, Pin.OUT),
    cs      = Pin(17, Pin.OUT),
    baud    = 62_500_000,
    buff    = memoryview(bytearray(115200))
)
```

<br />

**Test Script**
>The below script can be used to test that the display is working with this driver and get an idea of the performance. You will need to change my instance of `ST7789` to reflect the pins your display is connected to.

```python
from machine import Pin, SPI
from random import randint
from st7789 import ST7789

@micropython.viper
def rect(buff:ptr16, x:int, y:int, w:int, h:int, c:int):
    b, L = ptr16(buff), int(w*h)
    sx = int(x+(y*240))
    for i in range(L):
        b[sx+(240*(i//w))+i%w] = c

display = ST7789(
    spi     = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT)),
    dc      = Pin(17, Pin.OUT),
    rst     = Pin(21, Pin.OUT),
    bl      = Pin(20, Pin.OUT),
    baud    = 62_500_000,
    bright  = 0xFF,
    rot     = 0,
    buff    = memoryview(bytearray(115200))
)

class Thing:
    def __init__(self, x:int, y:int, w:int, h:int, c:int, sx:int, sy:int):
        self.x, self.y   = x, y
        self.w, self.h   = w, h
        self.sx, self.sy = sx, sy
        self.c = c
        self.xr = range(240-w+1)
        self.yr = range(240-h+1)
        
    def update(self):
        self.sx = self.sx if self.sx+self.x in self.xr else -self.sx
        self.sy = self.sy if self.sy+self.y in self.yr else -self.sy
        self.x += self.sx
        self.y += self.sy
        rect(display.buffer, self.x, self.y, self.w, self.h, self.c)
 
        
def make_things(cnt:int = 5):
    things = [0]*cnt
    for n in range(cnt):
        a = randint(20, 40)
        things[n] = Thing(randint(0, 240-a), randint(0, 240-a), a, a, randint(0xF000, 0xFFFF), randint(4, 8), randint(4, 8))
    return things      
        
things = make_things(50)

while True:
    display.clear_buff(randint(0x0000, 0x7F7F))
    
    for t in things:
        t.update()
    
    display.update_buff()
```

<br />

-------

<br />

## Tips

Overclocking a Raspberry Pi Pico can make a big difference regarding the performance you experience with this driver. Unfortunately, without making a change to the `pico-sdk`, overclocking the Pico will actually result in worse performance. If you would like to make the changes to the sdk, you can get the information in [this post](https://www.raspberrypi.org/forums/viewtopic.php?f=146&t=311664&p=1871443#p1865146). There are other posts earlier in that thread which give a lot of information regarding non-obvious behavior. To make a long story short: if you aren't willing to make the changes and rebuild the firmware **do not overclock your pico while running ANY SPI device**. You **will** take a severe performance hit if you do.


