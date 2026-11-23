import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 7 variables por sexenio
# crec: PIB real anual % | percapita: PIB per cápita anual % | inflacion: media geométrica %
# deuda_pp: cambio deuda/PIB (pp) | homicidios: tasa promedio por 100k (Colmex)
# salario_real: cambio % del salario mínimo real (80s-90s = estimado, 2000+ = oficial)
# empleo_formal: millones de empleos IMSS creados (estimado)
sex = pd.DataFrame([
    {'sexenio':'De la Madrid','crec':0.1,'percapita':-2.2,'inflacion':83.4,'deuda_pp':np.nan,'homicidios':21.69,'salario_real':-40,'empleo_formal':1.5},
    {'sexenio':'Salinas','crec':4.1,'percapita':2.1,'inflacion':15.6,'deuda_pp':0.0,'homicidios':17.59,'salario_real':-20,'empleo_formal':2.0},
    {'sexenio':'Zedillo','crec':3.3,'percapita':2.0,'inflacion':21.8,'deuda_pp':0.0,'homicidios':14.37,'salario_real':-15,'empleo_formal':2.5},
    {'sexenio':'Fox','crec':1.9,'percapita':0.4,'inflacion':4.4,'deuda_pp':-0.8,'homicidios':10.05,'salario_real':-1,'empleo_formal':2.5},
    {'sexenio':'Calderón','crec':1.7,'percapita':-0.1,'inflacion':4.3,'deuda_pp':14.2,'homicidios':18.75,'salario_real':-1,'empleo_formal':2.3},
    {'sexenio':'Peña Nieto','crec':2.4,'percapita':0.8,'inflacion':4.2,'deuda_pp':7.6,'homicidios':22.18,'salario_real':3,'empleo_formal':4.0},
    {'sexenio':'AMLO','crec':0.9,'percapita':0.0,'inflacion':5.0,'deuda_pp':8.5,'homicidios':25.84,'salario_real':110,'empleo_formal':2.4},
])

def minmax(v, higher_better):
    v = v.astype(float)
    lo, hi = v.min(), v.max()
    return (v - lo) / (hi - lo) * 100 if higher_better else (hi - v) / (hi - lo) * 100

# Normalizar (0-100)
sex['s_crec'] = minmax(sex['crec'], True)
sex['s_percapita'] = minmax(sex['percapita'], True)
sex['s_inflacion'] = minmax(sex['inflacion'], False)
sex['s_deuda'] = minmax(sex['deuda_pp'], False)
sex['s_homicidios'] = minmax(sex['homicidios'], False)
sex['s_salario'] = minmax(sex['salario_real'], True)
sex['s_empleo'] = minmax(sex['empleo_formal'], True)

cols4 = ['s_crec','s_percapita','s_inflacion','s_deuda']
cols7 = cols4 + ['s_homicidios','s_salario','s_empleo']
sex['puntaje_4v'] = sex[cols4].mean(axis=1)
sex['puntaje_7v'] = sex[cols7].mean(axis=1)  # de la Madrid NaN en deuda -> media de 6 disponibles
sex.to_csv('data/evaluacion_sexenios.csv', index=False, encoding='utf-8')

print('=== PUNTAJE CON 7 VARIABLES (0-100) ===')
print(f'{"Sexenio":13s} {"Crec":>4s} {"Infl":>4s} {"Deuda":>5s} {"Homic":>5s} {"Salario":>7s} {"Empleo":>6s} {"GLOBAL":>7s}')
for _, r in sex.iterrows():
    print(f'{r.sexenio:13s} {r.s_crec:4.0f} {r.s_inflacion:4.0f} {r.s_deuda:5.0f} {r.s_homicidios:5.0f} {r.s_salario:7.0f} {r.s_empleo:6.0f} {r.puntaje_7v:7.1f}')

print('\n=== RANKING: 4 variables vs 7 variables ===')
r4 = sex.sort_values('puntaje_4v', ascending=False)
r7 = sex.sort_values('puntaje_7v', ascending=False)
print(f'{"Pos":>4s} {"4 variables (solo economía)":34s} {"7 variables (completo)":30s}')
for i in range(7):
    print(f'{i+1:>4d} {r4.iloc[i].sexenio + " " + str(round(r4.iloc[i].puntaje_4v)):34s} {r7.iloc[i].sexenio + " " + str(round(r7.iloc[i].puntaje_7v)):30s}')

# gráfico comparativo 4v vs 7v
fig, ax = plt.subplots(figsize=(10, 5))
r = sex.sort_values('puntaje_7v')
x = np.arange(len(r))
w = 0.35
ax.barh(x + w/2, r['puntaje_7v'], w, color='#2ca02c', label='7 variables (completo)')
ax.barh(x - w/2, r['puntaje_4v'], w, color='#b0b0b0', label='4 variables (solo economía)')
ax.set_yticks(x); ax.set_yticklabels(r['sexenio'])
ax.set_xlabel('Puntaje (0-100)'); ax.set_xlim(0, 110)
ax.set_title('Evaluación por sexenio: solo economía vs completo (con seguridad/social)')
ax.legend(fontsize=9); ax.grid(alpha=0.3, axis='x')
plt.tight_layout(); plt.savefig('results/evaluacion_sexenios.png', dpi=120); plt.close()
print('\nGuardado: data/evaluacion_sexenios.csv + results/evaluacion_sexenios.png')
