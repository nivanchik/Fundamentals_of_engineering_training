import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv', names=["V", "t"]) 

t = data['t']
V = data['V']

plt.plot(t, V, label='Зависимость V(t)', marker='o', color='b', linestyle='-', markersize=6)

plt.title('Процесс заряда и разряда конденсатора', fontsize=16, fontweight='bold')
plt.xlabel('Время t, c', fontsize=12)
plt.ylabel('Напряжение V, В', fontsize=12)

interval = 10 
plt.xticks(t[::interval], rotation=45, fontsize=10)

plt.minorticks_on()
plt.tick_params(axis='both', which='minor', length=4, color='gray')

plt.legend(loc='best', fontsize=10)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.tick_params(axis='both', which='major', labelsize=10)

plt.savefig('graph.svg', format='svg')

plt.text(85, 2.3, 'Время заряда = 1.47 с', fontsize=12, color='red')
plt.text(85, 2.0, 'Время разряда = 4,58 с', fontsize=12, color='blue')

plt.show()