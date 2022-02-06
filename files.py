from genericpath import isfile
from msilib.schema import File
from operator import mod
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

def createDirectory(path: str) -> str:
    """
        It will simulate mkdir -p functionality
    """
    try:
        os.makedirs(path)
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
    return (str(date.year), conversion[date.month], date.day)

def getCreationDate(file: str):
    date = datetime.datetime.fromtimestamp(os.path.getctime(file))
    return convertDate(date)

def getModifiedDate(file: str):
    date = datetime.datetime.fromtimestamp(os.path.getmtime(file))
    return convertDate(date)

def copyFile(sourceFile: str, destinationFile: str):
    """
       sourcePath: complete path of file including the file name
       desticationPath: complete path of file including the file name
    """
    shutil.copy2(sourceFile, destinationFile)

def createCopyOfFile(sourceFile, destinationFile):
    """
        Args:
            sourceFile: /hdd/somefolder/a.txt
            destinationFile: /backup/2011/Mar/a.txt

        If a file a.txt already exists, and we have a newer file:
            then check a1.txt exists. If not, create
                else check a2.txt exists and so on.
    """
    copy = " copy "
    if not os.path.isfile(destinationFile):
        copyFile(sourceFile, destinationFile)
    else:
        destinationFile = os.path.splitext(destinationFile)[0] + str(copy) + os.path.splitext(destinationFile)[1]
        return createCopyOfFile(sourceFile, destinationFile)

def generateDestinationPath(fileName, modifiedDate, targetFolder):
    year = modifiedDate[0]
    month = modifiedDate[1]
    path = targetFolder + "/" + year + "/" + month + "/"
    return path

def differentialBackup():
    """
        CURRENTLY SINGLE THREADED OPERATION
        The steps are:
            1. Get all the files in 1 array
            2. For every file:
                a. Get its creation and modification dates
                b. Check if the destination directory exists or not. If not, then create
                c. Check if the file already exists there:
                    If yes, then get the modification and creation dates of both.
                    Compare. If not equal, then recursively create a copy of this file.
    """
    
    sourceFolder, targetFolder = getArguments()
    filesArray = getAllFiles(sourceFolder)

    for file in filesArray:
        fileName = file[1]
        filePath = file[0]
        creationDate = getCreationDate(filePath)
        modifiedDate = getModifiedDate(filePath)
        destinationPath = generateDestinationPath(fileName, modifiedDate, targetFolder)
        if not os.path.isdir(destinationPath):
            createDirectory(destinationPath)
        destinationFilePath = destinationPath + fileName
        createCopyOfFile(filePath, destinationFilePath)

    pass

differentialBackup()