import csv
import os
import json
import glob

class reader:

    @staticmethod
    def getfilename(file):
        return file.split('/')[-1].split('.')[0]

    @staticmethod
    def getFile(filename, extension):
        path = '/Users/koray/PycharmProjects/AphasiaProject/'
        path += filename + '.' + extension
        return glob.glob(path)[0]

    @staticmethod
    def getResourcePath(text=None, audio=None, output=None):
        file = audio if audio is not None else text if text is not None else output
        dir = 'audio/' if audio is not None else 'text/' if text is not None else 'output/'

        filepath = os.path.join(
            os.path.dirname(__file__),
            'data/'+dir, file)

        return filepath

    @staticmethod
    def exportToCSV(file, newFilename):

        with open(reader.getResourcePath(output=file)) as f:
            with open('/Users/koray/PycharmProjects/aeneasproject/data/output/'+ newFilename + '.csv', 'w') as csvfile:
                data = json.load(f)

                fieldnames = ['begin', 'end', 'zin']
                writer = csv.writer(csvfile, delimiter='\t')
                writer.writerow(fieldnames)

                for fragment in data["fragments"]:
                    writer.writerow([fragment['begin'], fragment['end'], fragment['lines'][0]])
                    print('begin:{}, end:{}, zin:{}'.format(fragment['begin'], fragment['end'], fragment['lines'][0]))


    @staticmethod
    def exportToDict(file, newFilename):
        with open(reader.getResourcePath(output=file)) as f:
            with open('/Users/koray/PycharmProjects/aeneasproject/data/output/' + newFilename + '.csv', 'w') as csvfile:
                data = json.load(f)

                fieldnames = ['begin', 'end', 'zin']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for fragment in data['fragments']:
                    writer.writerow({fieldnames[0]:fragment['begin'], fieldnames[1]:fragment['end'], fieldnames[2]:fragment['lines'][0]})

    @staticmethod
    def readCSV(file):
        with open(file, 'r') as csvfile:
            # skip first row
            next(csvfile)

            for row in reader:
                print(','.join(row))
                print('begin:{}, end:{}'.format(row['begin'], row['end']))

    @staticmethod
    def readDict(file):
        with open(file, 'r') as csvfile:
            lijst = []
            reader = csv.DictReader(csvfile)

            for x in reader:
                lijst.append({'begin': x['begin'],'end':x['end'], 'word':x['word']})

            return lijst


    @staticmethod
    def readJson(file):
        with open(reader.getResourcePath(output=file), 'r') as f:
            data = json.load(f)
            print(type(data))
            yield data


    @staticmethod
    def readJsonFullPath(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            yield data


    @staticmethod
    def createJsonFile(name, extension):
        with open(name + '.' + extension, 'w') as jsonfile:
            jsonfile.close()