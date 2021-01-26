# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import sys
import subprocess

inputdir = ''
outputdir = ''

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputdir = sys.argv[1]
    outputdir = sys.argv[2]
    print('Inputdir: ', os.listdir(inputdir), ' Outputdir: ', os.listdir(outputdir))

    for file in os.scandir(inputdir):
        filename = file.name.rsplit(".", 1)[0]
        tempfolder = 'converTemp'+filename
        subprocess.run(["7z", "x", file, "-o"+tempfolder])
        subprocess.run(["7z", "a", "-t7z", "-m0=lzma2", "-mx=9", "-mfb=64", "-md=64m", "-ms=on", outputdir+filename,
                        "-r", "./"+tempfolder+"/*"])
        subprocess.run(["rm", "-r", tempfolder])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
