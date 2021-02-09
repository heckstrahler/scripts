# This Python script, converts the content a folder to .7z archives through utilizing 7zip with lzma2:9. The folder
# must ONLY contain archives supported by 7zip and nothing else. To increase overall cpu utilization decompression
# and compression runs in parallel with the decompression part being additionally multi threaded. However to decrease
# the read load on in input drive the decompression part in single threaded. First argument is the input folder, the
# second argument is the output folder.
import queue
import threading
import os
import sys
import subprocess


def decompression(name, inputQueue, outputQueue):
    while True:
        inputFile = inputQueue.get()
        subprocess.run(["echo", f'{name} is decompressing {inputFile.name}'])
        filename = inputFile.name.rsplit(".", 1)[0]
        tempFolder = f'convertTemp{filename}'
        subprocess.run(["nice", "-n", "5", "7z", "x", inputFile, f'-o{tempFolder}'], stdout=subprocess.DEVNULL)
        outputQueue.put(inputFile)
        subprocess.run(["echo", f'{name} finished decompressing {inputFile.name}'])
        inputQueue.task_done()


def compression(name, inputQueue, directory):
    while True:
        inputFile = inputQueue.get()
        subprocess.run(["echo", f'{name} is compressing {inputFile.name}'])
        filename = inputFile.name.rsplit(".", 1)[0]
        tempFolder = f'convertTemp{filename}'
        subprocess.run(
            ["nice", "-n", "5", "7z", "a", "-t7z", "-m0=lzma2", "-mx=9", "-mfb=64", "-md=64m", "-ms=on",
             f'{directory}{filename}', "-r", f'./{tempFolder}/*'], stdout=subprocess.DEVNULL)
        subprocess.run(["rm", "-r", tempFolder])
        subprocess.run(["echo", f'{name} finished compressing {inputFile.name}'])
        inputQueue.task_done()


if __name__ == "__main__":
    decompressionQueue = queue.Queue()
    compressionQueue = queue.Queue(2)

    inputDir = sys.argv[1]
    outputDir = sys.argv[2]
    for file in os.scandir(inputDir):
        decompressionQueue.put(file)

    decompressionThread = threading.Thread(target=decompression,
                                           args=(f'decompression-worker', decompressionQueue, compressionQueue))
    decompressionThread.setDaemon(True)
    decompressionThread.start()

    compressionThreads = []
    for i in range(2):
        thread = threading.Thread(target=compression, args=(f'compression-worker-{i}', compressionQueue, outputDir))
        compressionThreads.append(thread)
        thread.setDaemon(True)
        thread.start()

    decompressionQueue.join()
    compressionQueue.join()
    subprocess.run([f'echo', f'Archive Folder to 7z conversion done'])
