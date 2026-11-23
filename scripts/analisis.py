import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Crecimiento real anual del PIB (%, series originales, INEGI/Banxico). 2020+ base 2018.
crec = {
    1982:0.0, 1983:-4.4, 1984:3.5, 1985:1.9, 1986:-3.7, 1987:2.1, 1988:1.3,
    1989:3.7, 1990:5.2, 1991:4.0, 1992:3.5, 1993:3.1, 1994:4.9,
    1995:-6.3, 1996:6.8, 1997:6.8, 1998:5.2, 1999:2.8, 2000:4.9,
    2001:-0.4, 2002:0.0, 2003:1.4, 2004:3.9, 2005:2.3, 2006:4.5,
    2007:2.3, 2008:1.1, 2009:-5.3, 2010:5.1, 2011:3.7, 2012:3.6,
    2013:1.4, 2014:2.8, 2015:3.3, 2016:2.6, 2017:2.1, 2018:2.2,
    2019:-0.1, 2020:-8.2, 2021:6.0, 2022:3.7, 2023:3.2, 2024:1.5, 2025:0.5,
}
df = pd.DataFrame([(a, c) for a, c in crec.items()], columns=['Anio','crecimiento'])
df.to_csv('data/pib_crecimiento_1982_2025.csv', index=False, encoding='utf-8')

SEXENIOS = [
    ('Miguel de la Madrid', 1983, 1988),
    ('Carlos Salinas', 1989, 1994),
    ('Ernesto Zedillo', 1995, 2000),
    ('Vicente Fox', 2001, 2006),
    ('Felipe Calderón', 2007, 2012),
    ('Enrique Peña Nieto', 2013, 2018),
    ('AMLO', 2019, 2024),
    ('Sheinbaum*', 2025, 2025),
]

rows = []
for nombre, ini, fin in SEXENIOS:
    g = [crec[y] for y in range(ini, fin+1)]
    # media geométrica
    acum = 1.0
    for x in g: acum *= (1 + x/100)
    anual = ((acum) ** (1/len(g)) - 1) * 100
    acum_pct = (acum - 1) * 100
    rows.append({'sexenio': nombre, 'inicio': ini, 'fin': fin,
                 'anual_prom': round(anual, 2), 'acumulado': round(acum_pct, 1),
                 'n_años': len(g)})
res = pd.DataFrame(rows)
res.to_csv('data/pib_por_sexenio.csv', index=False, encoding='utf-8')

print('=== CRECIMIENTO DEL PIB POR SEXENIO (1983-2024) ===')
print(f'{"Sexenio":22s} {"Periodo":12s} {"Anual prom":>11s} {"Acumulado":>10s}')
for _, r in res.iterrows():
    marca = ' *' if r.sexenio.endswith('*') else ''
    print(f'{r.sexenio:22s} {r.inicio}-{r.fin:<5} {r.anual_prom:>9.2f}% {r.acumulado:>9.1f}%{marca}')

# ---- gráfico 1: promedio anual por sexenio ----
fig, ax = plt.subplots(figsize=(10, 5))
colores = ['#1f77b4']*7 + ['#d3d3d3']
ax.bar(res['sexenio'], res['anual_prom'], color=colores)
for i, r in res.iterrows():
    ax.text(i, r.anual_prom + 0.08, f"{r.anual_prom:.2f}%", ha='center', fontsize=9)
ax.axhline(0, color='gray', lw=0.8)
ax.set_ylabel('Crecimiento promedio anual (%)')
ax.set_title('Crecimiento del PIB de México por sexenio (1983-2024)')
plt.xticks(rotation=20, ha='right')
plt.tight_layout(); plt.savefig('results/pib_por_sexenio.png', dpi=120); plt.close()

# ---- gráfico 2: serie anual con crisis marcadas ----
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(df['Anio'], df['crecimiento'], color='#1f77b4', lw=1.5, marker='o', ms=3)
ax.axhline(0, color='gray', lw=0.8)
ax.fill_between(df['Anio'], 0, df['crecimiento'], where=(df['crecimiento']<0), color='#d62728', alpha=0.3)
for y, txt in [(1983,'crisis deuda'), (1986,'petróleo'), (1995,'crisis peso'), (2009,'crisis global'), (2020,'COVID')]:
    ax.annotate(txt, xy=(y, crec[y]), xytext=(y-1.5, crec[y]-3), fontsize=8,
                arrowprops=dict(arrowstyle='->', color='gray'))
ax.set_ylabel('Crecimiento anual (%)'); ax.set_title('Crecimiento anual del PIB de México, 1982-2025')
ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('results/pib_serie_anual.png', dpi=120); plt.close()

# ---- PIB per cápita por sexenio (fuente: FMI WEO) ----
pc = pd.DataFrame({'sexenio':['De la Madrid','Salinas','Zedillo','Fox','Calderón','Peña Nieto','AMLO'],
                   'pib_pc':[-2.2, 2.1, 2.0, 0.4, -0.1, 0.8, 0.0]})
pc.to_csv('data/pib_percapita_por_sexenio.csv', index=False, encoding='utf-8')
fig, ax = plt.subplots(figsize=(9, 4))
colores = ['#d62728' if v<0 else '#2ca02c' for v in pc['pib_pc']]
ax.bar(pc['sexenio'], pc['pib_pc'], color=colores)
ax.axhline(0, color='gray', lw=0.8)
for i, v in enumerate(pc['pib_pc']):
    ax.text(i, v + (0.08 if v>=0 else -0.25), f"{v:.1f}%", ha='center', fontsize=9)
ax.set_ylabel('Crecimiento PIB per cápita anual (%)')
ax.set_title('PIB per cápita por sexenio (FMI WEO)')
plt.xticks(rotation=20, ha='right')
plt.tight_layout(); plt.savefig('results/pib_percapita.png', dpi=120); plt.close()
print('\nPIB per cápita por sexenio:', dict(zip(pc.sexenio, pc.pib_pc)))
