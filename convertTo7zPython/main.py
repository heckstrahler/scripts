# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import os
import sys
import subprocess


def oldConvert():
    filename = file.name.rsplit(".", 1)[0]
    tempFolder = 'convertTemp' + filename
    subprocess.run(["7z", "x", file, "-o" + tempFolder])
    subprocess.run(["7z", "a", "-t7z", "-m0=lzma2", "-mx=9", "-mfb=64", "-md=64m", "-ms=on", outputDir + filename, "-r",
                    "./" + tempFolder + "/*"])
    subprocess.run(["rm", "-r", tempFolder])


async def decompressionWorker(name, decompressionQueue, compressionQueue):
    while True:
        # Get a "work item" out of the queue.
        file = await decompressionQueue.get()

        # do something
        filename = file.name.rsplit(".", 1)[0]
        tempFolder = 'convertTemp' + filename
        subprocess.run(["7z", "x", file, "-o" + tempFolder])

        await compressionQueue.put(file)
        # Notify the queue that the "work item" has been processed.
        decompressionQueue.task_done()

async def compressionWorker(name, compressionQueue, outputDir):
    while True:
        # Get a "work item" out of the queue.
        file = await compressionQueue.get()

        # do something
        filename = file.name.rsplit(".", 1)[0]
        tempFolder = 'convertTemp' + filename
        subprocess.run(
            ["7z", "a", "-t7z", "-m0=lzma2", "-mx=9", "-mfb=64", "-md=64m", "-ms=on", outputDir + filename, "-r",
             "./" + tempFolder + "/*"])
        subprocess.run(["rm", "-r", tempFolder])
        
        # Notify the queue that the "work item" has been processed.
        compressionQueue.task_done()

# Press the green button in the gutter to run the script.
async def main():
    decompressionQueue = asyncio.Queue()
    compressionQueue = asyncio.Queue(2)

    inputDir = "/home/heckstrahler/Desktop/test"  # sys.argv[1]
    outputDir = "/home/heckstrahler/Desktop/test"  #sys.argv[2]
    for file in os.scandir(inputDir):
        decompressionQueue.put_nowait(file)
        # oldConvert()
        
    decompressionTask = asyncio.create_task(decompressionWorker(f'worker-decompression', decompressionQueue, compressionQueue))
    compressionTasks = []
    for i in range(2):
        task = asyncio.create_task(compressionWorker(f'worker-{i}-compression', compressionQueue, outputDir))
        compressionTasks.append(task)

    await decompressionQueue.join()
    decompressionTask.cancel
    
    await compressionQueue.join()
    for task in compressionTasks:
        task.cancel

asyncio.run(main())
