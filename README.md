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

**.update_buff(`col`)**
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

 Arg     | Type       | Description                                 | Default
---------|------------|---------------------------------------------|--------------
**buff** | memoryview | the contents to write to the display RAM    | **REQUIRED**
**x**    | int        | the x location to begin the write           | **REQUIRED**
**y**    | int        | the y location to begin the write           | **REQUIRED**
**w**    | int        | the width to write                          | **REQUIRED**
**h**    | int        | the height to write                         | **REQUIRED**
