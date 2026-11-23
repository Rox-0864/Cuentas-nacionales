import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Datos por sexenio (fuentes ya validadas en el análisis)
# crec: crecimiento PIB real anual % | percapita: PIB per cápita anual % |
# inflacion: media geométrica anual % | deuda_pp: cambio en deuda neta/PIB (puntos)
sex = pd.DataFrame([
    {'sexenio':'De la Madrid','crec':0.1,'percapita':-2.2,'inflacion':83.4,'deuda_pp':np.nan},
    {'sexenio':'Salinas','crec':4.1,'percapita':2.1,'inflacion':15.6,'deuda_pp':0.0},
    {'sexenio':'Zedillo','crec':3.3,'percapita':2.0,'inflacion':21.8,'deuda_pp':0.0},
    {'sexenio':'Fox','crec':1.9,'percapita':0.4,'inflacion':4.4,'deuda_pp':-0.8},
    {'sexenio':'Calderón','crec':1.7,'percapita':-0.1,'inflacion':4.3,'deuda_pp':14.2},
    {'sexenio':'Peña Nieto','crec':2.4,'percapita':0.8,'inflacion':4.2,'deuda_pp':7.6},
    {'sexenio':'AMLO','crec':0.9,'percapita':0.0,'inflacion':5.0,'deuda_pp':8.5},
])

def minmax(v, higher_better):
    v = v.astype(float)
    lo, hi = v.min(), v.max()
    if higher_better:
        return (v - lo) / (hi - lo) * 100
    else:  # lower better -> invertir
        return (hi - v) / (hi - lo) * 100

# Normalizar cada variable (0-100)
sex['s_crec'] = minmax(sex['crec'], True)
sex['s_percapita'] = minmax(sex['percapita'], True)
sex['s_inflacion'] = minmax(sex['inflacion'], False)
sex['s_deuda'] = minmax(sex['deuda_pp'], False)  # menor aumento = mejor

# Puntaje global: promedio de las variables disponibles (pesos iguales)
cols3 = ['s_crec','s_percapita','s_inflacion']
cols4 = cols3 + ['s_deuda']
sex['puntaje_3v'] = sex[cols3].mean(axis=1)
sex['puntaje_4v'] = sex[cols4].mean(axis=1)  # NaN en de la Madrid (sin dato de deuda)

sex = sex.sort_values('puntaje_4v', ascending=False, na_position='last')
sex.to_csv('data/evaluacion_sexenios.csv', index=False, encoding='utf-8')

print('=== PUNTAJE POR SEXENIO (0-100, mayor = mejor) ===')
print(f'{"Sexenio":14s} {"Crec":>5s} {"PerCáp":>7s} {"Infl":>5s} {"Deuda":>6s} {"GLOBAL":>7s}')
print('-'*50)
for _, r in sex.iterrows():
    deuda = f"{r.s_deuda:6.0f}" if pd.notna(r.s_deuda) else '   n/d'
    print(f'{r.sexenio:14s} {r.s_crec:5.0f} {r.s_percapita:7.0f} {r.s_inflacion:5.0f} {deuda} {r.puntaje_4v:7.1f}')

print('\n=== RANKING (puntaje global) ===')
ranking = sex.dropna(subset=['puntaje_4v']).sort_values('puntaje_4v', ascending=False)
for i, (_, r) in enumerate(ranking.iterrows(), 1):
    print(f'  {i}. {r.sexenio:14s} {r.puntaje_4v:5.1f}')
print(f'  (De la Madrid: {sex[sex.sexenio=="De la Madrid"].puntaje_3v.iloc[0]:.1f} en 3 variables, sin dato de deuda)')

# ---- gráfico: barras del puntaje global ----
fig, ax = plt.subplots(figsize=(9, 4.5))
plot = sex.dropna(subset=['puntaje_4v']).sort_values('puntaje_4v')
colores = ['#2ca02c' if p >= 75 else '#ff7f0e' if p >= 55 else '#d62728' for p in plot['puntaje_4v']]
ax.barh(plot['sexenio'], plot['puntaje_4v'], color=colores)
for i, r in plot.iterrows():
    ax.text(r.puntaje_4v + 1, list(plot['sexenio']).index(r.sexenio), f"{r.puntaje_4v:.0f}", va='center', fontsize=11, fontweight='bold')
ax.set_xlabel('Puntaje global (0-100)'); ax.set_xlim(0, 110)
ax.set_title('Puntaje comparativo por sexenio (4 variables, pesos iguales)')
ax.grid(alpha=0.3, axis='x')
plt.tight_layout(); plt.savefig('results/evaluacion_sexenios.png', dpi=120); plt.close()
print('\nGuardado: data/evaluacion_sexenios.csv + results/evaluacion_sexenios.png')
