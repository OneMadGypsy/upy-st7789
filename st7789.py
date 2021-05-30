from machine import Pin, SPI, PWM
from utime import sleep_ms as tsleep_ms
from math import log as mlog
import gc

_SWRST   = b'\x01'
_SLPIN   = b'\x10'
_SLPOUT  = b'\x11'
_NORON   = b'\x13'
_COLMOD  = b'\x3A'
_MADCTL  = b'\x36'
_INVON   = b'\x21'
_DISPOFF = b'\x28'
_DISPON  = b'\x29'
_CASET   = b'\x2A'
_RASET   = b'\x2B'
_RAMWR   = b'\x2C'
_TEOFF   = b'\x34'
_TEON    = b'\x35'

class ST7789(object):
    @property
    def buffer(self) -> memoryview:
        return self.__buff
        
    def __init__(self, spi:SPI, dc:Pin, cs:Pin=None, rst:Pin=None, bl:Pin=None, te:Pin=None, baud:int=31_250_000, bright:int=0xFF, rot:int=0, buff:memoryview=None) -> None:
        try:
            master = spi.MASTER
        except AttributeError:
            spi.init(baudrate=baud, phase=0, polarity=(1 if cs is None else 0))
        else:
            spi.init(master, baudrate=baud, phase=0, polarity=(1 if cs is None else 0))
        
        self.__spi    = spi
        self.__cs     = cs
        self.__dc     = dc
        self.__buff   = buff
        self.__width  = 240
        self.__height = 240

        self.__rst = rst
        self.reset()   #reset display if a reset pin is defined
        
        self.__te = te
        self.tear_en() #enable tearing if a tearing pin was defined
        
        #configure backlight if a pin was provided
        self.__bl = None
        if isinstance(bl, Pin):
            self.__bl = PWM(bl)
            self.backlight(bright)

        self.__command(_SWRST), tsleep_ms(150)  #software reset
        self.sleep_en(False)                    #sleep mode off
        
        #16 bits per pixel RGB565
        self.__command(_COLMOD, b'\x05'), tsleep_ms(10)   
        
        self.rotation(rot)      #config memory address
        
        self.__command(_INVON), tsleep_ms(10)   #inversion on
        self.__command(_NORON), tsleep_ms(10)   #normal on
        self.display_en()                       #display on
        
    def __command(self, cmd, data=None, n:int=0) -> None:
        #_> convert cmd to bytes if int
        cmd = cmd if not isinstance(cmd, int) else cmd.to_bytes(1, 'big')
        #_> convert data to bytes if int
        if isinstance(data, int):
            n = n if n else (1 if not data else int(mlog(data, 256)) + 1)
            data = data.to_bytes(n, 'big')
         
        #_> write cmd and data
        cs = isinstance(self.__cs, Pin)
        if cs: self.__cs(0)
            
        self.__dc(0), self.__spi.write(cmd)
        if data: self.__dc(1), self.__spi.write(data)
            
        if cs: self.__cs(1)
        
    def __set_win_addr(self, x:int, y:int, w:int, h:int) -> None:
        self.__command(_CASET, (self.__startx + x << 16) | (self.__startx + w - 1), 4)
        self.__command(_RASET, (self.__starty + y << 16) | (self.__starty + h - 1), 4)
    
    ##__>           ENABLE/DISABLE FEATURES         <__##
    
    #__> ENABLE DISPLAY
    #_      @param enable:bool True|False enable display
    def display_en(self, enable:bool=True) -> None:
        self.__command(_DISPON if enable else _DISPOFF), tsleep_ms(10)
    
    #__> SET SLEEP MODE
    #_      @param enable:bool True|False sleep|dont sleep   
    def sleep_en(self, enable:bool=True) -> None:
        self.__command(_SLPIN if enable else _SLPOUT), tsleep_ms(10)
    
    #__> ENABLE TEARING PIN
    #_      @param enable:bool True|False enable tearing pin
    def tear_en(self, enable:bool=True) -> None:
        self.__command(_TEON if enable else _TEOFF) if isinstance(self.__te, Pin) else self.__command(_TEOFF) 
        
    #__> ROTATE DISPLAY
    #_      @param rot:int - amount to rotate in 90 degree increments. negative values are allowed
    def rotation(self, rot:int) -> None:
        cmd, self.__startx, self.__starty = ((0x00,0,0),(0xA0,320-self.__width,0),(0xC0,0,320-self.__height),(0x60,0,0))[(rot+360)//90%4]
        self.__command(_MADCTL, cmd, 1)
         
    #__> RESET DEVICE
    #_      @param wait:int - ms to wait between toggling display
    def reset(self, wait:int=10) -> None:
        if isinstance(self.__rst, Pin):
            for n in (1, 0, 1): self.__rst(n), tsleep_ms(wait)
        
    #__> SET BACKLIGHT BRIGHTNESS
    #_      @param bright:int - 0 to 255
    def backlight(self, bright:int=255) -> None:
        if isinstance(self.__bl, PWM):
            self.__bl.duty_u16(int(((min(bright, 255) / 255) ** 2.8) * 65534))
       
    ##__>           INTERNAL BUFFER INTERFACE           <__##
    
    #__> FILL INTERNAL BUFFER WITH REQUESTED COLOR
    #_      @param col:int - 16 bit color to fill internal buffer with
    @micropython.viper
    def clear_buff(self, col:int): #cheat like you mean it
        try:
            L = int(len(self.__buff))//4
            if L:
                b = ptr32(self.__buff)
                c = (col << 16) | col 
                for n in range(L):
                    b[n] = c
                return
        except TypeError:
            print('No Buffer')
     
    #__> UPDATE DISPLAY WITH INTERNAL BUFFER CONTENTS
    def update_buff(self) -> None:
        if not self.__buff is None:
            self.__set_win_addr(0, 0, self.__width, self.__height)
            self.__command(_RAMWR, self.__buff)
            return
        raise ValueError('No Buffer')
    
    ##__>           EXTERNAL BUFFER INTERFACE           <__##     
    
    #__> FILL DISPLAY RAM WITH REQUESTED COLOR
    #_      @param col:int  - 16 bit color to fill display ram with
    #_      @param rows:int - amount of rows to fill on each iteration
    def clear(self, col:int=0, rows:int=8):
        rows = max(rows, 1)
        col  = col.to_bytes(2, 'big')
        mv   = memoryview(bytearray(col*(self.__width*rows)))
        for r in range(self.__height//rows):
            self.update(mv, 0, r*rows, self.__width, self.__height)
        gc.collect()
         
    #__> UPDATE REQUESTED DISPLAY AREA WITH buff
    #_      @param buff:memoryview   - buffer to fill requesteeed area with
    #_      @params (x, y, w, h):int - area properties
    def update(self, buff:memoryview, x:int, y:int, w:int, h:int) -> None:
        self.__set_win_addr(x, y, w, h)
        self.__command(_RAMWR, buff)
