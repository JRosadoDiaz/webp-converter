import os
from PIL import Image
from filetype import FileType as FT


def scanFiles(directory):
    files = []
    for item in os.listdir(directory):
        if item.endswith(".webp"):
            files.append(item)

    return files


def moveFile(directory, targetFile):
    webpFolder = directory + '/WEBP'
    if not os.path.isdir(webpFolder):
        os.mkdir(directory + "/WEBP")

    os.replace(directory + '/' + targetFile, webpFolder + '/' + targetFile)


def deleteFile(directory, targetFile):
    os.remove(directory + "/" + targetFile)


def convert(directory, targetFile, fileType):
    im = Image.open(directory + '/' + targetFile)
    if fileType == FT.JPEG:
        im.save(directory + "/" + targetFile.replace(".webp", ".jpg"), "jpeg")
    elif fileType == FT.PNG:
        im.save(directory + "/" + targetFile.replace(".webp", ".png"), "png")
