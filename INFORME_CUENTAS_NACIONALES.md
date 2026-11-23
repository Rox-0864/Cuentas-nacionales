# Informe — Cuentas nacionales de México por sexenio (1983–2024)

> Análisis del crecimiento del PIB real (y per cápita) de México, agregado por
> sexenios, para los últimos ~40 años.

---

## 1. Crecimiento del PIB por sexenio

Media geométrica anual (año calendario):

| Sexenio | Periodo | Anual prom. | Acumulado |
|---|---|---|---|
| Miguel de la Madrid | 1983–1988 | **0.1%** | 0.4% |
| Carlos Salinas | 1989–1994 | **4.1%** | 27.0% |
| Ernesto Zedillo | 1995–2000 | **3.3%** | 21.2% |
| Vicente Fox | 2001–2006 | **1.9%** | 12.2% |
| Felipe Calderón | 2007–2012 | **1.7%** | 10.6% |
| Enrique Peña Nieto | 2013–2018 | **2.4%** | 15.3% |
| AMLO | 2019–2024 | **0.9%** | 5.6% |

*(Sheinbaum 2025: 0.5%, dato preliminar, un solo año.)*

## 2. PIB per cápita por sexenio (FMI WEO)

| Sexenio | PIB per cápita anual |
|---|---|
| De la Madrid | −2.2% |
| Salinas | +2.1% |
| Zedillo | +2.0% |
| Fox | +0.4% |
| Calderón | −0.1% |
| Peña Nieto | +0.8% |
| AMLO | 0.0% |

## 3. Lectura

1. **Dos regímenes claros**: de 1983 a 2000 la economía creció ~3-4% anual (a
   pesar de las crisis de 1982, 1986 y 1994); de 2001 en adelante cayó a un
   rango de **1.7-2.4%** ("crecimiento mediocre"), y con AMLO a **0.9%**
   (el más bajo desde De la Madrid, marcado por la pandemia 2020, −8.2%).

2. **Las crisis están repartidas, no siempre "culpa" del presidente en turno**:
   Zedillo absorbió la crisis de 1994 (heredada de Salinas) y aun así creció 3.3%;
   Calderón la crisis global de 2009; AMLO la pandemia de 2020.

3. **El per cápita lo dice crudo**: desde 2001 la economía apenas genera más
   producto por persona (Fox +0.4%, Calderón −0.1%, Peña +0.8%, AMLO 0.0%).
   Con una población que crece ~1% anual, un PIB que crece ~1-2% deja el ingreso
   por habitante prácticamente estancado por más de dos décadas.

## 4. Nota metodológica (importante)

El PIB de INEGI ha cambiado de **año base** varias veces (1993, 2003, 2008, 2013,
2018 y 2024), y cada cambio **recalcula** la serie. Las tasas de crecimiento que
se comparan aquí provienen de la **serie retropolada** oficial (series originales),
que INEGI reconstruye encadenando las bases. Aun así:

- Los años **2024 y 2025 son preliminares** y se revisan con cada publicación.
- El dato de 2025 (0.5%) es la cifra más reciente y aún no definitiva.
- Los agregados por sexenio dependen de **cómo se atribuye el año de transición**
  (1982 a López Portillo, 2024 repartido entre AMLO y Sheinbaum por el cambio de
  fecha de toma de posesión). Aquí se usó la convención de año calendario completo.

---

## 5. Reproducir

```bash
python scripts/analisis.py      # agrega por sexenio + gráficos
streamlit run app.py            # dashboard
```

Datos en `data/`; gráficos en `results/`. Fuentes: INEGI (SCNM, series originales),
Banco de México, FMI WEO.
