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
 Arg       | Type  | Description                          | Default
-----------|-------|--------------------------------------|--------------
**enable** | bool  | sleep on/sleep off                  | True

<br />

**.tear_en(`enable`)**
 Arg       | Type  | Description                                  | Default
-----------|-------|----------------------------------------------|--------------
**enable** | bool  | enable/disable tearing pin              | True

<br />

**.rotation(`rot`)**
 Arg       | Type  | Description                         | Default
-----------|-------|-------------------------------------|--------------
**rot**    | int   | rotation value (0, 90, 180, 270)   | 0

<br />

**.reset(`wait`)**
 Arg       | Type  | Description                         | Default
-----------|-------|-------------------------------------|--------------
**wait**   | int   | ms to wait between toggling display | 10

<br />

**.backlight(`bright`)**
 Arg       | Type  | Description                          | Default
-----------|-------|--------------------------------------|--------------
**bright** | int   | brightness value (0 to 255)      | 255
