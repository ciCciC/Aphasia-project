import glob, csv

import librosa
import numpy as np


def readDict(filepath):
    with open(filepath, 'r') as csvfile:
        return [sentence for sentence in csv.DictReader(csvfile)]


def getFiles(folderpath, amount=None):
    files = glob.glob(folderpath + '*')
    size = len(files)
    return files[0:amount if amount is not None else size]


def getTime(seconds, sample_rate):
    return int(seconds * sample_rate)


def getRegions(audio, side, boundary, frame_size, sample_rate):
    leftRegion = []
    rightRegion = []

    if 'L' in side:
        for walk in range(0, 5):
            frame = boundary - (frame_size * walk)
            left = getTime(frame - frame_size, sample_rate)
            right = getTime(frame, sample_rate)
            tmpRegion = audio[left:right]
            leftRegion.append(tmpRegion)

    if 'R' in side:
        for walk in range(0, 5):
            frame = boundary + (frame_size * walk)
            left = getTime(frame, sample_rate)
            right = getTime(frame + frame_size, sample_rate)
            tmpRegion = audio[left:right]
            rightRegion.append(tmpRegion)

    return leftRegion if 'L' in side else rightRegion


def exportAudio(region, folderpath, name, sample_rate):
    exportName = folderpath + name + ".wav"
    librosa.output.write_wav(exportName, region, sample_rate)


def exportAudios(regions, folderpath, name, sample_rate):
    for index, region in enumerate(regions):
        exportAudio(region, folderpath, name+str(index+1), sample_rate)


def exportDataCSV(region, label, diphone, sample_rate, writer):
    region = '|'.join(['{:}'.format(x) for x in region])
    writer.writerow({'region': region, 'label': label, 'diphone': diphone, 'sample_rate': sample_rate})


def exportDatasCSV(regions, label, diphone, sample_rate, writer):
    for region in regions:
        exportDataCSV(region, label, diphone, sample_rate, writer)


diphoneDir = '/Users/koray/PycharmProjects/AphasiaProject/diphones/'
folderpath = '/Users/koray/PycharmProjects/AphasiaProject/textfilestest/'
files = getFiles(folderpath)

subRegion = 0.100
tsubRegion = subRegion / 2
region = 0.500

with open(folderpath + 'dataset.csv', 'w') as toWrite:

    fieldnames = ['region', 'label', 'diphone', 'sample_rate']
    writer = csv.DictWriter(toWrite, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, delimiter=',')

    writer.writeheader()

    for x in range(0, len(files)-(len(files)-1), 1):

        filedict = readDict(files[x])
        audiopath = filedict[0]['audiopath']

        audio, sample_rate = librosa.load(audiopath)

        count = 1
        while count < len(filedict):
            prevW = filedict[count - 1]
            currW = filedict[count]

            boundaryL = float(prevW['end'])
            boundaryR = float(currW['begin'])

            phonemeL = prevW['word'][-1]
            phonemeR = currW['word'][0]

            tsubRegionL = audio[getTime(boundaryL-tsubRegion, sample_rate):getTime(boundaryL, sample_rate)]
            tsubRegionR = audio[getTime(boundaryR, sample_rate):getTime(boundaryR + tsubRegion, sample_rate)]

            nRegionL = getRegions(audio, 'L', boundaryL - tsubRegion, subRegion, sample_rate)
            nRegionR = getRegions(audio, 'R', boundaryR + tsubRegion, subRegion, sample_rate)

            tRegion = np.concatenate((tsubRegionL, tsubRegionR), axis=None)


            # Export to CSV
            exportDataCSV(tRegion, 1, phonemeL+phonemeR, sample_rate, writer)

            exportDatasCSV(nRegionL, 0, 'nan', sample_rate, writer)
            exportDatasCSV(nRegionR, 0, 'nan', sample_rate, writer)

            # Export as audiosegments
            # exportAudio(tRegion, diphoneDir, 'tRegion'+str(count), sample_rate)
            #
            # exportAudios(nRegionL, diphoneDir, 'fRegionL'+str(count), sample_rate)
            # exportAudios(nRegionR, diphoneDir, 'fRegionR'+str(count), sample_rate)

            count += 1

print('finished')