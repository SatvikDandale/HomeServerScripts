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

        
        assert(os.path.isdir(sourceFolder))
        assert(os.path.isdir(targetFolder))

        if (sourceFolder == targetFolder):
            print("Both paths are same.")
            raise Exception()

        return sourceFolder, targetFolder

    except:
        raise Exception("Check the arguments supplied.")


def getAllFiles(sourceFolder):
    filesArray = []
    print("=== Generating a list of all the files in the source folder. ===")
    for path, subdirs, files in os.walk(sourceFolder):
        for name in files:
            # print(os.path.join(path, name))
            filesArray.append(os.path.join(path, name))
    print("=== The list is generated. ===")
    print("=== Total number of files are: {}. ===".format(len(filesArray)))
    return filesArray

sourceFolder, targetFolder = getArguments()
filesArray = getAllFiles(sourceFolder)

