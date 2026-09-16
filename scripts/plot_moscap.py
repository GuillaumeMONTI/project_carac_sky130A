import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CV_FILE = ROOT / "work/tb_mos_01v8_moscap_cv.dat"
GEOM_FILE = ROOT / "work/tb_mos_01v8_moscap_geometry.dat"

OUT = ROOT / "report/figures/moscap"
OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# Load data
# ============================================================

cv = np.loadtxt(CV_FILE, skiprows=1)

vcap = cv[:, 0]
cgn_f = cv[:, 1]
cgp_f = cv[:, 2]

# Convert F -> fF
cgn_ff = cgn_f * 1e15
cgp_ff = cgp_f * 1e15


geom = np.loadtxt(GEOM_FILE, skiprows=1)

w = geom[:, 0]
l = geom[:, 1]

cgn_geom_ff = geom[:, 2] * 1e15
cgn_density = geom[:, 3]

cgp_geom_ff = geom[:, 4] * 1e15
cgp_density = geom[:, 5]


# ============================================================
# 1) Cg versus capacitor voltage
# ============================================================

plt.figure(figsize=(6.5, 4.2))

plt.plot(vcap, cgn_ff, label="NMOS")
plt.plot(vcap, cgp_ff, label="PMOS")

plt.xlabel(r"Capacitor voltage $V_{\mathrm{CAP}}$ (V)")
plt.ylabel(r"Gate capacitance $C_G$ (fF)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(OUT / "moscap_cv_01v8.pdf")
plt.close()


# ============================================================
# 2) Normalized Cg versus L
#    Use W = 10 um
# ============================================================

mask = np.isclose(w, 10.0)

plt.figure(figsize=(6.5, 4.2))

plt.plot(l[mask], cgn_density[mask], marker="o", label="NMOS")
plt.plot(l[mask], cgp_density[mask], marker="o", label="PMOS")

plt.xlabel(r"Channel length $L$ ($\mu$m)")
plt.ylabel(r"$C_G/(WL)$ (fF/$\mu$m$^2$)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(OUT / "moscap_density_vs_l_01v8.pdf")
plt.close()


# ============================================================
# 3) Cg versus W
#    Use L = 0.5 um
# ============================================================

mask = np.isclose(l, 0.5)

plt.figure(figsize=(6.5, 4.2))

plt.plot(w[mask], cgn_geom_ff[mask], marker="o", label="NMOS")
plt.plot(w[mask], cgp_geom_ff[mask], marker="o", label="PMOS")

plt.xlabel(r"Device width $W$ ($\mu$m)")
plt.ylabel(r"Gate capacitance $C_G$ (fF)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(OUT / "moscap_cg_vs_w_01v8.pdf")
plt.close()

print(f"Plots written to: {OUT}")
