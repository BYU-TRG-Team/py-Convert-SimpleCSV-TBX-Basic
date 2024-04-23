#!/usr/bin/env python3

if __name__ == "__main__":
    import sys
    from .core import Converter

    c = Converter(sys.argv[2])
    c.convert(sys.argv[1], *sys.argv[3:])
