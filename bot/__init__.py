import sys

# check python version
if sys.version_info < (3, 5, 1):
    print("elonusbot requires Python 3.5.1 or newer.")
    sys.exit(1)
