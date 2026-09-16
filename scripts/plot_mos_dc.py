import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NFET_FILE = ROOT / "work/tb_nfet_01v8_dc.dat"
PFET_FILE = ROOT / "work/tb_pfet_01v8_dc.dat"

OUT = ROOT / "report/figures/mos_dc"
OUT.mkdir(parents=True, exist_ok=True)

W_UM = 10.0


# ============================================================
# Load ngspice wrdata files
#
# NFET columns:
# 0: v-sweep
# 1: VGS
# 2: ID
# 3: gm
# 4: gds
# 5: ro
# 6: gm/ID
# 7: gm/gds
# 8: VTH
# 9: VDSAT
#
# PFET columns:
# 0: v-sweep
# 1: VSG
# 2: |ID|
# 3: |gm|
# 4: |gds|
# 5: ro
# 6: gm/ID
# 7: gm/gds
# 8: |VTH|
# 9: |VDSAT|
# ============================================================

n = np.loadtxt(NFET_FILE, skiprows=1)
p = np.loadtxt(PFET_FILE, skiprows=1)

vgs_n = n[:, 1]
id_n = n[:, 2]
gmid_n = n[:, 6]
gain_n = n[:, 7]

vsg_p = p[:, 1]
id_p = p[:, 2]
gmid_p = p[:, 6]
gain_p = p[:, 7]


# ============================================================
# 1) Transfer characteristic
# ============================================================

plt.figure(figsize=(6.5, 4.2))

plt.semilogy(vgs_n, id_n, label="NMOS")
plt.semilogy(vsg_p, id_p, label="PMOS")

plt.xlabel(r"Gate-source voltage $V_{GS}$ / $V_{SG}$ (V)")
plt.ylabel(r"Drain current $|I_D|$ (A)")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(OUT / "id_vs_vg_01v8.pdf", bbox_inches="tight")
plt.close()


# ============================================================
# 2) gm/ID versus current density
# ============================================================

jd_n = id_n / W_UM
jd_p = id_p / W_UM

JD_MIN = 1e-10  # A/um

mask_n = (
    np.isfinite(gmid_n)
    & (jd_n >= JD_MIN)
    & (gmid_n > 0)
)

mask_p = (
    np.isfinite(gmid_p)
    & (jd_p >= JD_MIN)
    & (gmid_p > 0)
)

plt.figure(figsize=(6.5, 4.2))

plt.semilogx(jd_n[mask_n], gmid_n[mask_n], label="NMOS")
plt.semilogx(jd_p[mask_p], gmid_p[mask_p], label="PMOS")

plt.xlabel(r"Current density $|I_D|/W$ (A/$\mu$m)")
plt.ylabel(r"$g_m/I_D$ (V$^{-1}$)")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(OUT / "gmid_vs_current_density_01v8.pdf",
            bbox_inches="tight")
plt.close()


# ============================================================
# 3) Intrinsic gain versus gm/ID
# ============================================================

mask_n = (
    np.isfinite(gmid_n)
    & np.isfinite(gain_n)
    & (jd_n >= JD_MIN)
    & (gmid_n > 0)
    & (gain_n > 0)
)

mask_p = (
    np.isfinite(gmid_p)
    & np.isfinite(gain_p)
    & (jd_p >= JD_MIN)
    & (gmid_p > 0)
    & (gain_p > 0)
)

plt.figure(figsize=(6.5, 4.2))

plt.plot(gmid_n[mask_n], gain_n[mask_n], label="NMOS")
plt.plot(gmid_p[mask_p], gain_p[mask_p], label="PMOS")

plt.xlabel(r"$g_m/I_D$ (V$^{-1}$)")
plt.ylabel(r"Intrinsic gain $g_m/g_{ds}$")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(OUT / "intrinsic_gain_vs_gmid_01v8.pdf",
            bbox_inches="tight")
plt.close()


print("Generated:")
for f in sorted(OUT.glob("*.pdf")):
    print(" -", f)
