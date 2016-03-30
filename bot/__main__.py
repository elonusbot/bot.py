import os
import sys

# store the original working directory, for use when restarting
original_wd = os.path.realpath(".")

# set up environment - we need to make sure we are in the install directory
path0 = os.path.realpath(sys.path[0] or '.')
install_dir = os.path.realpath(os.path.dirname(__file__))
if path0 == install_dir:
    sys.path[0] = path0 = os.path.dirname(install_dir)
os.chdir(path0)

from bot.bot import Bot

def main():
    __bot = Bot()

    restart = __bot.run()

    if (restart):
        # write code to restart here >.<
        return;

main()
