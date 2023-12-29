% Параметры
packet_length = 1000;
crc_lengths = 1:30; % Различные длины CRC
num_trials = 100; % Количество испытаний для каждого CRC

% Инициализация массивов для хранения результатов
error_probabilities = zeros(length(crc_lengths), 1);

% Имитация испытаний
for i = 1:length(crc_lengths)
    crc_length = crc_lengths(i);
    errors_undetected = 0;
    
    for trial = 1:num_trials
        % Генерация случайного пакета данных
        packet = randi([0, 1], 1, packet_length);
        
        % Вычисление CRC
        generator = [1, 1, 1, 1, 1, 1, 1, 1]; % коэффициенты порождающего полинома
        remainder = crc32(packet, generator);
        
        % Внесение ошибок
        error_position = randi([1, packet_length]);
        packet(error_position) = ~packet(error_position);
        
        % Пересчет CRC
        remainder_with_error = crc32(packet, generator);
        
        % Проверка наличия ошибок
        if sum(remainder_with_error) ~= 0
            errors_undetected = errors_undetected + 1;
        end
    end
    
    % Вычисление вероятности необнаружения ошибок
    error_probabilities(i) = errors_undetected / num_trials;
end

% Построение графика
plot(crc_lengths, error_probabilities, '-o');
title('Вероятность необнаружения ошибок в зависимости от длины CRC');
xlabel('Длина CRC');
ylabel('Вероятность необнаружения ошибок');
grid on;

% Функция для вычисления CRC
function remainder = crc32(data, generator)
    data_with_zeros = [data, zeros(1, length(generator) - 1)];
    
    for i = 1:length(data)
        if data_with_zeros(i) == 1
            data_with_zeros(i:i+length(generator)-1) = xor(data_with_zeros(i:i+length(generator)-1), generator);
        end
    end
    
    remainder = data_with_zeros(end - length(generator) + 2:end);
end
