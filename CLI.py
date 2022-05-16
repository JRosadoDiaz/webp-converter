import converter
import filetype as FT
import os


def doWork():
    repeatCheck = True

    while(repeatCheck):
        print("Enter directory to begin conversions")
        targetDirectory = input()
        filesFound = converter.scanFiles(targetDirectory)
        print(str(len(filesFound)) + " files were found\n")

        print(
            "(1) JPEG\n" +
            "(2) PNG - This option often makes files bigger than original\n" +
            "Select which type to convert to:"
        )

        convertAns = input()
        fileType = None
        if convertAns == "1":
            fileType = FT.JPEG
        elif convertAns == "2":
            fileType = FT.PNG

        print(
            "Delete original webp file after conversion?\n" +
            "Note: undeleted files will be moved to a new folder called 'WEBP'\n" +
            "(1) yes\n" +
            "(2) no"
        )
        deleteAns = input()

        for file in filesFound:
            converter.convert(targetDirectory, file, fileType)
            if deleteAns == "1":
                print("Deleting " + file)
                converter.deleteFile(targetDirectory, file)
            elif deleteAns == "2":
                print("Moving " + file)
                converter.moveFile(targetDirectory, file)
        print("CONVERSIONS DONE\n")
        print("Do another folder?\n(1) yes\n(2) no")
        repeatAns = input()
        if repeatAns == "1":
            repeatCheck = True
        elif repeatAns == "2":
            repeatCheck = False

        if(repeatCheck == False):
            break

    print("Closing program...")
