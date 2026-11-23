import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 1. Participación de la manufactura en el PIB (%, valores corrientes, INEGI)
manuf = pd.DataFrame({
    'Anio': [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023],
    'manufactura_pib': [18.3,18.2,17.4,17.8,17.7,18.8,18.1,18.2,19.8,19.9,20.2,20.2,19.9,20.2,20.8,21.4,20.1],
})
manuf.to_csv('data/manufactura_pib.csv', index=False, encoding='utf-8')

# 2. Gran división (VAB % del PIB) — terciarización
sectores = pd.DataFrame({
    'Anio': [2003, 2013, 2018, 2023],
    'Primarias': [3.6, 3.3, 3.4, 3.2],
    'Secundarias': [33.7, 32.8, 30.5, 31.5],
    'Terciarias': [62.7, 63.9, 66.1, 64.5],
})
sectores.to_csv('data/pib_sectores.csv', index=False, encoding='utf-8')

# 3. Producción de petróleo de Pemex (millones barriles/día)
pemex = pd.DataFrame({
    'Anio': [2004, 2008, 2013, 2018, 2024],
    'mbd': [3.4, 2.8, 2.5, 1.8, 1.5],
})
pemex.to_csv('data/pemex_produccion.csv', index=False, encoding='utf-8')

print('=== MANUFACTURA % DEL PIB (2007-2023) ===')
print(f"  inicio 2007: {manuf.manufactura_pib.iloc[0]}% | final 2023: {manuf.manufactura_pib.iloc[-1]}%")
print(f"  (el salto 2014->2015 es el cambio de año base, no un crecimiento real)")
print('\n=== GRAN DIVISIÓN (% VAB) ===')
print(sectores.to_string(index=False))
print('\n=== PEMEX (millones barriles/día) ===')
for _, r in pemex.iterrows():
    print(f"  {r.Anio}: {r.mbd} mbd")

# ---- gráficos ----
fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

# 1. manufactura estancada
a = axes[0]
a.plot(manuf['Anio'], manuf['manufactura_pib'], color='#1f77b4', lw=2, marker='o', ms=5)
a.axvspan(2013.5, 2015.5, color='gray', alpha=0.15)
a.text(2014.5, 21.7, 'cambio\naño base', ha='center', fontsize=7, color='gray')
a.set_title('Manufactura: estancada en ~18-20% del PIB'); a.set_ylim(15, 23); a.grid(alpha=0.3)
a.set_ylabel('% del PIB')

# 2. terciarización
b = axes[1]
b.plot(sectores['Anio'], sectores['Terciarias'], color='#2ca02c', lw=2, marker='o', ms=5, label='Terciarias (servicios)')
b.plot(sectores['Anio'], sectores['Secundarias'], color='#1f77b4', lw=2, marker='o', ms=5, label='Secundarias (industria)')
b.plot(sectores['Anio'], sectores['Primarias'], color='#d62728', lw=2, marker='o', ms=5, label='Primarias')
b.set_title('Terciarización: servicios dominan'); b.grid(alpha=0.3); b.legend(fontsize=8)
b.set_ylabel('% del VAB')

# 3. petróleo
c = axes[2]
c.plot(pemex['Anio'], pemex['mbd'], color='#8c564b', lw=2, marker='o', ms=6)
c.fill_between(pemex['Anio'], 0, pemex['mbd'], color='#8c564b', alpha=0.15)
c.set_title('Pemex: el colapso petrolero'); c.grid(alpha=0.3)
c.set_ylabel('millones barriles/día')
for i, r in pemex.iterrows():
    c.text(r.Anio, r.mbd + 0.1, f"{r.mbd}", ha='center', fontsize=8)

plt.tight_layout(); plt.savefig('results/sectores.png', dpi=120); plt.close()
print('\nGuardado: data/manufactura_pib.csv + data/pib_sectores.csv + data/pemex_produccion.csv + results/sectores.png')
