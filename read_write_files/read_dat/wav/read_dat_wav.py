import wave
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
# parser.add_argument("file", help="file to read")
parser.add_argument("-f","--file", help="file to read from", nargs='?', type=str, required=True)
args = parser.parse_args()


# Specify the path to your WAV file
# file_path = 'path/to/your/file.wav'

from scipy.io import wavfile
samplerate, data = wavfile.read(args.file)

plt.plot(data)
plt.show()
