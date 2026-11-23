import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Datos de los megaproyectos (costo y desempeño) — fuentes: SHCP, Pemex/SEC, IMIQ, prensa
mega = pd.DataFrame([
    {'proyecto': 'Tren Maya', 'costo_inicial': 150000, 'costo_final': 500000, 'unidad': 'M MXN',
     'sobrecosto_pct': 233, 'desempeno_pct': 5, 'nota': '5% de afluencia proyectada, pérdidas operativas 788%'},
    {'proyecto': 'Refinería Dos Bocas', 'costo_inicial': 8000, 'costo_final': 21000, 'unidad': 'M USD',
     'sobrecosto_pct': 162, 'desempeno_pct': 45, 'nota': 'opera a 41-50% de capacidad, mayor sobrecosto mundial'},
    {'proyecto': 'AIFA (+ NAIM cancelado)', 'costo_inicial': 75000, 'costo_final': 185000, 'unidad': 'M MXN',
     'sobrecosto_pct': np.nan, 'desempeno_pct': np.nan, 'nota': 'reemplaza al NAIM (mejor ubicado); ~110 mil M MXN desperdiciados'},
    {'proyecto': 'Corredor Interoceánico', 'costo_inicial': np.nan, 'costo_final': np.nan, 'unidad': 'M MXN',
     'sobrecosto_pct': np.nan, 'desempeno_pct': np.nan, 'nota': 'apuesta a nearshoring; polos de desarrollo mayormente vacíos'},
])
mega.to_csv('data/megaproyectos.csv', index=False, encoding='utf-8')

print('=== MEGAPROYECTOS (costo y desempeño) ===')
for _, r in mega.iterrows():
    if pd.notna(r.sobrecosto_pct):
        print(f"  {r.proyecto:28s} {r.costo_inicial:>9,.0f} -> {r.costo_final:>9,.0f} {r.unidad}  sobrecosto +{r.sobrecosto_pct:.0f}%")
    else:
        print(f"  {r.proyecto:28s} {r.nota}")
    print(f"     desempeño: {r.nota}")
    print()

# ---- gráfico 1: sobrecosto (barras) ----
fig, ax = plt.subplots(figsize=(8, 4))
dos = mega.dropna(subset=['sobrecosto_pct'])
cols = ['#d62728']*len(dos)
ax.barh(dos['proyecto'], dos['sobrecosto_pct'], color=cols)
for i, r in dos.iterrows():
    ax.text(r.sobrecosto_pct + 5, i, f"+{r.sobrecosto_pct:.0f}%", va='center', fontsize=11, fontweight='bold')
ax.set_xlabel('Sobrecosto (%)'); ax.set_title('Sobrecosto de los megaproyectos (vs presupuesto original)')
ax.set_xlim(0, 280); ax.grid(alpha=0.3, axis='x')
plt.tight_layout(); plt.savefig('results/megaproyectos_sobrecosto.png', dpi=120); plt.close()

# ---- gráfico 2: desempeño vs meta ----
fig, ax = plt.subplots(figsize=(8, 4))
perf = mega.dropna(subset=['desempeno_pct'])
ax.barh(perf['proyecto'], perf['desempeno_pct'], color=['#d62728', '#ff7f0e'])
for i, r in perf.iterrows():
    ax.text(r.desempeno_pct + 1, i, f"{r.desempeno_pct:.0f}% de meta", va='center', fontsize=10)
ax.axvline(100, color='#2ca02c', ls='--', lw=1.5)
ax.text(100.5, 0.5, 'meta (100%)', color='#2ca02c', fontsize=9)
ax.set_xlabel('% de la meta'); ax.set_title('Desempeño vs meta (afluencia / capacidad)')
ax.set_xlim(0, 120); ax.grid(alpha=0.3, axis='x')
plt.tight_layout(); plt.savefig('results/megaproyectos_desempeno.png', dpi=120); plt.close()
print('Guardado: data/megaproyectos.csv + 2 gráficos en results/')
