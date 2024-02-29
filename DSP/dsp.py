import numpy as np
import matplotlib.pyplot as plt

def get_FIR_taps(fc,fs,LEN):
    f=fc/fs
    x=np.arange(-LEN//2,LEN//2)+0.5
    hx=2*fc/fs*np.sin(2*np.pi*f*x)/(2*np.pi*f*x)/2
    return(hx)

def fir_lpf(v,hx):
    out=np.convolve(v,hx, mode='same')
    return(out)

def fft_lpf(v,fc_relative):
    size=len(v)
    spec0=np.fft.fft(v)
    spec0[fc_relative:-fc_relative] = 0
    out=np.fft.ifft(spec0)
    return(out)


def hann_window(v):
    wind=(1-np.cos(np.arange(len(v))/len(v)*2*np.pi))/2
    return(wind*v)

def agwn(v,A):
    # A=np.sum(np.abs(v)**2)/10**(SNR/10)
    out=v+np.random.normal(0,A/np.sqrt(2),len(v))+1j*np.random.normal(0,A/np.sqrt(2),len(v))
    return(out)


# def get_CPI(ref_idx, path: str, channels=None) -> np.ndarray:

#     # Load cpi
#     # iq_samples = iq.load_cpi(path)[0]
#     iq_samples = iq.load_iq(path)[0]

#     ref_ch, surv_chs = chprep.isolate_channels( iq_samples, ref_idx) #cfg['hw_config']['ref_ch_index'] )
#     chan_num =  len(surv_chs) if channels is None else channels

#     # memory allocation
#     out = 1j*np.zeros( (chan_num+1, len(ref_ch) ) )

#     out[0,:]    = ref_ch
#     out[1::,:]  = surv_chs

#     return out


# def get_cpi_shape(ref_idx):
    
#     # Load files
#     if CPI_PROCESS_LIMIT == -1:
#         cpi_files = list_files(list_of_cpis)
#     else:
#         cpi_files = list_files(list_of_cpis)[:CPI_PROCESS_LIMIT]

#     if len(cpi_files) == 0:
#         raise ValueError("No IQ files found in {}".format(iq_path))

#     # return the shape of a cpi
#     cpi_shape = np.shape(get_CPI(ref_idx, cpi_files[0]))
#     channel_number  = cpi_shape[0]
#     cpi_size        = cpi_shape[1]

    # return channel_number, cpi_size


# def get_filter_tools(cpi_size, station_number):

#     # Allocate array for mixing signals to mix differnt stations to DC
#     downmix_array = 1j*np.zeros([station_number, cpi_size]) # get the array for downmixing different stations

#     f = (np.arange((-cpi_size/2),cpi_size/2)/cpi_size*fs0+f_rf)/1e6 # get the vector of measurement frequencies

#     for station_idx in range(station_number):
#         f_mix = f_rf-station_frqs[station_idx]*1e6
#         downmix_array[station_idx,:] = np.exp(f_mix/fs0*1j*2*np.pi*np.arange(cpi_size))

#     hx = hann_window(get_FIR_taps(fc,fs0,FIR_LEN))

#     return f, downmix_array, hx

def filter_channel(signal, rf, fs, FIR_LEN, fc, f_sig):
    size = len(signal)
    f = (np.arange(size)/size-0.5)*fs+rf # get the vector of measurement frequencies
    
    f_mix = rf-f_sig
    downmix_array = np.exp(f_mix/fs*1j*2*np.pi*np.arange(size))

    hx = hann_window(get_FIR_taps(fc,fs,FIR_LEN))
    hx=hx/np.sum(hx)
    # hx = hx/np.sqrt(np.sum(hx**2)/len(hx)**2)

    filtered_signal = fir_lpf((signal*downmix_array),hx)
    # filtered_signal = fft_lpf((signal*downmix_array),hx)

    return filtered_signal

def complex_plot(samples):
    plt.figure()
    # plt.plot(samples,'.-')
    plt.plot(np.real(samples),  '-',   color='C0',     alpha=1,    label="Real")
    plt.plot(np.imag(samples),  '-',   color='C1',     alpha=1,    label="Imag")
    plt.plot(np.abs(samples),   '--',   color='grey',   alpha=0.5,  label="Abs")
    plt.plot(-np.abs(samples),  '--',   color='grey',   alpha=0.5,  label="-Abs")
    plt.legend()
    # plt.ylim([-128,128])
    # plt.title(title)
    plt.grid()
    # plt.show()