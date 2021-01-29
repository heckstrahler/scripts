# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import queue
import threading
import os
import sys
import subprocess


def decompression(name, inputQueue, outputQueue):
    while True:
        inputFile = inputQueue.get()
        subprocess.run(["echo", f'{name} is decompressing {inputFile}'])
        filename = inputFile.name.rsplit(".", 1)[0]
        tempFolder = 'convertTemp' + filename
        subprocess.run(["7z", "x", inputFile, "-o" + tempFolder])
        outputQueue.put(inputFile)
        inputQueue.task_done()
        subprocess.run(["echo", f'{name} finished decompressing {inputFile}'])


def compression(name, inputQueue, directory):
    while True:
        inputFile = inputQueue.get()
        subprocess.run(["echo", f'{name} is compressing {inputFile}'])
        filename = inputFile.name.rsplit(".", 1)[0]
        tempFolder = 'convertTemp' + filename
        subprocess.run(
            ["7z", "a", "-t7z", "-m0=lzma2", "-mx=9", "-mfb=64", "-md=64m", "-ms=on", directory + filename, "-r",
             "./" + tempFolder + "/*"])
        subprocess.run(["rm", "-r", tempFolder])
        inputQueue.task_done()
        subprocess.run(["echo", f'{name} finished compressing {inputFile}'])


if __name__ == "__main__":
    decompressionQueue = queue.Queue()
    compressionQueue = queue.Queue(2)

    inputDir = sys.argv[1]
    outputDir = sys.argv[2]
    for file in os.scandir(inputDir):
        decompressionQueue.put(file)
        # oldConvert()

    decompressionTask = threading.Thread(target=decompression,
                                         args=(f'worker-decompression', decompressionQueue, compressionQueue))
    decompressionTask.setDaemon(True)
    decompressionTask.start()

    compressionTasks = []
    for i in range(2):
        task = threading.Thread(target=compression, args=(f'worker-{i}-compression', compressionQueue, outputDir))
        compressionTasks.append(task)
        task.setDaemon(True)
        task.start()

    decompressionQueue.join()
    compressionQueue.join()
    subprocess.run([f'echo', f'Zip to 7z conversion done'])
