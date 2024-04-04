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

def complex_plot(samples):
    plt.figure()
    # plt.plot(samples,'.-')
    plt.plot(np.real(samples),  '-',   color='C0',     alpha=1,    label="Real")
    plt.plot(np.imag(samples),  '-',   color='C1',     alpha=1,    label="Imag")
    plt.plot(np.abs(samples),   '--',   color='grey',   alpha=0.5,  label="Abs")
    plt.plot(-np.abs(samples),  '-',   color='grey',   alpha=0.5,  label="-Abs")
    plt.legend()
    # plt.ylim([-128,128])
    # plt.title(title)
    plt.grid()
    # plt.show()