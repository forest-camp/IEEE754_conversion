# IEEE754_conversion

## Introduction

A useful tool to convert float/half between hex and bin type.

## Quick start

Just type in terminal
```shell
python fp16_cvt.py 0x3fff
```
you will get:
```
                                SIGN           EXP                          MAN
Value :                          0              0                       1.9990234375
Encoded as :                     0              15                          1023
Binary :                         0          0 1 1 1 1               1 1 1 1 1 1 1 1 1 1
Decimal representation:        -1.9990234375
Binary Representation:         0b0011111111111111
Hexadecimal Representation:    0x3fff

```
or:
```shell
python fp32_cvt.py 0x7fffffff
```
you will get:
```
                                SIGN             EXP                                    MAN
Value :                          0               128                             1.9999998807907104
Encoded as :                     0               255                                  8388607
Binary :                         0         1 1 1 1 1 1 1 1         1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
Decimal representation:        -6.805646932770577e+38
Binary Representation:         0b01111111111111111111111111111111
Hexadecimal Representation:    0x7fffffff
**************************************************************************************************************
                                                Not a Number!
**************************************************************************************************************

```

## Some useful links

https://www.h-schmidt.net/FloatConverter/IEEE754.html

http://weitz.de/ieee/
