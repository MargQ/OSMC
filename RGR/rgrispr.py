import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftshift


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):                      # перевод из текста в биты
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):                    # перевод из битов в текст
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def CRC(data):
    G = [1,0,1,0,0,1,1,1]
    data = data + 7 * [0]
    for i in range(0,len(data)-7):
        if(data[i] == 1):
            for j in range(len(G)):
                data[i+j] = data[i+j] ^ G[j]
    crc = data[len(data)-7:]

    return crc


def CRC_RX(data):
    G = [1,0,1,0,0,1,1,1]
    for i in range(0,len(data)-7):
        if(data[i] == 1):
            for j in range(len(G)):
                data[i+j] = data[i+j] ^ G[j]
    crc = data[len(data)-7:]

    return crc    


def CRC_error(crc):
    f = 0
    for i in range(len(crc)):
        if crc[i] == 1:
            f = 0
            print("Error data!")
            break
        else:
            f = 1
    if f == 1:
        print("Successful!")

    

def Gold():
    x = [0,1,1,1,1] 
    y = [1,0,1,1,0]
    last_x = []
    last_y = []
    psevdo = []

    size = 31

    for i in range(size):
        #print(x)
        last_x.append(x[4])
        temp_x = x[2] ^ x[3]
        x = x[-1:] + x[:-1]
        x[0] = temp_x
        
        last_y.append(y[4])
        temp_y = y[1] ^ y[2]
        y = y[-1:] + y[:-1]
        y[0] = temp_y

    for i in range(size):   
        psevdo.append(last_x[i] ^ last_y[i])
    return psevdo 

def Correlat(gold, signal):
    max = 0
    for j in range(len(signal)-len(gold)):
        corr_sum = np.correlate(gold, signal[:(len(gold))])
        if corr_sum > max:
            max = corr_sum
            index = j
        signal = np.roll(signal,-1)
    return index

def demodulation_symbol(signal):
    for i in range(len(signal)):
        if signal[i]>0.5:
            signal[i]=1
        else:
            signal[i]=0
    return signal

def Spectrum_NS_first(mass_bit_np_gold_crc,mass_np_samples,signal,signal_noise_orig):   
    spectrum_ns_20_tx = fft(signal)
    spectrum_ns_20_rx = fft(signal_noise_orig)

    ns = 10 
    mass_np_samples_10 = np.repeat(mass_bit_np_gold_crc,ns)
    signal1_10 = np.zeros(len(mass_np_samples))
    signal_10 = np.insert(signal1_10, index, mass_np_samples_10)
    noise = np.random.normal(mu, sigma, len(signal_10))
    signal_noise_10 = signal_10 + noise

    spectrum_ns_10_tx = fft(signal_10)
    spectrum_ns_10_rx = fft(signal_noise_10)

    ns = 50 
    mass_np_samples_50 = np.repeat(mass_bit_np_gold_crc,ns)
    signal1_50 = np.zeros(len(mass_np_samples))
    signal_50 = np.insert(signal1_50, index, mass_np_samples_50)
    noise = np.random.normal(mu, sigma, len(signal_50))
    signal_noise_50 = signal_50 + noise

    spectrum_ns_50_tx = fft(signal_50)
    spectrum_ns_50_rx = fft(signal_noise_50)

    plt.figure(10)
    plt.subplot(3,2,1)
    plt.title("RX (NS = 20) ")
    plt.plot(spectrum_ns_20_rx)
    plt.subplot(3,2,2)
    plt.title("TX (NS = 20)")
    plt.plot(spectrum_ns_20_tx)

    plt.subplot(3,2,3)
    plt.title("RX (NS = 10) ")
    plt.plot(spectrum_ns_10_rx)
    plt.subplot(3,2,4)
    plt.title("TX (NS = 10)")
    plt.plot(spectrum_ns_10_tx)

    plt.subplot(3,2,5)
    plt.title("RX (NS = 50) ")
    plt.plot(spectrum_ns_50_rx)
    plt.subplot(3,2,6)
    plt.title("TX (NS = 50)")
    plt.plot(spectrum_ns_50_tx)    

def Spectrum_NS_second(mass_bit_np_gold_crc,mass_np_samples,signal,signal_noise_orig):   
    w = np.linspace(-np.pi,np.pi,len(signal))
    spectrum_ns_20_tx = fft(signal)
    spectrum_ns_20_tx = fftshift(spectrum_ns_20_tx)
    spectrum_ns_20_rx = fft(signal_noise_orig)
    spectrum_ns_20_rx = fftshift(spectrum_ns_20_rx)
    
    ns = 10 
    mass_np_samples_10 = np.repeat(mass_bit_np_gold_crc,ns)
    signal1_10 = np.zeros(len(mass_np_samples))
    signal_10 = np.insert(signal1_10, index, mass_np_samples_10)
    noise = np.random.normal(mu, sigma, len(signal_10))
    signal_noise_10 = signal_10 + noise

    spectrum_ns_10_tx = fft(signal_10)
    spectrum_ns_10_tx = fftshift(spectrum_ns_10_tx)
    spectrum_ns_10_rx = fft(signal_noise_10)
    spectrum_ns_10_rx = fftshift(spectrum_ns_10_rx)



    ns = 50 
    mass_np_samples_50 = np.repeat(mass_bit_np_gold_crc,ns)
    signal1_50 = np.zeros(len(mass_np_samples))
    signal_50 = np.insert(signal1_50, index, mass_np_samples_50)
    noise = np.random.normal(mu, sigma, len(signal_50))
    signal_noise_50 = signal_50 + noise

    spectrum_ns_50_tx = fft(signal_50)
    spectrum_ns_50_tx = fftshift(spectrum_ns_50_tx)
    spectrum_ns_50_rx = fft(signal_noise_50)
    spectrum_ns_50_rx = fftshift(spectrum_ns_50_rx)

    plt.figure(10)
    plt.subplot(1,2,1)
    plt.title("RX")
    print(len(w))
    print(len(spectrum_ns_10_rx))
    plt.plot(spectrum_ns_20_rx,"r")
    plt.plot(spectrum_ns_10_rx,"g")
    plt.plot(spectrum_ns_50_rx,"y")
    plt.subplot(1,2,2)
    plt.title("TX")
    plt.plot(spectrum_ns_50_tx, "y")
    plt.plot(spectrum_ns_20_tx, "r")
    plt.plot(spectrum_ns_10_tx, "g")
    # plt.subplot(1,2,2)
    # plt.title("TX")
    # plt.plot(w,abs(spectrum_ns_50_tx), "y")
    # plt.plot(w,abs(spectrum_ns_20_tx), "r")
    # plt.plot(w,abs(spectrum_ns_10_tx), "g")
    

    plt.legend (('NS=20', 'NS=10', "NS=50"))
    
def Sigma(sigma, signal,mass_bit_list_crc, mass_np_samples):
    ratio = []
    ns = 20
    #print(len(sigma))
    for i in range(len(sigma)):

        noise = np.random.normal(mu, sigma[i], len(signal))
        signal_noise = signal + noise
        signal_noise = signal_noise[401:]
        signal_noise = signal_noise[:len(mass_np_samples)]
        de_signal = demodulation_symbol(signal_noise)
        signal_2D = de_signal.reshape(-1, ns)
        bit_gold_crc = signal_2D[:,1]
        bit_crc = bit_gold_crc[31:]
        bit_crc = list(bit_crc)
        bit_list = list(map(int,bit_crc))
        good = 0

        for j in range(len(bit_list)):
            if mass_bit_list_crc[j] == bit_crc[j]:
                good +=1
        ratio.append(good)

    ratio = np.asarray(ratio)
    ratio = ratio / len(bit_crc)
    #print(ratio)  
    return ratio        
