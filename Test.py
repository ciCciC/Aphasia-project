from store import datastore

# f = wave.open(file_path, 'r')

# with io.open(file_path, 'rb') as audio_file:
#     contentSize = audio_file.read()

# signal = contentSize
# signal = np.fromstring(signal, 'Int16')

# plt.figure(1)
# plt.title('Signal Wave...')
# plt.plot(signal)
# plt.show()


# filedirectory = os.path.join(os.path.dirname(__file__),'temporary/')
#
# print(filedirectory)
#
# file_name = os.path.join(
#             os.path.dirname(__file__),
#             'audio', 'Bestandnaam.mp3')
#
# sound = AudioSegment.from_mp3(file_name)
#
# nieuweBestandnaam = 'nieuweBestandnaam'
#
# AudioTranscribe.exportAudio(sound,
#                             filedirectory,
#                             nieuweBestandnaam,
#                             'wav')

# def drawGraph(data):
#     data1 = []
#     data2 = []
#     for x in data:
#         data1.append(x[0])
#         data2.append(x[1])
#
#     colors = np.random.rand(120)
#     # plt.figure(1)
#     plt.title('Signal Wave...')
#     # plt.scatter(data2, data1, c=colors, alpha=5.5)
#     figure = plt.gcf()
#     plt.subplot()
#     plt.stem(data2, data1)
#     plt.show()
#     figure.savefig('signal_wave_dbfs.png')


audioName = 'haunted'
format = 'mp3'

datastore.datastore.addAudioFile(source_file_name=audioName, fileFormat=format)

datastore.datastore.list_storage_files()
