f1=6;
f2=14;
f3=13;

t = linspace(1, 100, 100);

S1(t) = cos(2*pi*f1*(t/100));
S2(t) = cos(2*pi*f2*(t/100));
S3(t) = cos(2*pi*f3*(t/100));

a1(t) = 4*S1(t) + 4*S2(t) + S3(t); %условие исходя из варианта
b1(t) = S1(t) + 1;
mult=0;
suma=0;
sumb=0;
for n = 1:100
    mult=mult+a1(n)*b1(n);
    suma=suma+a1(n).^2;
    sumb=sumb+b1(n).^2;
end
fprintf("\nКорреляция a1 и b1=%f\n", mult);
xmult=mult/sqrt(suma*sumb);
fprintf('Нормализованная корреляция a1 и b1=%f\n', xmult);
%2 массива значений
x21 = [1 2 3 4 5 6 7];
x22 = [1 2 3 4 5 6 7];
%условие
a2 = [0.3 0.2 -0.1 4.2 -2 1.5 0];
b2 = [0.3 4 -2.2 1.6 0.1 0.1 0.2];
rhoab2 = a2(1, 1)*b2(1, 1) + a2(1, 2)*b2(1, 2) + a2(1, 3)*b2(1, 3) + a2(1, 4)*b2(1, 4) + a2(1, 5)*b2(1, 5) + a2(1, 6)*b2(1, 6) + a2(1, 7)*b2(1, 7);
fprintf("\nКорелляция a2 и b2 = %f\n", rhoab2);
deoniatorab2=sqrt((a2(1, 1).^2 + a2(1, 2).^2 + a2(1, 3).^2 + a2(1, 4).^2 + a2(1, 5).^2 + a2(1, 6).^2 + a2(1, 7).^2)*(b2(1, 1).^2 + b2(1, 2).^2 + b2(1, 3).^2 + b2(1, 4).^2 + b2(1, 5).^2 + b2(1, 6).^2 + b2(1, 7).^2));
xrhoab2=rhoab2/deoniatorab2;
fprintf("Нормализованная корелляция a2 и b2 = %f\n", xrhoab2);
subplot(3,1,1);
plot(x21, a2, x22, b2);
title('a2, b2');
xlabel('X');
ylabel('Y');
legend('a2', 'b2');
grid on;
%сдвиг d
d = [0 0 0 0 0 0 0];
maxcor=1;
for g = 1:7
b2last7=b2(1, 7);
for n = 1:6
    b2(1, 8-n)=b2(1, 8-n-1);
end
b2(1, 1)=b2last7;
rhoab2 = a2(1, 1)*b2(1, 1) + a2(1, 2)*b2(1, 2) + a2(1, 3)*b2(1, 3) + a2(1, 4)*b2(1, 4) + a2(1, 5)*b2(1, 5) + a2(1, 6)*b2(1, 6) + a2(1, 7)*b2(1, 7);
fprintf("\nКорелляция a2 и b2(%d) = %f\n", g, rhoab2);
deoniatorab2=sqrt((a2(1, 1).^2 + a2(1, 2).^2 + a2(1, 3).^2 + a2(1, 4).^2 + a2(1, 5).^2 + a2(1, 6).^2 + a2(1, 7).^2)*(b2(1, 1).^2 + b2(1, 2).^2 + b2(1, 3).^2 + b2(1, 4).^2 + b2(1, 5).^2 + b2(1, 6).^2 + b2(1, 7).^2));
xrhoab2=rhoab2/deoniatorab2;
fprintf("Нормализованная корелляция a2 и b2(%d) = %f\n", g, xrhoab2);
d(1, g)=xrhoab2;
if d(1, g) >= d(1, maxcor) %сравнение в массиве нормализ корреляции
    maxcor = g;
    subplot(3,1,2);
    plot(x21, a2, x22, b2);
    title(['a2, b2[' num2str(maxcor) ']']);
    xlabel('X');
    ylabel('Y');
    legend('a2', 'b2');
    grid on;
end
end
subplot(3,1,3);
plot(x21, d);
title('Корреляционная функция');
xlabel('X');
ylabel('d');
legend('d');
grid on;