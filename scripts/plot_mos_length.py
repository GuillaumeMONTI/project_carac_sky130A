import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NFET_FILE = ROOT / "work/tb_nfet_01v8_length.dat"
PFET_FILE = ROOT / "work/tb_pfet_01v8_length.dat"

OUT = ROOT / "report/figures/mos_dc"
OUT.mkdir(parents=True, exist_ok=True)

W_UM = 10.0

L_ALL = np.array([0.18, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 10.0])

# Representative lengths shown in the report
L_PLOT = [0.18, 0.5, 2.0, 10.0]

# Avoid numerical garbage at extremely small currents
JD_MIN = 1e-10   # A/um


# ============================================================
# Load data
#
# NFET columns:
# 0  v-sweep
# 1  L
# 2  VGS
# 3  ID
# 4  gm
# 5  gds
# 6  gm/ID
# 7  gm/gds
# 8  VTH
# 9  VDSAT
#
# PFET columns:
# 0  v-sweep
# 1  L
# 2  |ID|
# 3  |gm|
# 4  |gds|
# 5  gm/ID
# 6  gm/gds
# 7  |VTH|
# 8  |VDSAT|
# ============================================================

n = np.loadtxt(NFET_FILE, skiprows=1)
p = np.loadtxt(PFET_FILE, skiprows=1)

Ln = n[:, 1]
Lp = p[:, 1]

vgs_n = n[:, 2]

id_n = n[:, 3]
gmid_n = n[:, 6]
gain_n = n[:, 7]
vth_n = n[:, 8]

id_p = p[:, 2]
gmid_p = p[:, 5]
gain_p = p[:, 6]
vth_p = p[:, 7]

jd_n = id_n / W_UM
jd_p = id_p / W_UM


# ============================================================
# 1) Threshold voltage versus L
#
# Use the high-gate-bias point of each length sweep.
# ============================================================

vth_n_L = []
vth_p_L = []

for L in L_ALL:

    mn = np.isclose(Ln, L)
    mp = np.isclose(Lp, L)

    # NFET sweep runs VGS = 0 -> 1.8
    idx_n = np.argmax(vgs_n[mn])
    vth_n_L.append(vth_n[mn][idx_n])

    # PFET sweep runs source VSG = 1.8 -> 0,
    # therefore maximum actual VSG occurs at the LAST row.
    vth_p_L.append(vth_p[mp][-1])

vth_n_L = np.array(vth_n_L)
vth_p_L = np.array(vth_p_L)

plt.figure(figsize=(6.5, 4.2))

plt.plot(L_ALL, vth_n_L, marker="o", label="NMOS")
plt.plot(L_ALL, vth_p_L, marker="o", label="PMOS")

plt.xlabel(r"Channel length $L$ ($\mu$m)")
plt.ylabel(r"Threshold-voltage magnitude $|V_{TH}|$ (V)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    OUT / "vth_vs_length_01v8.pdf",
    bbox_inches="tight"
)
plt.close()


# ============================================================
# 2) gm/ID versus current density
#
# Solid lines: NMOS
# Dashed lines: PMOS
# ============================================================

plt.figure(figsize=(6.5, 4.2))

for L in L_PLOT:

    mn = (
        np.isclose(Ln, L)
        & np.isfinite(gmid_n)
        & (jd_n >= JD_MIN)
        & (gmid_n > 0)
    )

    mp = (
        np.isclose(Lp, L)
        & np.isfinite(gmid_p)
        & (jd_p >= JD_MIN)
        & (gmid_p > 0)
    )

    # Sort by current density
    on = np.argsort(jd_n[mn])
    op = np.argsort(jd_p[mp])

    line_n, = plt.semilogx(
        jd_n[mn][on],
        gmid_n[mn][on],
        label=rf"NMOS $L={L:g}\,\mu$m"
    )

    plt.semilogx(
        jd_p[mp][op],
        gmid_p[mp][op],
        linestyle="--",
        label=rf"PMOS $L={L:g}\,\mu$m"
    )

plt.xlabel(r"Current density $|I_D|/W$ (A/$\mu$m)")
plt.ylabel(r"$g_m/I_D$ (V$^{-1}$)")
plt.grid(True, which="both", alpha=0.3)
plt.legend(fontsize=7)
plt.tight_layout()

plt.savefig(
    OUT / "gmid_vs_current_density_length_01v8.pdf",
    bbox_inches="tight"
)
plt.close()


# ============================================================
# 3) Intrinsic gain versus gm/ID
# ============================================================

plt.figure(figsize=(6.5, 4.2))

for L in L_PLOT:

    mn = (
        np.isclose(Ln, L)
        & np.isfinite(gmid_n)
        & np.isfinite(gain_n)
        & (jd_n >= JD_MIN)
        & (gmid_n > 0)
        & (gain_n > 0)
    )

    mp = (
        np.isclose(Lp, L)
        & np.isfinite(gmid_p)
        & np.isfinite(gain_p)
        & (jd_p >= JD_MIN)
        & (gmid_p > 0)
        & (gain_p > 0)
    )

    on = np.argsort(gmid_n[mn])
    op = np.argsort(gmid_p[mp])

    gain_n_db = 20*np.log10(gain_n[mn][on])
    gain_p_db = 20*np.log10(gain_p[mp][op])

    plt.plot(
        gmid_n[mn][on],
        gain_n_db,
        label=rf"NMOS $L={L:g}\,\mu$m"
    )

    plt.plot(
        gmid_p[mp][op],
        gain_p_db,
        linestyle="--",
        label=rf"PMOS $L={L:g}\,\mu$m"
    )

plt.xlabel(r"$g_m/I_D$ (V$^{-1}$)")
plt.ylabel(r"Intrinsic gain $20\log_{10}(g_m/g_{ds})$ (dB)")
plt.grid(True, alpha=0.3)
plt.legend(fontsize=7)
plt.tight_layout()

plt.savefig(
    OUT / "intrinsic_gain_db_vs_gmid_length_01v8.pdf",
    bbox_inches="tight"
)
plt.close()


# ============================================================
# Print threshold table for sanity checking
# ============================================================

print()
print("Threshold voltage versus channel length")
print("-----------------------------------------")
print(" L [um]      NMOS VTH [V]      PMOS |VTH| [V]")

for L, vn, vp in zip(L_ALL, vth_n_L, vth_p_L):
    print(f"{L:6.2f}        {vn:8.4f}          {vp:8.4f}")

print()
print("Generated:")
print(OUT / "vth_vs_length_01v8.pdf")
print(OUT / "gmid_vs_current_density_length_01v8.pdf")
print(OUT / "intrinsic_gain_vs_gmid_length_01v8.pdf")
