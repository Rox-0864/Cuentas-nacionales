import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Cuentas Nacionales de México", page_icon="📈", layout="wide")

@st.cache_data
def cargar():
    crec = pd.read_csv("data/pib_crecimiento_1982_2025.csv")
    sex = pd.read_csv("data/pib_por_sexenio.csv")
    pc = pd.read_csv("data/pib_percapita_por_sexenio.csv")
    dinfl = pd.read_csv("data/inflacion_por_sexenio.csv")
    deuda = pd.read_csv("data/deuda_por_sexenio.csv")
    return crec, sex, pc, dinfl, deuda

crec, sex, pc, dinfl, deuda = cargar()

st.title("📈 Cuentas Nacionales de México — por sexenio")
st.caption("Crecimiento del PIB real 1983–2024 · INEGI/Banxico/FMI")

st.markdown("""
**El dato que resume 40 años:** la economía mexicana pasó de crecer **~3-4% anual** en los
sexenios de Salinas y Zedillo (a pesar de las crisis) a un **"crecimiento mediocre" de ~1-2%**
desde 2001, y a **0.9%** con AMLO (el más bajo desde De la Madrid). El PIB per cápita lleva
dos décadas prácticamente estancado.
""")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mejor sexenio", "Salinas", "4.1% anual")
c2.metric("Peor sexenio", "De la Madrid", "0.1% anual", delta_color="inverse")
c3.metric("AMLO (2019-24)", "0.9% anual", "−6.7 pts vs Salinas", delta_color="inverse")
c4.metric("Crecimiento 2025 (prel.)", "0.5%")

st.markdown("---")

# 1. Por sexenio
st.header("1 · Crecimiento promedio anual por sexenio")
fig = go.Figure()
colores = ["#1f77b4"] * (len(sex) - 1) + ["#c0c0c0"]
fig.add_trace(go.Bar(x=sex["sexenio"], y=sex["anual_prom"], marker_color=colores,
                     text=[f"{v:.2f}%" for v in sex["anual_prom"]], textposition="outside"))
fig.add_hline(y=0, line_color="gray", line_width=1)
fig.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0),
                  yaxis_title="% anual", yaxis=dict(range=[-1, 5]))
st.plotly_chart(fig, use_container_width=True)
st.caption("Media geométrica anual. Sheinbaum (2025, gris) con un solo año preliminar.")

st.markdown("---")

# 2. Serie anual
st.header("2 · Serie anual (1982-2025) con las crisis")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=crec["Anio"], y=crec["crecimiento"], mode="lines+markers",
                          name="Crecimiento anual", line=dict(color="#1f77b4", width=1.5)))
# sombrear recesiones
for y, txt in [(1983, "crisis deuda"), (1986, "petróleo"), (1995, "crisis peso"),
               (2009, "crisis global"), (2020, "COVID")]:
    fig2.add_annotation(x=y, y=crec[crec["Anio"] == y]["crecimiento"].iloc[0],
                        text=txt, showarrow=True, arrowhead=2, ay=28, font=dict(size=10))
fig2.add_hline(y=0, line_color="gray", line_width=1)
fig2.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0), yaxis_title="% anual")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 3. PIB per cápita
st.header("3 · PIB per cápita por sexenio (lo que le toca a cada persona)")
fig3 = go.Figure()
colores3 = ["#d62728" if v < 0 else "#2ca02c" for v in pc["pib_pc"]]
fig3.add_trace(go.Bar(x=pc["sexenio"], y=pc["pib_pc"], marker_color=colores3,
                      text=[f"{v:.1f}%" for v in pc["pib_pc"]], textposition="outside"))
fig3.add_hline(y=0, line_color="gray", line_width=1)
fig3.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0), yaxis_title="% anual")
st.plotly_chart(fig3, use_container_width=True)
st.warning("**El punto crudo:** desde 2001 el PIB per cápita crece menos del 1% anual (Fox +0.4%, "
           "Calderón −0.1%, Peña +0.8%, AMLO 0.0%). Con la población creciendo ~1% anual, un PIB "
           "de ~1-2% deja el ingreso por habitante **estancado por más de 20 años**.")

st.markdown("---")

# 4. PIB por sectores
st.header("4 · PIB por sectores — la industrialización trunca")
sect = pd.read_csv("data/pib_sectores.csv")
manuf = pd.read_csv("data/manufactura_pib.csv")
pemex = pd.read_csv("data/pemex_produccion.csv")
cA, cB, cC = st.columns(3)
with cA:
    st.subheader("Manufactura (% PIB)")
    f = go.Figure()
    f.add_trace(go.Scatter(x=manuf["Anio"], y=manuf["manufactura_pib"], mode="lines+markers",
                           line=dict(color="#1f77b4", width=2)))
    f.add_vrect(x0=2013.5, x1=2015.5, fillcolor="gray", opacity=0.15, line_width=0)
    f.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), yaxis=dict(range=[15, 23]), yaxis_title="% PIB")
    st.plotly_chart(f, use_container_width=True)
    st.caption("Estancada ~18-20% por 30 años pese a TLCAN/T-MEC.")
with cB:
    st.subheader("Gran división (% VAB)")
    f = go.Figure()
    for col, color, name in [("Terciarias", "#2ca02c", "Servicios"), ("Secundarias", "#1f77b4", "Industria"),
                             ("Primarias", "#d62728", "Primarias")]:
        f.add_trace(go.Scatter(x=sect["Anio"], y=sect[col], mode="lines+markers", name=name,
                               line=dict(color=color, width=2)))
    f.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), yaxis_title="% VAB")
    st.plotly_chart(f, use_container_width=True)
with cC:
    st.subheader("Pemex (mbd)")
    f = go.Figure()
    f.add_trace(go.Scatter(x=pemex["Anio"], y=pemex["mbd"], mode="lines+markers",
                           line=dict(color="#8c564b", width=2), fill="tozeroy"))
    f.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), yaxis_title="mbd")
    st.plotly_chart(f, use_container_width=True)
st.warning("**La causa estructural del bajo crecimiento:** México no se industrializó (manufactura plana ~18-20%), "
           "se terciarizó hacia servicios de baja productividad (63-66%) y perdió su motor petrolero (Pemex −56%). "
           "El nearshoring prometido no aparece en los datos (manufactura −0.4% en 2024).")

st.markdown("---")

# 5. Inflación
st.header("5 · Inflación por sexenio")
fig4 = go.Figure()
colores4 = ["#d62728" if v > 20 else "#1f77b4" for v in dinfl["anual"]]
fig4.add_trace(go.Bar(x=dinfl["sexenio"], y=dinfl["anual"], marker_color=colores4,
                      text=[f"{v:.0f}%" for v in dinfl["anual"]], textposition="outside"))
fig4.add_hline(y=3, line_dash="dot", line_color="gray")
fig4.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0),
                   yaxis_title="% anual", yaxis=dict(type="log", range=[0.3, 2.1]))
st.plotly_chart(fig4, use_container_width=True)
st.caption("Escala logarítmica. La hiperinflación de los 80 (~85%) fue domada en los 90; desde Fox ronda "
           "4-5%. AMLO tuvo la más alta del siglo XXI (5.0% anual) por el shock 2021-22. Meta Banxico: 3% (línea punteada).")

st.markdown("---")

# 5. Deuda
st.header("6 · Deuda pública por sexenio (cierre, % PIB)")
d = deuda[~deuda["sexenio"].str.endswith("*")]
fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=d["sexenio"], y=d["deuda_pib"], mode="lines+markers",
                          line=dict(color="#1f77b4", width=3), marker=dict(size=9),
                          text=[f"{v:.1f}%" for v in d["deuda_pib"]], textposition="top center"))
fig5.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0), yaxis_title="% del PIB",
                   yaxis=dict(range=[0, 52]))
st.plotly_chart(fig5, use_container_width=True)
st.warning("La deuda fue baja y estable (15%) en los 90 y con Fox; **saltó con Calderón (2008)** y no ha "
           "dejado de subir. AMLO la incrementó +8.5 pp (a 44.8%) y cerró con **déficit récord (~5-6% del PIB)**. "
           "La medida amplia (SHRFSP) ya supera 51%.")

st.markdown("---")

# 6b. Megaproyectos
st.header("6b · Megaproyectos: ¿inversión o elefante blanco?")
mega = pd.read_csv("data/megaproyectos.csv")
st.markdown("""
| Proyecto | Costo inicial | Costo final | Sobrecosto | Desempeño |
|---|---|---|---|---|
| Tren Maya | $150 mil M MXN | $450-544 mil M MXN | **+233%** | 5% de afluencia, pérdidas 788% |
| Refinería Dos Bocas | $8 mil M USD | $21 mil M USD | **+162%** | 41-50% de capacidad (mayor sobrecosto mundial) |
| AIFA | $75 mil M MXN | ~$185 mil M MXN | — | reemplaza al NAIM (mejor ubicado) |
| Corredor Interoceánico | moderado | moderado | bajo | polos de desarrollo vacíos |
""")
dos = mega.dropna(subset=["sobrecosto_pct"])
fig_m = go.Figure(go.Bar(y=dos["proyecto"], x=dos["sobrecosto_pct"], orientation="h",
                         marker_color="#d62728",
                         text=[f"+{v:.0f}%" for v in dos["sobrecosto_pct"]], textposition="outside"))
fig_m.update_layout(height=260, margin=dict(l=0, r=0, t=10, b=0), xaxis_title="Sobrecosto (%)",
                    xaxis=dict(range=[0, 280]))
st.plotly_chart(fig_m, use_container_width=True)
st.warning("**Veredicto:** en su mayoría son **elefantes blancos** — sobrecostos de 2-3x, opacidad y retorno "
           "dudoso, no inversión que eleve la productividad. Dos Bocas es el caso más claro (refina crudo pesado "
           "inadecuado y sigue en pruebas). El Tren Maya pierde ~$7 M MXN/día. El Corredor Interoceánico es el único "
           "conceptualmente defendible, pero especulativo. El déficit récord no se fue en productividad, se fue en "
           "obra simbólica.")

st.markdown("---")

# 7. Veredicto
st.header("7 · ¿Estamos mejor con el cambio desde AMLO?")
st.markdown("""
| Variable | Resultado AMLO | Veredicto |
|---|---|---|
| Inflación | 5.0% anual | Mejor que los 80, **peor que Fox/Calderón/Peña** |
| Deuda/PIB | +8.5 pp | **Peor**: déficit récord 2024 |
| Crecimiento | 0.9% anual | **Peor**: el más bajo desde De la Madrid |
| Pobreza (ingreso) | −6.7 pts | **Mejor**, vía transferencias y con duda metodológica (CONEVAL→INEGI) |
""")
st.info("**Respuesta honesta:** no es un 'mejor' limpio. Hubo una **mejora social real por ingreso** "
        "(transferencias, pensiones, remesas, salario mínimo), pero **financiada con deuda y déficit récord**, "
        "y con el **crecimiento más bajo en casi 40 años**. En inflación ya estábamos 'bien' desde los 2000; "
        "el sexenio no lo mejoró. Es un trade-off: más gasto social, menos crecimiento y más deuda.")

st.markdown("---")

# 7. Pronóstico
st.header("8 · Pronóstico cauto (2026-2027)")
c1p, c2p = st.columns(2)
c1p.metric("Inflación 2026 (proy.)", "~3.2%", "converge a meta 3%")
c2p.metric("Deuda/PIB 2027 (proy.)", "~47-48%", "riesgo al alza si no baja el déficit")
st.caption("Rangos de planificación, no cifras puntuales: la deuda depende de decisiones fiscales, "
           "no de una tendencia natural.")

st.markdown("---")

st.header("9 · Nota metodológica")
st.markdown("""
- INEGI cambió el **año base** del PIB varias veces (1993, 2003, 2008, 2013, 2018, 2024); cada
  cambio recalcula la serie. Las tasas usadas provienen de la **serie retropolada** oficial.
- **2024 y 2025 son preliminares** y se revisan en cada publicación.
- El agregado por sexenio depende de cómo se atribuye el año de transición (aquí se usó año
  calendario completo; 1982 → López Portillo, 2024 → AMLO, 2025 → Sheinbaum).
""")
st.caption("Fuentes: INEGI (SCNM, series originales), Banco de México, FMI WEO. "
           "Reproducible: `scripts/analisis.py`.")
