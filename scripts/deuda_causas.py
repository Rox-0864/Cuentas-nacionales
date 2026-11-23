import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 1. Causas de los saltos de deuda recientes
causas = pd.DataFrame([
    {'sexenio':'Calderón (2006-2012)','salto_pp':14.2,
     'causa':'Crisis global 2008-09 (caída de ingresos + gasto contracíclico) + reconocimiento de los PIDIREGAS (deuda fuera de balance de Pemex/CFE que se sacó a la luz)'},
    {'sexenio':'Peña Nieto (2012-2018)','salto_pp':7.6,
     'causa':'Colapso del precio del petróleo (2014-16, de $97 a $37 USD) que hundió los ingresos petroleros; Pemex se endeudó para tapar el hueco; depreciación del peso infló la deuda externa'},
    {'sexenio':'AMLO (2018-2024)','salto_pp':8.5,
     'causa':'Tres prioridades de gasto: rescate de Pemex (~2.2 billones), programas sociales (~2.7 billones) y megaobras (~1.05 billones), más el impacto del COVID-19'},
])
causas.to_csv('data/deuda_causas.csv', index=False, encoding='utf-8')

# 2. Composición del gasto de AMLO (billones de pesos)
gasto = pd.DataFrame([
    {'rubro':'Programas sociales (Bienestar)','billones':2.7},
    {'rubro':'Rescate de Pemex','billones':2.2},
    {'rubro':'Megaobras (8 emblema)','billones':1.05},
])
gasto.to_csv('data/amlo_gasto.csv', index=False, encoding='utf-8')

print('=== CAUSAS DE LOS SALTOS DE DEUDA ===')
for _, r in causas.iterrows():
    print(f"\n{r.sexenio}  (+{r.salto_pp} pp)")
    print(f"  {r.causa}")

print('\n=== GASTO DE AMLO (billones MXN) ===')
for _, r in gasto.iterrows():
    print(f"  {r.rubro}: ${r.billones:.2f} billones")

print('\n  Deuda neta total AMLO: ~$3.2 billones')
print(f"  Megaobras ≈ {1.05/3.2*100:.0f}% de la deuda neta")

# ---- gráfico: composición del gasto AMLO ----
fig, ax = plt.subplots(figsize=(9, 4.5))
colores = ['#ff7f0e', '#d62728', '#1f77b4']
ax.barh(gasto['rubro'], gasto['billones'], color=colores)
for i, r in gasto.iterrows():
    ax.text(r.billones + 0.05, i, f"${r.billones:.2f} billones", va='center', fontsize=11, fontweight='bold')
ax.axvline(3.2, color='gray', ls='--', lw=1.5)
ax.text(3.22, 2.1, 'deuda neta total ~$3.2 billones', color='gray', fontsize=9)
ax.set_xlabel('Billones de pesos (MXN)')
ax.set_title('¿A dónde se fue el gasto del sexenio de AMLO? (las 3 prioridades)')
ax.grid(alpha=0.3, axis='x')
ax.set_xlim(0, 3.6)
plt.tight_layout(); plt.savefig('results/amlo_gasto.png', dpi=120); plt.close()
print('\nGuardado: data/deuda_causas.csv + data/amlo_gasto.csv + results/amlo_gasto.png')
