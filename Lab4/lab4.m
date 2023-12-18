%x = [0, 0, 1, 1, 0]; %6
%y = [0, 1, 1, 0, 1]; %13
x = [0, 0, 1, 1, 1]; %7
y = [0, 1, 0, 0, 0]; %8

% Массивы для хранения оригинальной и сдвинутой последовательностей
original = zeros(1, 31);
shifted = zeros(1, 31);

% Заполнение массива результатов операции XOR и сохранение оригинала
for i = 1:31
    original(i) = xor(x(5), y(5));
    shifted(i) = xor(x(5), y(5));

    sumx = xor(x(4), x(5));
    x = [sumx, x(1:4)];

    sumy = xor(y(2), y(5));
    y = [sumy, y(1:4)];
end

% Вывод заголовка таблицы
fprintf('Сдвиг |         Биты         | Автокорреляция\n');

corr = xcorr(original, 'coeff');
% Вывод строк таблицы

figure;
plot(corr);

for shift = 0:31
    fprintf('%5d | ', shift);

    % Вывод битов оригинала
    for i = 1:31
        fprintf('%d', shifted(i));
    end

    fprintf(' | ');

    % Используйте abs для избежания ошибки выхода за пределы массива
    autocorr_value = corr(abs(length(original) - shift) + 1);

    fprintf('%+1.3f\n', autocorr_value);

    % Сдвиг массива
    shifted = [shifted(end), shifted(1:end-1)];
end