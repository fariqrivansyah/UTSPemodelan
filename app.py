import streamlit as st
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go

# -------------------------------
# UI GENERAL
# -------------------------------
st.set_page_config(
    page_title="Simulasi Hoaks SIR Termodifikasi",
    page_icon="📢",
    layout="wide"
)

st.title("📢 Simulasi Penyebaran Informasi Hoaks di Media Sosial")
st.subheader("Model SIR Termodifikasi • Grafik Plotly Interaktif")

st.markdown("""
Model ini mensimulasikan penyebaran hoaks dengan 4 kompartemen:

- 🟦 **S — Susceptible** (Rentan)
- 🟥 **I — Infected** (Menyebarkan Hoaks)
- 🟩 **R — Recovered** (Sadar Hoaks)
- 🟨 **H — Hoax Believer** (Percaya Jangka Panjang)

### Persamaan Model *(ODE)*

- dS/dt = – β S I  
- dI/dt = β S I – γ I – α I  
- dR/dt = γ I  
- dH/dt = α I  
""")

st.write("---")

# -------------------------------
# INPUT PARAMETER
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    beta = st.slider("Tingkat Penyebaran Hoaks (β)", 0.01, 1.0, 0.4)
    gamma = st.slider("Tingkat Penyadaran (γ)", 0.01, 1.0, 0.2)

with col2:
    alpha = st.slider("Tingkat Menjadi Pemercaya Hoaks (α)", 0.01, 1.0, 0.1)
    duration = st.slider("Durasi Simulasi (Hari)", 10, 200, 80)

st.write("## 🧮 Kondisi Awal Populasi")

col3, col4, col5, col6 = st.columns(4)
with col3:
    S0 = st.number_input("S0 (Rentan)", 0, 100000, 9000)
with col4:
    I0 = st.number_input("I0 (Terpapar Hoaks)", 0, 100000, 100)
with col5:
    R0 = st.number_input("R0 (Sadar Hoaks)", 0, 100000, 0)
with col6:
    H0 = st.number_input("H0 (Percaya Hoaks)", 0, 100000, 50)

# -------------------------------
# MODEL ODE
# -------------------------------
t = np.linspace(0, duration, 500)

def sir_modified(y, t, beta, gamma, alpha):
    S, I, R, H = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I - alpha * I
    dRdt = gamma * I
    dHdt = alpha * I
    return [dSdt, dIdt, dRdt, dHdt]

y0 = [S0, I0, R0, H0]
result = odeint(sir_modified, y0, t, args=(beta, gamma, alpha))
S, I, R, H = result.T

# -------------------------------
# PLOTLY GRAPH INTERAKTIF
# -------------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Rentan (S)', line=dict(width=3)))
fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Penyebar Hoaks (I)', line=dict(width=3)))
fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Sadar Hoaks (R)', line=dict(width=3)))
fig.add_trace(go.Scatter(x=t, y=H, mode='lines', name='Percaya Hoaks (H)', line=dict(width=3)))

fig.update_layout(
    title="📊 Grafik Penyebaran Hoaks (Plotly Interaktif)",
    xaxis_title="Waktu (hari)",
    yaxis_title="Jumlah Populasi",
    hovermode="x unified",
    template="plotly_dark",
    legend=dict(orientation="h", y=-0.2),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# OUTPUT STATISTIK
# -------------------------------
st.write("## 📌 Statistik Akhir Simulasi")

colA, colB, colC, colD = st.columns(4)
colA.metric("Rentan Akhir (S)", f"{S[-1]:.2f}")
colB.metric("Penyebar (I)", f"{I[-1]:.2f}")
colC.metric("Sadar Hoaks (R)", f"{R[-1]:.2f}")
colD.metric("Pemercaya Hoaks (H)", f"{H[-1]:.2f}")
