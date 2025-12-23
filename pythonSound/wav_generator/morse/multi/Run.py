import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write

import sys
sys.path.append('/home/roland/Desktop/Python/DSP')
import dsp

Nz=5      #kitöltőnullák
sr=10    #samprate
fs=44100    
f=1024      #modFrq
rep=1      #repeat

AGWN = 0.05

# Morse code dictionary
morse_code_dict = {
    'A': '.-',     'B': '-...',   'C': '-.-.', 
    'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',
    'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',
    'S': '...',    'T': '-',      'U': '..-',
    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..',
    '0': '-----',  '1': '.----',  '2': '..---',
    '3': '...--',  '4': '....-',  '5': '.....',
    '6': '-....',  '7': '--...',  '8': '---..',
    '9': '----.',
    ' ': '/'  # Space represented as a slash in Morse
}

# morse_binary_dict = {
#     '-': np.array([0,1,1,1]),
#     '.': np.array([0,1]),
#     ' ': np.array([0,0,0]),
#     '/': np.array([0,0,0])
# }

morse_binary_dict = {
    '-': [0,1,1,1],
    '.': [0,1],
    ' ': [0,0,0],
    '/': [0,0,0]
}

# Function to encode text to Morse code
def text_to_morse(text):
    text = text.upper()
    morse = []
    for char in text:
        code = morse_code_dict.get(char, '')  # Default to '' if not found
        morse.append(code)
    return ' '.join(morse)


def morse_to_binary(morse):
    morse = morse.upper()
    binary = []
    for char in morse:
        code = morse_binary_dict.get(char, '')  # Default to '' if not found
        binary.extend(code)
    return binary


def inc(v, R):
    w=np.zeros(len(v)*R)
    print(len(v)*R)
    for i in range(len(v)):
        for j in range(R):
            #print(i*R+j)
            #w[i*R+j]=v[i]
            w[i*R+j]=v[i]
    return(w)

def repeat(v,a):
    w=np.zeros(len(v)*a)
    for i in range(a):
        w[(i*len(v)):((i+1)*len(v))]=np.array(v)
    return(w)

def upmix(v,f,fs):
    P=np.arange(len(v))*f/fs*2*np.pi
    mix=np.exp(1j*P)
    w=v*mix
    return(w)

def dec(v,a):
    w=v[::a]
    return(w)

def resa(v,fs,b):
    w=dec(inc(v,fs),b)
    return(w)

def comp2cui8(v):
    code=np.zeros(len(v)*2)
    code[::2]=np.real(v)+128
    code[1::2]=np.imag(v)+128
    out=code.astype('uint8')
    return out

def modulation_depth_from_dB(dB:float):
    c=10**(dB/20)
    modulation_depth = (c-1)/(c+1)
    return modulation_depth

codes=[]

# frq_list=[1000, 1050, 1100, 1150, 1200, 1250]
# text_list=["NOAA ", "MANT ", "URTABOR ", "MISKOLC", "K NORBI", "K TIBOR", "KOROLJOV", "TUCSOK","KALIMBA","NEWTON"]
# text_list=["ANTAL", "BELA", "CECIL", "DENS", "ENDRE"]
text_list=["       CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ CQ"]

# text_list=["HA4RBA"]

# frq_list=[100, 1000, 10000]
# text_list=["a", "e", "e"]

# frq_list=[10, 100, 1000]
# text_list=["a", "e", "T"]

for i in range(len(text_list)):
    text=text_list[i]
    morse_code=text_to_morse(text)
    print(morse_code)
    code=morse_to_binary(morse_code)
    print(code)
    code1=np.array(code)
    code11=np.concatenate([code1,np.zeros(Nz)])
    code2=repeat(code11,rep)
    code21=np.concatenate([np.zeros(Nz),code2])
    #code3=resa(code21,fs,sr)
    code3=inc(code21,int(fs/sr))
    code4=upmix(code3,f+i*50,fs)
    # code4=upmix(code3,frq_list[i],fs)



    plt.plot(code21,'.-')
    plt.title(f'bitrate: {sr} simbol/sec, sampFrq: {fs} Hz,\n codeLen: {len(code)}, zeros: {Nz}')
    plt.grid()
    plt.savefig('code.png')
    #plt.show()
    codes.append(code4)

# Find the length of the longest array
max_len = max(len(arr) for arr in codes)

# Initialize result with zeros
result = [0] * max_len

# Add element-wise, skipping missing values
for arr in codes:
    for i in range(len(arr)):
        result[i] += arr[i]

result=np.array(result)/len(text_list)

scaled = np.int16(np.real(result) * 32767)
write(f'out.wav', fs, scaled)

result = result*(1+0.9*np.real(dsp.sines(0.05,fs,len(result))))

result=0.4*dsp.agwn(result,AGWN)
out=(np.real(result)*128+127).astype('uint8')
out.tofile("out.ui8")





# t=np.arange(len(result))/fs
# plt.figure()
# plt.plot(t,result)
# plt.xlabel("time [sec]")
# plt.ylabel("Amplitude []")
# plt.grid()
# plt.savefig("time_dom.png")
# plt.show()


# # powerspec=dsp.average_correlation_spectrum(result,result, 10000, True)
# powerspec=np.abs(np.fft.fft(result))**2
# f=np.range(len(result)


# plt.figure()
# plt.plot(np.log(powerspec))
# plt.grid()
# plt.show()