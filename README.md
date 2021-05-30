# upy-st7789


A simple st7789 driver written in micropython. This repo is still under development. The code works, but is limited in features.

### Community:

_To officially file a bug report or feature request you can use these templates:_   [bug report](https://github.com/OneMadGypsy/pupy-st7789/blob/main/.github/ISSUE_TEMPLATE/bug_report.md) | [feature request](https://github.com/OneMadGypsy/upy-st7789/blob/main/.github/ISSUE_TEMPLATE/feature_request.md)

_To discus features, bugs or share your own project that utilize code in this repo:_   [join the discussion](https://github.com/OneMadGypsy/upy-st7789/discussions/1)

<br />

-------

<br />


## Docs:


**ST7789(`spi`, `dc`, `cs`, `rst`, `bl`, `te`, `baud`, `bright`, `rot`, `buff`)**
> Main SDCard interface

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
**buff**   | memoryview | to be used as internal buffer   | None
