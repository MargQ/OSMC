import numpy as np
import matplotlib.pyplot as plt

# Ввод с клавиатуры своего имени и фамилии.
name = input("Введите своё имя: ")
surname = input("Введите свою фамилию: ")

def name_to_bits(name): # Функция преобразования имени в битовую последовательность
    bits = [] # Создаем пустой список, в который будем добавлять биты.
    for char in name:
        ascii_value = ord(char) # Получаем ASCII-код символа.
        binary_value = bin(ascii_value)[2:] # Преобразуем ASCII-код в двоичное значение.
        binary_value_padded = binary_value.zfill(8) # Дополняем двоичное значение нулями слева до 8 знаков.
        bits.extend([int(bit) for bit in binary_value_padded]) # Конвертируем каждый бит в целое число и добавляем в список.
    return bits # Возвращаем список битов.

L = len(name) * 8 # Вычисляем общую длину имени в битах.
bit_sequence = name_to_bits(name) + name_to_bits(surname) # Создаем битовую последовательность путем объединения битовых последовательностей имени и фамилии.
print("Битовая последовательность name & surname: ", bit_sequence) # Выводим битовую последовательность.
#Визуализация последовательности на графике.
plt.figure(figsize=(17,6))
plt.subplot(121)
plt.plot(bit_sequence, marker='o')
plt.xlabel('Индекс')
plt.ylabel('Значение бита')
plt.title('Битовая последовательность')
# Параметры для вычисления CRC.
M = 8 # Длина генератора CRC.
G = [1, 1, 0, 0, 0, 0, 1, 1] # Полином генератора CRC.
# Функция вычисления CRC.
def calculate_crc(bit_sequence, M, G):
    crc_generator = np.zeros(M, dtype=int) # Инициализация генератора CRC нулями.
    shifted = np.copy(crc_generator)  # Создание копии генератора CRC.
    for i in range(len(bit_sequence)): # Итерация по битам входной последовательности.
        original_bit = bit_sequence[i]  # Исходный бит.
        shifted_bit = shifted[-1] # Бит, находящийся в конце сдвинутого регистра.
        crc_generator[-1] = shifted_bit ^ original_bit # Вычисление нового бита CRC.
        shifted[:-1] = shifted[1:]  # Сдвиг копии генератора CRC вправо.
        shifted[-1] = original_bit # Замена первого бита копии генератора CRC исходным битом.
    return crc_generator # Возврат результата вычисления CRC.
# Вычисление CRC.
crc = calculate_crc(bit_sequence, M, G) # Вызов функции вычисления CRC.
bit_sequence_with_crc = np.concatenate((bit_sequence, crc)) # Объединение исходной последовательности с CRC.
# Генерация последовательности Голда.
MAX = len(bit_sequence_with_crc) # Максимальное количество итераций цикла Голда.
array_x = np.zeros(5, dtype=int) # Регистр X.
array_y = np.zeros(5, dtype=int) # Регистр Y.
gold_sequence = [] # Пустой список для последовательности Голда.
for i in range(MAX): # Итерация по количеству бит в последовательности Голда.
    original_bit = array_x[4] ^ array_y[4] # Исходный бит, полученный из регистров X и Y.
    shifted_bit = original_bit # Сохранение исходного бита.
    gold_sequence.append(shifted_bit) # Добавление исходного бита в последовательность Голда.

    sum_x = array_x[0] ^ array_x[2] # Первое сложение для регистра X.
    sum_y = array_y[1] ^ array_y[3] # Второе сложение для регистра Y.

    array_x[1:] = array_x[:-1] # Сдвиг значений регистра X вправо.
    array_y[1:] = array_y[:-1] # Сдвиг значений регистра Y вправо.
    array_x[0] = sum_x # Замена первого бита регистра X полученным значением суммы.
    array_y[0] = sum_y # Замена первого бита регистра Y полученным значением суммы.

# Визуализация битовой последовательности с CRC на графике
plt.subplot(1,2,2)
plt.plot(bit_sequence_with_crc, marker='o')
plt.xlabel('Индекс')
plt.ylabel('Значение бита')
plt.title('Битовая последовательность с CRC')

N = int(input("Введите количество отсчетов на бит: ")) # Запрос колиества отсчетов на бит
def bits_to_signal(bits, N):
    signal = []
    for bit in bits:
        signal.extend([bit]*N)
    return signal

signal = bits_to_signal(bit_sequence_with_crc, N) #результат функции bits_to_signal
# Визуализация последовательности сигнала
plt.figure(figsize=(17,6))
plt.subplot(121)
plt.plot(signal)
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.title('Последовательность сигнала')
# Создание нового массива с введенным значением
index = int(input("Введите число от 0 до {}: ".format(N*(L+M+len(gold_sequence)))))
Signal = np.zeros(max(index + len(signal), 2 * N * (L + M + len(G))))
Signal[index:index + len(signal)] = signal
# Визуализация массива Signal
plt.subplot(122)
plt.plot(Signal)
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.title('Массив Signal')
# Генерация шума п.7
# Ввод значения стандартного отклонения шума с клавиатуры
sigma = float(input("Введите стандартное отклонение шума: "))
# Генерация шума с помощью нормального распределения
noise = np.random.normal(0, sigma, len(Signal))
# Сложение информационного сигнала с шумом
noisy_signal = Signal + noise
# Построение графика зашумленного принятого сигнала
plt.figure(figsize=(8, 5))
plt.subplot(121)
plt.plot(noisy_signal)
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.title('Зашумленный принятый сигнал')

# Step 8
def correlation_receiver(signal, gold_sequence):
    correlation = np.correlate(signal, gold_sequence, mode='full')
    max_index = np.argmax(correlation)
    return max_index, correlation

start_index, correlation_result = correlation_receiver(noisy_signal, gold_sequence)
print("Start Index: ", start_index)
print("Correlation Result: ", correlation_result)

# Step 9
P = 0.5
def decision_maker(signal, threshold):
    bits = []
    for i in range(0, len(signal), N):
        sample = sum(signal[i:i+N]) / N
        if sample >= (threshold + 1) / 2:
            bits.append(1)
        else:
            bits.append(0)
    return bits

decoded_bits = decision_maker(noisy_signal[start_index:], P)
print("Decoded Bits: ", decoded_bits)
 