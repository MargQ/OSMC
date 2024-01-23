import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftshift

# Преобразование имени и фамилии в битовую строку ASCII-кодов
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):                      # перевод из текста в биты
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):                    # перевод из битов в текст
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def CRC(data):
    G = [1,1,1,1,1,1,1,1]
    data = data + 7 * [0]
    for i in range(0,len(data)-7):
        if(data[i] == 1):
            for j in range(len(G)):
                data[i+j] = data[i+j] ^ G[j]
    crc = data[len(data)-7:]

    return crc

def CRC_RX(data):
    G = [1,1,1,1,1,1,1,1]
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
    x = [0,0,1,1,0] 
    y = [0,1,1,0,1]
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

def Gold2():
    x = [0,0,1,1,1] 
    y = [0,1,0,0,1]
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

def compute_correlat(gold, signal):
    correlation_result = np.correlate(signal, gold, mode='full')
    max_corr = np.max(correlation_result)
    # поделим результат корреляции на максимальное значение в этом результате
    normalized_corr = correlation_result / max_corr
    return normalized_corr

def demodulation_symbol(signal):
    for i in range(len(signal)):
        if signal[i]>0.5:
            signal[i]=1
        else:
            signal[i]=0
    return signal
    
def Spectrum(mass_bit_np_gold_crc,mass_np_samples,signal,signal_noise_orig):   
    w = np.linspace(-np.pi,np.pi,len(signal))
    spectrum_ns_20_tx = fft(signal)
    spectrum_ns_20_tx = fftshift(spectrum_ns_20_tx)
    spectrum_ns_20_rx = fft(abs(signal_noise_orig))
    spectrum_ns_20_rx = fftshift(abs(spectrum_ns_20_rx))
    
    ns = 10 
    mass_np_samples_10 = np.repeat(mass_bit_np_gold_crc,ns)
    signal1_10 = np.zeros(len(mass_np_samples))
    signal_10 = np.insert(signal1_10, index, mass_np_samples_10)
    noise = np.random.normal(mu, sigma, len(signal_10))
    signal_noise_10 = signal_10 + noise
    w2 =  np.linspace(-np.pi,np.pi,len(signal_10))


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
    w3 =  np.linspace(-np.pi,np.pi,len(signal_50))

    spectrum_ns_50_tx = fft(signal_50)
    spectrum_ns_50_tx = fftshift(spectrum_ns_50_tx)
    spectrum_ns_50_rx = fft(signal_noise_50)
    spectrum_ns_50_rx = fftshift(spectrum_ns_50_rx)

    plt.figure(10)
    plt.xlabel('Частота, рад')
    plt.ylabel('Амплитуда')
    plt.subplot(1,1,1)
    plt.title("RX")
    print(len(w))
    print(len(spectrum_ns_10_rx))
    plt.plot(w3, abs(spectrum_ns_50_rx),"y")
    plt.plot(w, abs(spectrum_ns_20_rx),"r")
    plt.plot(w2, abs(spectrum_ns_10_rx),"g")
    
    plt.figure(11)
    plt.xlabel('Частота, рад')
    plt.ylabel('Амплитуда')
    plt.subplot(1,1,1)
    plt.title("TX")
    plt.plot(w3, abs(spectrum_ns_50_tx),"y")
    plt.plot(w, abs(spectrum_ns_20_tx),"r")
    plt.plot(w2, abs(spectrum_ns_10_tx),"g")
    plt.legend (('NS=20', 'NS=10', "NS=50"))
    
name = 'Boborykina Margarita'

bit_name = text_to_bits(name)

# Преобразование битовой строки bit_name в список целых чисел (int)
mass_bit_list = list(map(int,bit_name))
# Преобразование в массив
mass_bit_np = np.array(mass_bit_list)

# Вычисление CRC для битовой строки
print("CRC = ", CRC(mass_bit_list))
# Генерация последовательности Голда
print("Gold = ", Gold())
# Генерация последовательности Голда2
print("Gold2 = ", Gold2())
# Конкатенация последовательностей Голда, данных и CRC
mass_bit_list_gold_crc = Gold() + mass_bit_list + CRC(mass_bit_list) + Gold2()
print("Data = ", mass_bit_list_gold_crc)
print("Data длина = ",len(mass_bit_np))
print("Data + golds + crc длина = ",len(mass_bit_list_gold_crc))
mass_bit_np_gold_crc = np.array(mass_bit_list_gold_crc)

plt.figure(1)
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.plot(mass_bit_np)
plt.title("Последовательность нулей и единиц")


plt.figure(2)
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.plot(mass_bit_np_gold_crc)
plt.title("Последовательность Голда + Data + CRC")

# repeat
ns = 20 
mass_np_samples = np.repeat(mass_bit_np_gold_crc,ns)

plt.figure(3)
plt.xlabel('Отсчеты')
plt.ylabel('Амплитуда')
plt.plot(mass_np_samples)
plt.title("Временные отсчеты")

signal1 = np.zeros(len(mass_np_samples))

# Индекс, по которому будет вставлен в массив (якобы введенный с клавиатуры)
index = 101
signal = np.insert(signal1, index, mass_np_samples)

plt.figure(4)
plt.xlabel('Отсчеты')
plt.ylabel('Амплитуда')
plt.plot(signal)
plt.title("Сигнал")

# 7
mu = 0
sigma = 0.1
noise = np.random.normal(mu, sigma, len(signal))
signal_noise = signal + noise
signal_noise_orig = signal_noise
plt.figure(5)
plt.xlabel('Отсчеты')
plt.ylabel('Амплитуда')
plt.plot(signal_noise)
plt.title("Сигнал с шумом")

# 8
gold = np.repeat(Gold(),ns)
signal = signal.astype(int)

index_srez = Correlat(gold,signal_noise)

signal_noise = signal_noise[index_srez:]
signal_noise = signal_noise[:len(mass_np_samples)]

print(len(signal_noise))
plt.figure(6)
plt.xlabel('Отсчеты')
plt.ylabel('Амплитуда')
plt.title("Декодированные биты + CRC")
plt.plot(signal_noise)

# 9
de_signal = demodulation_symbol(signal_noise)

plt.figure(7)
plt.xlabel('Отсчеты')
plt.ylabel('Амплитуда')
plt.title("Демодуляция символов")
plt.plot(de_signal)

signal_2D = de_signal.reshape(-1, ns)
bit_gold_crc = signal_2D[:,1]

plt.figure(8)
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.title("Последовательность Голда + Декодированные биты + CRC")
plt.plot(bit_gold_crc)

# 10
bit_crc = bit_gold_crc[len(Gold()):]

plt.figure(9)
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.title("Декодированные биты + CRC")
plt.plot(bit_crc)

# 11
bit_crc = list(bit_crc)
print("data+crc",len(bit_crc))
print("Проверка crc")
CRC_error(CRC_RX(list(map(int,bit_crc))))

# 12
bit = bit_crc[:len(mass_bit_list)]
print(len(bit))

plt.figure(12)
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.title("Декодированные биты")
plt.plot(bit)
bit = list(map(int,bit))

bit = "".join(map(str, bit))
decode_name = text_from_bits(bit)
print(decode_name)
# 13
Spectrum(mass_bit_np_gold_crc,mass_np_samples,signal,signal_noise_orig)

correlation_result = compute_correlat(gold, signal_noise_orig)
plt.figure(13)
plt.plot(correlation_result)
plt.title("График корреляции")


plt.show()  