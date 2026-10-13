"""Parte 0.2 – Simulación de procesos AR(1)."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def acf_manual(y, k):
    """r_k estimada a mano (misma fórmula del enunciado)."""
    y = np.asarray(y, float)
    n = len(y)
    d = y - y.mean()
    return np.sum(d[k:] * d[:n - k]) / np.sum(d ** 2)


def simular_ar1(phi, n=300, burn=200, c=0.0, sigma=1.0, rng=None):
    """Simula n pasos de un AR(1), descartando los primeros `burn`."""
    rng = rng or np.random.default_rng()
    eps = rng.normal(0, sigma, n + burn)
    y = np.zeros(n + burn)
    prev = 0.0
    for t in range(n + burn):
        y[t] = c + phi * prev + eps[t]
        prev = y[t]
    return y[burn:]


def ols_phi(y):
    """Estimado OLS de phi: y_t contra y_{t-1} con intercepto."""
    X = np.column_stack([np.ones(len(y) - 1), y[:-1]])
    return np.linalg.lstsq(X, y[1:], rcond=None)[0][1]


N, R = 300, 5000
BANDA = 1.96 / np.sqrt(N)
SEMILLAS = {0: 101, 0.5: 102, 0.9: 103, 1: 104}  # una semilla por escenario

# --- Gráfica: una realización de cada phi ---
fig, axes = plt.subplots(4, 1, figsize=(9, 9), sharex=True)
for ax, (phi, s) in zip(axes, SEMILLAS.items()):
    y = simular_ar1(phi, N, rng=np.random.default_rng(s + 1000))
    ax.plot(y, lw=0.9)
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_title(f"AR(1) con $\\phi$ = {phi}", fontsize=10)
axes[-1].set_xlabel("t")
fig.tight_layout()
fig.savefig("fig_0_2_realizaciones.png", dpi=150)

# --- Tabla: 5 000 réplicas por phi ---
se = lambda v: np.std(v, ddof=1) / np.sqrt(len(v))
filas = []
for phi, s in SEMILLAS.items():
    rng = np.random.default_rng(s)
    r1, r5, rech, ph = [], [], [], []
    for _ in range(R):
        y = simular_ar1(phi, N, rng=rng)
        a1 = acf_manual(y, 1)
        r1.append(a1)
        r5.append(acf_manual(y, 5))
        rech.append(float(abs(a1) > BANDA))
        ph.append(ols_phi(y))
    filas.append({
        "phi": phi,
        "r1 prom": np.mean(r1), "EE r1": se(r1),
        "r5 prom": np.mean(r5), "EE r5": se(r5), "phi^5": phi ** 5,
        "tasa rechazo": np.mean(rech), "EE tasa": se(rech),
        "phi OLS prom": np.mean(ph), "EE phi OLS": se(ph),
    })

tabla = pd.DataFrame(filas).round(4)
print(tabla.to_string(index=False))
tabla.to_csv("tabla_0_2.csv", index=False)
