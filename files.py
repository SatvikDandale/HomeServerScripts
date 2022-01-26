import os, time, shutil, datetime, glob
import getopt, sys

"""
    The command line arguments should include:
        1. The source folder path (absolute if possible)
        2. The taget folder path
"""

def getArguments():
    try:
        # The first argument is the current script file
        argumentList = sys.argv[1:]
        print(argumentList)
        assert len(argumentList) == 2

        sourceFolder = ""
        targetFolder = ""
        for argument in argumentList:
            if "--sourceFolder" in argument:
                sourceFolder = argument.split("=")[1]
            elif "--targetFolder" in argument:
                targetFolder = argument.split("=")[1]

        print(sourceFolder)
        print(targetFolder)
        
        assert(os.path.isdir(sourceFolder))
        assert(os.path.isdir(targetFolder))

    except:
        raise Exception("Check the arguments supplied.")


getArguments()