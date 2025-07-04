import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write


Nz=5      #kitöltőnullák
sr=5    #samprate
fs=44100    
f=1024      #modFrq
rep=1      #repeat

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


# textlist=["HA4RBA", "MANT", "URTABOR", "MISKOLC"]
# for i in range(len(textlist)):
text="HA4RBA"
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
code4=upmix(code3,f,fs)


plt.plot(code21,'.-')
plt.title(f'bitrate: {sr} simbol/sec, sampFrq: {fs} Hz,\n codeLen: {len(code)}, zeros: {Nz}')
plt.grid()
plt.savefig('code.png')
#plt.show()


scaled = np.int16(code4 * 32767)
write('out.wav', fs, scaled)
