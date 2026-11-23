import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 10 variables por sexenio (los 80-90 marcados con * son estimaciones)
# gini: al cierre (INEGI/ENIGH) | corrupcion: IPC promedio (Transparencia Intl) |
# instituciones: WGI Estado de Derecho (Banco Mundial, percentil)
sex = pd.DataFrame([
    {'sexenio':'De la Madrid','crec':0.1,'percapita':-2.2,'inflacion':83.4,'deuda_pp':np.nan,'homicidios':21.69,'salario_real':-40,'empleo_formal':1.5,'gini':0.44,'corrupcion':28,'instituciones':50},
    {'sexenio':'Salinas','crec':4.1,'percapita':2.1,'inflacion':15.6,'deuda_pp':0.0,'homicidios':17.59,'salario_real':-20,'empleo_formal':2.0,'gini':0.49,'corrupcion':30,'instituciones':55},
    {'sexenio':'Zedillo','crec':3.3,'percapita':2.0,'inflacion':21.8,'deuda_pp':0.0,'homicidios':14.37,'salario_real':-15,'empleo_formal':2.5,'gini':0.49,'corrupcion':33,'instituciones':56},
    {'sexenio':'Fox','crec':1.9,'percapita':0.4,'inflacion':4.4,'deuda_pp':-0.8,'homicidios':10.05,'salario_real':-1,'empleo_formal':2.5,'gini':0.47,'corrupcion':35,'instituciones':50},
    {'sexenio':'Calderón','crec':1.7,'percapita':-0.1,'inflacion':4.3,'deuda_pp':14.2,'homicidios':18.75,'salario_real':-1,'empleo_formal':2.3,'gini':0.46,'corrupcion':35,'instituciones':45},
    {'sexenio':'Peña Nieto','crec':2.4,'percapita':0.8,'inflacion':4.2,'deuda_pp':7.6,'homicidios':22.18,'salario_real':3,'empleo_formal':4.0,'gini':0.43,'corrupcion':31,'instituciones':40},
    {'sexenio':'AMLO','crec':0.9,'percapita':0.0,'inflacion':5.0,'deuda_pp':8.5,'homicidios':25.84,'salario_real':110,'empleo_formal':2.4,'gini':0.40,'corrupcion':29,'instituciones':37},
])

def minmax(v, higher_better):
    v = v.astype(float)
    lo, hi = v.min(), v.max()
    return (v - lo) / (hi - lo) * 100 if higher_better else (hi - v) / (hi - lo) * 100

sex['s_crec'] = minmax(sex['crec'], True)
sex['s_percapita'] = minmax(sex['percapita'], True)
sex['s_inflacion'] = minmax(sex['inflacion'], False)
sex['s_deuda'] = minmax(sex['deuda_pp'], False)
sex['s_homicidios'] = minmax(sex['homicidios'], False)
sex['s_salario'] = minmax(sex['salario_real'], True)
sex['s_empleo'] = minmax(sex['empleo_formal'], True)
sex['s_gini'] = minmax(sex['gini'], False)
sex['s_corrupcion'] = minmax(sex['corrupcion'], True)
sex['s_instituciones'] = minmax(sex['instituciones'], True)

cols7 = ['s_crec','s_percapita','s_inflacion','s_deuda','s_homicidios','s_salario','s_empleo']
cols10 = cols7 + ['s_gini','s_corrupcion','s_instituciones']
sex['puntaje_7v'] = sex[cols7].mean(axis=1)
sex['puntaje_10v'] = sex[cols10].mean(axis=1)
sex.to_csv('data/evaluacion_sexenios.csv', index=False, encoding='utf-8')

print('=== PUNTAJE CON 10 VARIABLES (0-100) ===')
cols_show = ['sexenio','s_crec','s_homicidios','s_salario','s_gini','s_corrupcion','s_instituciones','puntaje_10v']
print(sex[cols_show].round(1).to_string(index=False))

print('\n=== RANKING: 7 variables vs 10 variables ===')
r7 = sex.sort_values('puntaje_7v', ascending=False)
r10 = sex.sort_values('puntaje_10v', ascending=False)
print(f'{"Pos":>4s} {"7 variables":30s} {"10 variables (completo)":30s}')
for i in range(7):
    print(f'{i+1:>4d} {r7.iloc[i].sexenio + " " + str(round(r7.iloc[i].puntaje_7v)):30s} {r10.iloc[i].sexenio + " " + str(round(r10.iloc[i].puntaje_10v)):30s}')

# gráfico comparativo 7v vs 10v
fig, ax = plt.subplots(figsize=(10, 5))
r = sex.sort_values('puntaje_10v')
x = np.arange(len(r)); w = 0.35
ax.barh(x + w/2, r['puntaje_10v'], w, color='#2ca02c', label='10 variables (completo)')
ax.barh(x - w/2, r['puntaje_7v'], w, color='#b0b0b0', label='7 variables')
ax.set_yticks(x); ax.set_yticklabels(r['sexenio'])
ax.set_xlabel('Puntaje (0-100)'); ax.set_xlim(0, 110)
ax.set_title('Evaluación por sexenio: 7 vs 10 variables (con desigualdad, corrupción e instituciones)')
ax.legend(fontsize=9); ax.grid(alpha=0.3, axis='x')
plt.tight_layout(); plt.savefig('results/evaluacion_sexenios.png', dpi=120); plt.close()
print('\nGuardado: data/evaluacion_sexenios.csv + results/evaluacion_sexenios.png')
