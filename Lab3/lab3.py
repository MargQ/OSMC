import matplotlib.pyplot as plt
import numpy as np


f1 = 6
f2 = 10
f3 = 13

t = np.arange(0,1,1/5)
s1 = np.cos(2*np.pi*f1*t)
s2 = np.cos(2*np.pi*f2*t)
s3 = np.cos(2*np.pi*f3*t)




a = 3*s1 + 4*s2 + s3
b = s1 + 1/4*s2
corr_usual = np.sum(a*b)
corr_a = np.sum(a*a)
corr_b = np.sum(b*b)
corr_norm = corr_usual / (corr_b*corr_a)
print("Корелляция : ", corr_usual )
print("Нормализованная корелляция : ", corr_norm )



correlat = []
a1 = [0.3, 0.2, -0.1, 4.2, -2, 1.5, 0]
b1 = [0.3, 4, -2.2, 1.6, 0.1, 0.1, 0.2]
t1 = np.arange(0,len(a1))

for i in range(0,len(a1)):
    data_new = np.roll(b1, i)
    correlat.append(np.sum(a1*data_new))
    


max_corr = np. argmax(correlat)
b_max = np.roll(b1, max_corr)

#print (max_corr)
plt.figure(1)
plt.subplot(2,1,1)
plt.title("array a")
plt.plot(t1,a1)
plt.subplot(2,1,2)
plt.title("array b")
plt.plot(t1,b1)
plt.figure(2)
plt.subplot(2,1,1)
plt.title("array a")
plt.plot(t1,a1)
plt.subplot(2,1,2)
plt.title("array b max correlation")
plt.plot(t1,b_max)
plt.figure(3)
#plt.subplot(5,1,5)
plt.title("correlation")
plt.plot(t1,correlat)

plt.show()
print(correlat)








