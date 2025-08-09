import numpy as np
import matplotlib.pyplot as plt

# HOW TO USE:
#
# import sys
# sys.path.append('/home/roland/Desktop/Python/DSP')
# import dsp

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

"also good for power spectrum, if two signals match"
def average_correlation_spectrum(surv, ref, correlation_length, do_avg=True):

    number_of_iterations = int(len(ref)/correlation_length)

    corr = 1j*np.zeros([correlation_length,number_of_iterations])

    for i in range(number_of_iterations):

        surv_spec   = np.fft.fftshift(np.fft.fft(surv[i*correlation_length:(i+1)*correlation_length])/correlation_length)
        ref_spec    = np.fft.fftshift(np.fft.fft(ref[i*correlation_length:(i+1)*correlation_length])/correlation_length)
        # corr        = corr + surv_spec * np.conjugate(ref_spec)
        corr[:,i]   = surv_spec * np.conjugate(ref_spec)

    if do_avg:
        out=np.mean(corr,axis=1)
        return out
    else:
        return corr

def get_delay_value(surv, ref, length_of_correlation, resolution_multiplier, get_transfer_function=False):

    avg_corr_spec = average_correlation_spectrum(surv, ref, length_of_correlation)

    avg_corr_spec = np.concatenate([1j*np.zeros(int(np.floor((resolution_multiplier-1)*len(avg_corr_spec)/2))),avg_corr_spec,1j*np.zeros(int(np.ceil((resolution_multiplier-1)*len(avg_corr_spec)/2)))])
    avg_corr_spec = np.fft.fftshift(avg_corr_spec)

    imp = np.fft.fftshift(np.fft.ifft(avg_corr_spec))
    max_idx = np.argmax(np.abs(imp))
    diff = (resolution_multiplier*length_of_correlation/2-max_idx)/resolution_multiplier

    if get_transfer_function:
        return diff, imp
    else:
        return diff

def frac_delay(vector, delay_value, resolution_multiplier):
    # vector is getting a fractionaal delay by the value of delay_value with the resolution or the resolution_multiplier
    # for example: delay value is 0.314 and resolution_multiplier is 10 then the actual delay value is int(delay_value*resolution_multiplier)/resolution_multiplier
    delay_value = delay_value * resolution_multiplier

    shifted_vector_spectrum = np.fft.fftshift(np.fft.fft(vector))
    zero_padded = np.concatenate([1j*np.zeros(int(np.floor((resolution_multiplier-1)*len(shifted_vector_spectrum)/2))),shifted_vector_spectrum,1j*np.zeros(int(np.ceil((resolution_multiplier-1)*len(shifted_vector_spectrum)/2)))])
    interpolated_signal = np.fft.ifft(np.fft.fftshift(zero_padded))

    delayed_interpolated_signal = np.roll(interpolated_signal,int(delay_value))
    out = delayed_interpolated_signal[::resolution_multiplier]

    return out


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

def filter_channel(signal, rf, fs, FIR_LEN, fc, f_sig, fft_filt=False):
    size = len(signal)
    f = (np.arange(size)/size-0.5)*fs+rf # get the vector of measurement frequencies
    
    f_mix = rf-f_sig
    downmix_array = np.exp(f_mix/fs*1j*2*np.pi*np.arange(size))

    if fft_filt:
        filtered_signal = fft_lpf((signal*downmix_array),fc)
    else:
        hx = hann_window(get_FIR_taps(fc,fs,FIR_LEN))
        hx=hx/np.sum(hx)
        # hx = hx/np.sqrt(np.sum(hx**2)/len(hx)**2)
        filtered_signal = fir_lpf((signal*downmix_array),hx)
        # filtered_signal = fft_lpf((signal*downmix_array),hx)

    return filtered_signal

def complex_plot(samples, t=None):
    if t is None:
        t=np.arange(len(samples))

    # plt.figure()
    # plt.plot(samples,'.-')
    plt.plot(t,np.real(samples),  '-',   color='C0',     alpha=1,    label="Real")
    plt.plot(t,np.imag(samples),  '-',   color='C1',     alpha=1,    label="Imag")
    plt.plot(t,np.abs(samples),   '--',   color='grey',   alpha=0.5,  label="Abs")
    plt.plot(t,-np.abs(samples),  '-',   color='grey',   alpha=0.5,  label="-Abs")
    # plt.legend()
    # plt.ylim([-128,128])
    # plt.title(title)
    plt.subplots_adjust(right=0.75)  # Adjust the right margin as needed
    # plt.subplots_adjust(top=0.75)  # Adjust the right margin as needed
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
    plt.grid()
    # Adjust layout to create more space for titles and labels
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.8, hspace=0.6)
    # plt.show()

    if t is not None:
        plt.xlabel("time [s]")

def sines(f,fs,n_samp):
    t=np.arange(n_samp)/fs
    out=np.exp(1j*2*np.pi*f*t)
    # out=np.exp(1j*2*np.real(np.pi*agwn(f*t,0.05)))
    return(out)

def incriminate(vector,inc_val):
    inc_val=int(np.floor(inc_val))
    out=np.ones(int(len(vector)*inc_val),dtype=complex)
    for idx,val in enumerate(vector):
        out[idx*inc_val:idx*inc_val+inc_val]=val
    return(out)


def modulate_harmronic(fc,fs,f_simb,vector):
    if f_simb == 0:
        out=sines(fc,fs,len(vector))
    else:
        inc_val=fs/f_simb
        out0=incriminate(vector,inc_val)
        out=out0*sines(fc,fs,len(out0))
    return out

def modulate_fm(fc,fs,f_simb,vector):
    if f_simb == 0:
        out=sines(fc,fs,len(vector))
    else:
        inc_val=fs/f_simb
        out0=incriminate(vector,inc_val)
        out1
        out=out0*sines(fc,fs,len(out0))
    return out

def get_random_bpsk(size):
    out = 2*np.random.randint(2, size=size)-np.ones(size)
    return out

def get_random_ook(size):
    out = np.random.randint(2, size=size)
    return out

def get_random_qpsk(size):
    phases = np.random.randint(4, size=size)
    out = np.exp(1j*phases*2*np.pi/4)
    return out

def get_random_npsk(size,n):
    phases = np.random.randint(n, size=size)
    out = np.exp(1j*phases*2*np.pi/n)
    return out

def get_random_manchester(size):
    size=int(np.ceil(size/2))
    bits = np.random.randint(2, size=size)
    out = np.zeros(size*2,dtype=complex)
    for idx,d in enumerate(bits):
        if d==0:
            out[idx*2]=-1
            out[idx*2+1]=1
        else:
            out[idx*2]=1
            out[idx*2+1]=-1
    return out

