x = [0, 0, 1, 1, 0]; %6
y = [0, 1, 1, 0, 1]; %13

randmass = zeros(1, 31);
for i = 1:31 %послед Голда
    xlast = 0;
    ylast = 0;
    if x(3) ~= x(4)
        xlast = 1;
    end
    if y(2) ~= y(5)
        ylast = 1;
    end
    for j = 5:-1:2
        x(j) = x(j-1);
        y(j) = y(j-1);
    end
    x(1) = xlast;
    y(1) = ylast;
    vivod = 0;
    if x(5) ~= y(5)
        vivod = 1;
    end
    randmass(i+1) = vivod;
    fprintf('%2d : x=[%d %d %d %d %d] y=[%d %d %d %d %d] vivod=%d randmass=%d\n', i, x(1), x(2), x(3), x(4), x(5), y(1), y(2), y(3), y(4), y(5), vivod, randmass(i));
end

x1 = [0, 0, 1, 1, 1]; %7
y1 = [0, 1, 0, 0, 0]; %8
randmass1 = zeros(1, 31);
for i = 1:31 %Голд
    xlast = 0;
    ylast = 0;
    if x1(3) ~= x1(4)
        xlast = 1;
    end
    if y1(2) ~= y1(5)
        ylast = 1;
    end
    for j = 5:-1:2
        x1(j) = x1(j-1);
        y1(j) = y1(j-1);
    end
    x1(1) = xlast;
    y1(1) = ylast;
    vivod = 0;
    if x1(5) ~= y1(5)
        vivod = 1;
    end
    randmass1(i) = vivod;
    fprintf('%2d : x1=[%d %d %d %d %d] y1=[%d %d %d %d %d] vivod=%d randmass1=%d\n', i, x1(1), x1(2), x1(3), x1(4), x1(5), y1(1), y1(2), y1(3), y1(4), y1(5), vivod, randmass1(i));
end
figure
subplot(3, 1, 1);
fprintf('                                                             Корреляция x,y \n');
fprintf(' С| B1| B2| B3| B4| B5| B6| B7| B8| B9|B10|B11|B12|B13|B14|B15|B16|B17|B18|B19|B20|B21|B22|B23|B24|B25|B26|B27|B28|B29|B30|B31|А.Kор\n');
vivodlast = randmass;
autocorr_values = zeros(1, 31);
shifts = 1:36;
for k = 1:36
    fprintf('%2d', k);
    if k ~= 1
        lastvivod = randmass(31);
        for n = 1:30
            randmass(32-n) = randmass(31-n);
        end
        randmass(1) = lastvivod;
    end
    [c, lags] = xcorr(randmass, vivodlast, 35, 'normalized');
    autocorr_values(k) = c(36);
    fprintf('|%3d', randmass);
    fprintf('|%.2f\n', autocorr_values(k));
end

    plot(shifts-1, autocorr_values, '-o','Color', 'green');
    title("Корреляция x,y");
    grid on;

%figure
subplot(3, 1, 2);
fprintf('                                                             Корреляция x1,y1 \n');
fprintf(' С| B1| B2| B3| B4| B5| B6| B7| B8| B9|B10|B11|B12|B13|B14|B15|B16|B17|B18|B19|B20|B21|B22|B23|B24|B25|B26|B27|B28|B29|B30|B31|А.Kор\n');
vivodlast = randmass1;
autocorr_values = zeros(1, 31);
shifts = 1:36;
for k = 1:36
    fprintf('%2d', k);
    if k ~= 1
        lastvivod = randmass1(31);
        for n = 1:30
            randmass1(32-n) = randmass1(31-n);
        end
        randmass1(1) = lastvivod;
    end
    [c, lags] = xcorr(randmass1, vivodlast, 35, 'normalized');
    autocorr_values(k) = c(36);
    fprintf('|%3d', randmass1);
    fprintf('|%.2f\n', autocorr_values(k));
end

    plot(shifts-1, autocorr_values, '-o');
    title("Корреляция x1,y1");
    grid on;
%корреляция между двумя последовательностями Голда
subplot(3, 1, 3);

r = xcorr(randmass, randmass1);
% значение корреляции
fprintf('rhoxy = ');
disp(r(32));

% график корреляции

plot(r,'-o','Color', 'red'); % Диапазон от -31 до 31
title('График корреляции между двумя последовательностями Голда');
xlabel('Сдвиг');
ylabel('Корреляция');

