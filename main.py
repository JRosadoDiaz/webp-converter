from msilib.schema import Directory
from PIL import Image
import os


def doWork():
    repeatCheck = True

    while(repeatCheck):
        print("Enter directory to begin conversions")
        targetDirectory = input()
        filesFound = scanFiles(targetDirectory)
        print(str(len(filesFound)) + " files were found\n")

        print(
            "(1) JPEG\n" +
            "(2) PNG - This option often makes files bigger than original\n" +
            "Select which type to convert to:"
        )

        convertAns = input()

        print(
            "Delete original webp file after conversion?\n" +
            "Note: undeleted files will be moved to a new folder called 'WEBP'\n" +
            "(1) yes\n" +
            "(2) no"
        )
        deleteAns = input()

        for file in filesFound:
            convert(targetDirectory, file, convertAns)
            if deleteAns == "1":
                print("Deleting " + file)
                os.remove(targetDirectory + "/" + file)
            elif deleteAns == "2":
                print("Moving " + file)
                newFolder = targetDirectory + "/WEBP"
                if not os.path.exists(newFolder):
                    os.makedirs(newFolder)

                os.replace(targetDirectory + "/" +
                           file, newFolder + "/" + file)
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


def scanFiles(directory):
    files = []
    for item in os.listdir(directory):
        if item.endswith(".webp"):
            files.append(item)

    return files


def convert(directory, filename, convertAns):
    im = Image.open(directory + "/" + filename).convert("RGB")

    if convertAns == "1":
        im.save(directory + "/" + filename.replace(".webp", ".jpg"), "jpeg")
    elif convertAns == "2":
        im.save(directory + "/" + filename.replace(".webp", ".png"), "png")


if __name__ == "__main__":
    doWork()
