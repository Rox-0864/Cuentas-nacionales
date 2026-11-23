import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Inflación anual (INPC, cierre de año, %)
infl = {
    1982:98.8, 1983:80.8, 1984:59.2, 1985:63.7, 1986:105.7, 1987:159.2, 1988:51.7,
    1989:19.7, 1990:29.9, 1991:18.8, 1992:11.9, 1993:8.0, 1994:7.1,
    1995:52.0, 1996:27.7, 1997:15.7, 1998:18.6, 1999:12.3, 2000:9.0,
    2001:4.4, 2002:5.7, 2003:4.0, 2004:5.2, 2005:3.3, 2006:4.1,
    2007:3.8, 2008:6.5, 2009:3.6, 2010:4.4, 2011:3.8, 2012:3.6,
    2013:4.0, 2014:4.1, 2015:2.1, 2016:3.4, 2017:6.8, 2018:4.8,
    2019:2.8, 2020:3.2, 2021:7.4, 2022:7.8, 2023:4.7, 2024:4.2, 2025:3.5,
}
dfi = pd.DataFrame([(a,c) for a,c in infl.items()], columns=['Anio','inflacion'])
dfi.to_csv('data/inflacion_1982_2025.csv', index=False, encoding='utf-8')

SEX = [
    ('De la Madrid', 1983, 1988), ('Salinas', 1989, 1994), ('Zedillo', 1995, 2000),
    ('Fox', 2001, 2006), ('Calderón', 2007, 2012), ('Peña Nieto', 2013, 2018), ('AMLO', 2019, 2024),
]
infs = []
for nom, ini, fin in SEX:
    g = [infl[y] for y in range(ini, fin+1)]
    acum = 1.0
    for x in g: acum *= (1 + x/100)
    anual = ((acum) ** (1/len(g)) - 1) * 100
    infs.append({'sexenio': nom, 'inicio': ini, 'fin': fin, 'anual': round(anual,1), 'acumulada': round((acum-1)*100,1)})
dinfl = pd.DataFrame(infs)
dinfl.to_csv('data/inflacion_por_sexenio.csv', index=False, encoding='utf-8')

# Deuda neta / PIB al cierre de sexenio (Banxico, serie consistente desde 1980)
deuda = pd.DataFrame({
    'sexenio': ['Salinas','Zedillo','Fox','Calderón','Peña Nieto','AMLO','Sheinbaum*'],
    'cierre': [1994, 2000, 2006, 2012, 2018, 2024, 2026],
    'deuda_pib': [15.2, 15.2, 14.4, 28.6, 36.3, 44.8, 47.9],
})
deuda.to_csv('data/deuda_por_sexenio.csv', index=False, encoding='utf-8')

print('=== INFLACIÓN POR SEXENIO (media geométrica anual) ===')
for _, r in dinfl.iterrows():
    print(f"  {r.sexenio:12s} {r.inicio}-{r.fin}  {r.anual:6.1f}% anual  (acumulada {r.acumulada:.0f}%)")
print('\n=== DEUDA NETA / PIB AL CIERRE ===')
for _, r in deuda.iterrows():
    print(f"  {r.sexenio:12s} {r.cierre}  {r.deuda_pib:5.1f}%")

# ---- gráfico 1: inflación por sexenio (log) ----
fig, ax = plt.subplots(figsize=(9, 4.5))
cols = ['#d62728' if r.anual > 20 else '#1f77b4' for _, r in dinfl.iterrows()]
ax.bar(dinfl['sexenio'], dinfl['anual'], color=cols)
ax.set_yscale('log')
ax.axhline(3, color='gray', ls=':', lw=1)
ax.text(0, 3.3, 'meta Banxico 3%', fontsize=8, color='gray')
for i, r in dinfl.iterrows():
    ax.text(i, r.anual*1.15, f"{r.anual:.0f}%", ha='center', fontsize=9)
ax.set_ylabel('Inflación anual (%) escala log')
ax.set_title('Inflación promedio anual por sexenio')
plt.xticks(rotation=20, ha='right')
plt.tight_layout(); plt.savefig('results/inflacion_por_sexenio.png', dpi=120); plt.close()

# ---- gráfico 2: deuda/PIB por sexenio ----
fig, ax = plt.subplots(figsize=(9, 4.5))
d = deuda.iloc[:-1]  # excluir Sheinbaum (en curso)
ax.plot(d['sexenio'], d['deuda_pib'], color='#1f77b4', lw=2, marker='o', ms=7)
for i, r in d.iterrows():
    ax.text(i, r.deuda_pib + 1.2, f"{r.deuda_pib:.1f}%", ha='center', fontsize=9)
ax.set_ylabel('Deuda neta / PIB (%)')
ax.set_title('Deuda pública por sexenio (cierre)')
ax.grid(alpha=0.3); ax.set_ylim(0, 52)
plt.tight_layout(); plt.savefig('results/deuda_por_sexenio.png', dpi=120); plt.close()

# ---- gráfico 3: scorecard (¿estamos mejor?) ----
fig, ax = plt.subplots(figsize=(10, 5))
vars_ = ['Inflación', 'Deuda/PIB', 'Crecimiento PIB', 'Pobreza (ingreso)']
sentido = ['mejor', 'peor', 'peor', 'mejor']  # vs era pre-AMLO
valores = [5.0, 8.5, 0.9, -6.7]  # AMLO: inflación, +pp deuda, crec, caída pobreza 2022 vs 2020
colores = ['#d62728' if s=='peor' else '#2ca02c' for s in sentido]
ax.barh(vars_, valores, color=colores)
ax.axvline(0, color='gray', lw=0.8)
for i, (v, s) in enumerate(zip(valores, sentido)):
    ax.text(v + (0.3 if v>=0 else -0.5), i, f"{v:+.1f}" + ("%" if 'Inflación' in vars_[i] or 'Crecimiento' in vars_[i] else " pp" if 'Deuda' in vars_[i] else " pp"), va='center', fontsize=10)
ax.set_title('Scorecard del sexenio de AMLO (vs situación previa)')
ax.set_xlabel('verde = mejora · rojo = empeora')
plt.tight_layout(); plt.savefig('results/scorecard.png', dpi=120); plt.close()

# ---- pronóstico cauto ----
print('\n=== PRONÓSTICO CAUTO (2026-2027) ===')
print('  Inflación: convergiendo a meta Banxico 3% -> 2026 ~3.2%, 2027 ~3.0% (si no hay shock)')
print('  Deuda/PIB: tendencia reciente +1.5 pp/año, pero SHCP apunta a estabilizar ~48-49%')
print('    -> escenario base: 2026 ~46-47%, 2027 ~47-48% (con riesgo al alza si el déficit no baja)')
