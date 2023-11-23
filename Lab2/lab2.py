import matplotlib.pyplot as plt 
import numpy as np 
import math as mt
from shapely.geometry import LineString

Pant_tx = 46 # Мощность передатчиков BS [дБм]
num_sec = 3 # Число секторов на одной BS
Pat_tx = 24 # Мощность передатчика пользовательского терминала [дБм]
Gant = 21 # Коэффициент усиления антенны BS [дБи]
PenetrationM = 15 # Запас мощности сигнала на проникновения сквозь стены [дБ]
IM= 1 # Запас мощности сигнала на интерференцию [дБ]
FeederLoss = 2 # уровень потерь сигнала при прохождении через фидер или джампер, дБ
##Модель распространения сигнала для макросот: COST 231 Hata;
##Модель распространения сигнала для фемто- и микросот:UMiNLOS
f = 1.8 # Диапазон частот [ГГц]
BW_UL = 10 # Полоса частот в UL [МГц]
BW_DL = 20 # Полоса частот в DL [МГц]
##Дуплекс UL и DL: FDD
NoiseFigure_ant = 2.4 # Коэффициент шума приемника BS [дБ]
NoiseFigure_at = 6 # коэффициент шума приемника пользователя [дБ]
RequiredSINR_DL = 2 # Требуемое отношение SINR для DL [дБ]
RequiredSINR_UL = 4 # Требуемое отношение SINR для UL [дБ]
#ThermalNoise_ant = -174+10
ThermalNoise_ant = -104 #тепловой шум приемника
ThermalNoise_at = -101 #тепловой шум приемника
RxSensBS = NoiseFigure_ant + ThermalNoise_ant + RequiredSINR_UL
RxSensUE = NoiseFigure_at + ThermalNoise_at + RequiredSINR_DL
##Число приемо-передающих антенн на BS (MIMO): 2
MIMOGain= 3 # MIMO c двумя передающими антеннами позволяет усилить сигнал на 3 дБ или в 2 раза (MIMOGain)

# расчет бюджета восходящего канала [дБ]
MAPL_UL = Pat_tx - FeederLoss + Gant + MIMOGain - IM - PenetrationM - RxSensBS 
# расчет бюджета нисходящего канала [дБ]
MAPL_DL = Pant_tx - FeederLoss + Gant + MIMOGain - IM - PenetrationM - RxSensUE

c= 3*10**8 #[м/с] скорость света
ytik = np.arange(0,200)
#Постройте зависимость величины входных потерь радиосигнала от
#расстояния между приемником и передатчиком по всем трем описанным в п.2.2
#моделям. Выберите нужную модель для заданных условий.

#Модель UMiNLOS (Urban Micro Non-Line-of-Sight)

def UMiNLOS():  # зависимость величины входных потерь радиосигнала от расстояния между приемником и передатчиком по UMiNLOS и FSPM
    d = np.arange(1,500)
    PLd = 26 * np.log10(f) + 22.7 + 36.7 * np.log10(d)
    FSPM = 20 * np.log10((4 * np.pi * f * 10**9 * d) / c )

    mapl_dl = [MAPL_DL] * len(d)
    mapl_ul = [MAPL_UL] * len(d)
    

    plt.figure(1)
    plt.ylabel("Потери сигнала, Дб")
    plt.xlabel("Расстояние между приемником и передатчиком, м")
    plt.plot(d,PLd)
    plt.plot(d,FSPM, "--")
    plt.plot(d, mapl_dl)
    plt.plot(d, mapl_ul, "--", "r")
    plt.yticks(np.arange(min(ytik), max(ytik)+1, 50))

    plt.legend(["UMiNLOS", "FSPM", "MAPL_DL", "MAPL_UL"], loc = 4)
    plt.grid(linewidth = 0.5)
    plt.show()

def Lclutter(key):           # Параметр для расчета модели cost231, пользователь выбирает местность
    if key == "DU":
        lutter = 3
    elif key == "U":
        lutter = 0
    elif key == "SU":
        lutter = - (2*(np.log10(f*10**3/28))**2 + 5.4)
    elif key == "RURAL":
        lutter = -(4.78 * (np.log10(f*10**3))**2 - 18.33 * np.log10(f*10**3) + 40.94)
    elif key == "ROAD":
        lutter = -(4.78 * (np.log10(f*10**3))**2 - 18.33 * np.log10(f*10**3) + 35.94)
    return lutter

def a(key):# Параметр для расчета модели cost231
    hms = 1
    if key == "DU":
        param_a = 3.2 *np.log10(11.75*hms)**2 - 4.97
    elif key == "SU":
        param_a = (1.1*np.log10(f*10**3) * hms - 1.56 * np.log10(f*10**3) - 0.8)
    return param_a

def s(d,hBS):        # составляющая для расчета модели cost231
    
    if d >= 1:
        param_s = 44.9 - 6.55 * np.log10(f*10**3)
    else:
        param_s =  (47.88 + 13.9 * np.log10(f*10**3) -13.9 * np.log10(hBS)) *  (1/np.log10(50))
    return param_s


def  COST_231():           # зависимость величины входных потерь радиосигнала от расстояния между приемником и передатчиком по UMiNLOS и COST_231
    d = np.arange(1,1000)
    mapl_dl = [MAPL_DL] * len(d)
    mapl_ul = [MAPL_UL] * len(d)
    A = 46.3
    B = 33.9 
    hBS = 50
    PLd = []
    for i in range(len(d)):
        PLd.append(A + B * np.log10(f*10**3) - 13.82 * np.log10(hBS) - a("DU") + s(d[i]*10**-3,hBS) * np.log10(d[i]*10**-3) + Lclutter("DU")) # urban

    FSPM = 20 * np.log10((4 * np.pi * f * 10**9 * d) / c )
    plt.figure(2)
    plt.ylabel("Потери сигнала, Дб")
    plt.xlabel("Расстояние между приемником и передатчиком, м")
    plt.plot(d,PLd)
    plt.plot(d,FSPM, "--")
    plt.plot(d, mapl_dl)
    plt.plot(d, mapl_ul, "--", "r")
    plt.yticks(np.arange(min(ytik), max(ytik)+1, 50))

    plt.legend(["COST_231", "FSPM", "MAPL_DL", "MAPL_UL"], loc = 4)
    plt.grid(linewidth = 0.5)
    plt.show()
UMiNLOS()
COST_231()
#def COST_231_UMiNLOS_Walfish(): # зависимость величины входных потерь радиосигнала от расстояния между приемником и передатчиком по UMiNLOS и FSPM и Walfish
d = np.arange(1,7000)
PLd_u = 26 * np.log10(f) + 22.7 + 36.7 * np.log10(d)

    # Walfish_Ikegami_LOS
PLd_w = 42.6 + 20 * np.log10(f*10**3) + 26*np.log10(d*10**-3)

A = 46.3
B = 33.9 
hBS = 50
PLd_c = []
mapl_dl = [MAPL_DL] * len(d)
mapl_ul = [MAPL_UL] * len(d)
'''stem_radius = [0]*len(d)
stem_radius[410] = MAPL_UL
stem_radius[5500] = MAPL_UL'''
    
for i in range(len(d)):
    PLd_c.append(A + B * np.log10(f*10**3) - 13.82 * np.log10(hBS) - a("DU") + s(d[i]*10**-3,hBS) * np.log10(d[i]*10**-3) + Lclutter("U")) # ROAD
   
   
plt.figure(1)
plt.ylabel("Потери сигнала, Дб")
plt.xlabel("Расстояние между приемником и передатчиком, м")
plt.plot(d,PLd_c)
plt.plot(d,PLd_u)
plt.plot(d,PLd_w)
plt.axhline (y=MAPL_DL, color='r', linestyle='--')
plt.axhline (y=MAPL_UL, color='y', linestyle='--')
plt.legend(["COST_231", "UMiNLOS", "Walfish-Ikegami","MAPL_DL", "MAPL_UL"], loc = 4)
plt.grid(linewidth = 0.5)
line_1 = LineString(np.column_stack((d,mapl_ul)))
line_2 = LineString(np.column_stack((d,PLd_w)))
line_3 = LineString(np.column_stack((d,mapl_ul)))
line_4 = LineString(np.column_stack((d,PLd_c)))
line_5 = LineString(np.column_stack((d,mapl_ul)))
line_6 = LineString(np.column_stack((d,PLd_u)))
intersection = line_1.intersection(line_2)    
intersection2 = line_3.intersection(line_4)
intersection3 = line_5.intersection(line_6)
plt.plot(*intersection.xy, 'ro')
plt.plot(*intersection2.xy, 'ro')
plt.plot(*intersection3.xy, 'ro')
plt.show()
    
    
    
    #MAPL_UL, PLd_u = shp.LineString(intersection).MAPL_ULPLd_u
    

Radius_U=678*10**-3
Radius_cost=5836*10**-3
#Radius_cost=5836*10**-3


#COST_231_UMiNLOS_Walfish()

S_big = 1.95 * Radius_cost**2
S_small = 1.95 * Radius_U**2
print("Уровень максимально допустимых потерь сигнала MAPL_UL =", MAPL_UL, "dB")

print("Уровень максимально допустимых потерь сигнала MAPL_DL =", MAPL_DL, "dB")

print("Радиус Базовой станции для модели UMiNLOS =",Radius_U, "км" )

print("Радиус Базовой станции для модели COST_231 =",Radius_cost, "км" )

print("Площадь одной базовой станции для модели UMiNLOS =", S_small, "км кв" )

print("Площадь одной базовой станции для модели COST_231 =", S_big, "км кв" )

S_usl_1 = 100
S_usl_2 = 4

count_sait_U= S_usl_2/S_small
count_sait_cost= S_usl_1/S_big
print("Необходимое количество базовых станций для модели UMiNLOS ",count_sait_U )

print("Необходимое количество базовых станций для модели COST_231 ",count_sait_cost )

