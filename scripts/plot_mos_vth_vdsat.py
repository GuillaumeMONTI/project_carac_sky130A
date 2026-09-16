import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NFET_FILE = ROOT / "work/tb_nfet_01v8_dc.dat"
PFET_FILE = ROOT / "work/tb_pfet_01v8_dc.dat"

OUT = ROOT / "report/figures/mos_dc"
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# Load data
#
# columns:
# 0 sweep
# 1 VGS / VSG
# 2 ID
# 3 gm
# 4 gds
# 5 ro
# 6 gm/ID
# 7 gm/gds
# 8 VTH / |VTH|
# 9 VDSAT / |VDSAT|
# ============================================================

n = np.loadtxt(NFET_FILE, skiprows=1)
p = np.loadtxt(PFET_FILE, skiprows=1)

vgs = n[:, 1]
vsg = p[:, 1]

vth_n = n[:, 8]
vth_p = p[:, 8]

vdsat_n = n[:, 9]
vdsat_p = p[:, 9]

id_n = n[:, 2]
id_p = p[:, 2]


# ============================================================
# Reference values at maximum gate bias
# ============================================================

i_n = np.argmax(vgs)
i_p = np.argmax(vsg)

print("Reference point at VG = 1.8 V")
print("--------------------------------")
print(f"NMOS VTH   = {vth_n[i_n]:.4f} V")
print(f"PMOS |VTH| = {vth_p[i_p]:.4f} V")
print(f"NMOS VDSAT = {vdsat_n[i_n]:.4f} V")
print(f"PMOS VSDAT = {vdsat_p[i_p]:.4f} V")
print(f"NMOS ID    = {id_n[i_n]*1e3:.4f} mA")
print(f"PMOS |ID|  = {id_p[i_p]*1e3:.4f} mA")
print(f"ID ratio N/P = {id_n[i_n]/id_p[i_p]:.2f}")


# ============================================================
# VDSAT versus gate voltage
# ============================================================

plt.figure(figsize=(6.5, 4.2))

plt.plot(vgs, vdsat_n, label="NMOS")
plt.plot(vsg, vdsat_p, label="PMOS")

plt.xlabel(r"Gate-source voltage $V_{GS}$ / $V_{SG}$ (V)")
plt.ylabel(r"Saturation-voltage magnitude $|V_{DSAT}|$ (V)")
plt.xlim(0, 1.8)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    OUT / "vdsat_vs_vg_01v8.pdf",
    bbox_inches="tight"
)

plt.close()

print()
print("Generated:")
print(OUT / "vdsat_vs_vg_01v8.pdf")
