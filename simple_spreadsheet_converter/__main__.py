#!/usr/bin/env python3

if __name__ == "__main__":
    import sys
    from .SimpleGlossaryConverter import SimpleGlossaryConverter

    c = SimpleGlossaryConverter(sys.argv[2])
    c.convert(sys.argv[1], *sys.argv[3:])
