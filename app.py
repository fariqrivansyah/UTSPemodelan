import streamlit as st
import numpy as np
from scipy.integrate import odeint
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

st.title("📢 Simulasi Penyebaran Informasi Hoaks di Media Sosial (Model SIR Termodifikasi)")

st.write("""
Model SIR termodifikasi digunakan untuk mensimulasikan penyebaran hoaks dengan empat kompartemen:
- **S**: Susceptible (rentan terpapar hoaks)
- **I**: Infected (menyebarkan hoaks)
- **R**: Recovered (sadar bahwa itu hoaks)
- **H**: Hoax Believer (percaya hoaks jangka panjang)

Persamaan model:

dS/dt = – β S I  
dI/dt = β S I – γ I – α I  
dR/dt = γ I  
dH/dt = α I
""")

# -------------------------
# Input parameter via Streamlit
# -------------------------
beta = st.slider("Tingkat Penyebaran Hoaks (β)", 0.01, 1.0, 0.5)
gamma = st.slider("Tingkat Penyadaran Anti-Hoaks (γ)", 0.01, 1.0, 0.2)
alpha = st.slider("Tingkat Menjadi Pemercaya Hoaks (α)", 0.01, 1.0, 0.1)

S0 = st.number_input("Populasi Rentan Awal (S0)", 0, 10000, 9900)
I0 = st.number_input("Populasi Terpapar Hoaks Awal (I0)", 0, 10000, 50)
R0 = st.number_input("Populasi Sadar Hoaks (R0)", 0, 10000, 0)
H0 = st.number_input("Pemercaya Hoaks Awal (H0)", 0, 10000, 50)

# Waktu simulasi
t = np.linspace(0, 50, 300)

# -------------------------
# Model SIR termodifikasi
# -------------------------
def modified_sir(y, t, beta, gamma, alpha):
    S, I, R, H = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I - alpha * I
    dRdt = gamma * I
    dHdt = alpha * I
    return [dSdt, dIdt, dRdt, dHdt]

y0 = [S0, I0, R0, H0]
solution = odeint(modified_sir, y0, t, args=(beta, gamma, alpha))
S, I, R, H = solution.T

# -------------------------
# Plot grafik
# -------------------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(t, S, label="Susceptible")
ax.plot(t, I, label="Infected (Hoax Spreaders)")
ax.plot(t, R, label="Recovered (Aware)")
ax.plot(t, H, label="Hoax Believers")
ax.set_xlabel("Waktu")
ax.set_ylabel("Populasi")
ax.set_title("Simulasi Penyebaran Hoaks Menggunakan Model SIR Termodifikasi")
ax.legend()

st.pyplot(fig)


    
      
    
