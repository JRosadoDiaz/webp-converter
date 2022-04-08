from msilib.schema import Directory
from PIL import Image
import os


def doWork():
    print("Enter directory to begin conversions")
    targetDirectory = input()
    print(targetDirectory)
    filesFound = scanFiles(targetDirectory)

    print(str(len(filesFound)) + " files were found")
    print("Delete original file after conversion? (1) yes (2) no")
    ans = input()

    for file in filesFound:
        convert(targetDirectory, file)
        if ans == "1":
            print("Deleting " + file)
            os.remove(targetDirectory + "/" + file)

    print("CONVERSIONS DONE")

    if ans == "2":
        print("Delete all webp files that were converted? (1) yes (2) no")
        answer = input()

        if answer == "1":
            print("Deleting files...")
            for file in filesFound:
                os.remove(targetDirectory + "/" + file)
        elif answer == "2":
            print("Moving files to new folder named 'WEBP'")
            newFolder = targetDirectory + "/WEBP"
            for file in filesFound:
                if not os.path.exists(newFolder):
                    os.makedirs(newFolder)

                os.replace(targetDirectory + "/" +
                           file, newFolder + "/" + file)
            print("DONE")

    print("Closing program...")


def scanFiles(directory):
    files = []
    for item in os.listdir(directory):
        if item.endswith(".webp"):
            files.append(item)

    return files


def convert(directory, filename):
    im = Image.open(directory + "/" + filename).convert("RGB")
    im.save(directory + "/" + filename.replace(".webp", ".jpg"), "jpeg")


if __name__ == "__main__":
    doWork()
