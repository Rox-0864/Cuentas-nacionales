import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Cuentas Nacionales de México", page_icon="📈", layout="wide")

@st.cache_data
def cargar():
    crec = pd.read_csv("data/pib_crecimiento_1982_2025.csv")
    sex = pd.read_csv("data/pib_por_sexenio.csv")
    pc = pd.read_csv("data/pib_percapita_por_sexenio.csv")
    return crec, sex, pc

crec, sex, pc = cargar()

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

st.header("4 · Nota metodológica")
st.markdown("""
- INEGI cambió el **año base** del PIB varias veces (1993, 2003, 2008, 2013, 2018, 2024); cada
  cambio recalcula la serie. Las tasas usadas provienen de la **serie retropolada** oficial.
- **2024 y 2025 son preliminares** y se revisan en cada publicación.
- El agregado por sexenio depende de cómo se atribuye el año de transición (aquí se usó año
  calendario completo; 1982 → López Portillo, 2024 → AMLO, 2025 → Sheinbaum).
""")
st.caption("Fuentes: INEGI (SCNM, series originales), Banco de México, FMI WEO. "
           "Reproducible: `scripts/analisis.py`.")
