from msilib.schema import File
import os
import time
import shutil
import datetime
import glob
import getopt
import sys

"""
    The command line arguments should include:
        1. The source folder path (absolute if possible)
        2. The taget folder path
"""


def getArguments():
    """
        There are 2 arguments expected:
            1. --sourceFolder=xyz
            2. --targetFolder=abc
    """
    try:
        # The first argument is the current script file
        argumentList = sys.argv[1:]
        # print(argumentList)
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
    """
        Returns a filesArray which contains all the files in the given directory and all subdirs (recursively)
        It is array of tuples: (pathOfFile + filename, filename);
    """
    filesArray = []
    print("=== Generating a list of all the files in the source folder. ===")
    for path, subdirs, files in os.walk(sourceFolder):
        for name in files:
            # print(os.path.join(path, name))
            filesArray.append((os.path.join(path, name), name))
    print("=== The list is generated. ===")
    print("=== Total number of files are: {}. ===".format(len(filesArray)))
    return filesArray

def createDirectory(path: str, name: str) -> str:
    path += "/" + name
    try:
        os.mkdir(path)
    except FileExistsError:
        print("=== The path {} already exists. ===".format(path))
    return path

def convertDate(date: datetime.datetime):
    """
        Expects a datetime object
        Returns a tuple: (year, month, day)
    """
    conversion = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep",
                  10: "Oct", 11: "Nov", 12: "Dec"}
    return (date.year, conversion[date.month], date.day)

def getCreationDate(file: str):
    date = datetime.datetime.fromtimestamp(os.path.getctime(file))
    return convertDate(date)

def getModifiedDate(file: str):
    date = datetime.datetime.fromtimestamp(os.path.getmtime(file))
    return convertDate(date)

def copyFile(sourcePath: str, destinationPath: str, file: str):
    """
       sourcePath: the path till the folder which contains the file. Not including the file name. 
       desticationPath: the path till the folder in which the file is expected
       file: just the file name
    """
    shutil.copy2(file, destinationPath + "/" + file)

sourceFolder, targetFolder = getArguments()
filesArray = getAllFiles(sourceFolder)
# createDirectory(".", "test")
# copyFile("./", "./test", "README.md")
