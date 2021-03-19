import sys
from importlib import import_module

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify lab #")
        sys.exit(1)
    import_module(sys.argv[1]).main(sys.argv[2:])
