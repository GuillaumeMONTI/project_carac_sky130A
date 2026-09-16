import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DC_FILE = ROOT / "work/tb_nfet_05v0_nvt_dc.dat"
OUTPUT_FILE = ROOT / "work/tb_nfet_05v0_nvt_id_vds.dat"

OUT = ROOT / "report/figures/native"
OUT.mkdir(parents=True, exist_ok=True)

W_UM = 10.0


# ============================================================
# Transfer characteristic
#
# DC file columns:
# 0 : ngspice sweep
# 1 : VGS
# 2 : ID
# ============================================================

dc = np.loadtxt(DC_FILE, skiprows=1)

vgs = dc[:, 1]
id_ = dc[:, 2]


# ============================================================
# Numerical gm and gm/ID
# ============================================================

gm = np.gradient(id_, vgs)

gmid = np.full_like(id_, np.nan)

# Ignore extremely small currents where numerical differentiation
# becomes meaningless.
valid = id_ > 1e-10

gmid[valid] = gm[valid] / id_[valid]

current_density = id_ / W_UM


# ============================================================
# 1) ID versus VGS
# ============================================================

mask = id_ > 0

plt.figure(figsize=(6.5, 4.2))

plt.semilogy(
    vgs[mask],
    id_[mask]
)

plt.xlabel(r"Gate-source voltage $V_{GS}$ (V)")
plt.ylabel(r"Drain current $I_D$ (A)")
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUT / "nfet_05v0_nvt_id_vs_vgs.pdf",
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 2) gm/ID versus current density
# ============================================================

mask = (
    np.isfinite(gmid)
    & (gmid > 0)
    & (current_density > 1e-11)
)

order = np.argsort(current_density[mask])

plt.figure(figsize=(6.5, 4.2))

plt.semilogx(
    current_density[mask][order],
    gmid[mask][order]
)

plt.xlabel(r"Current density $I_D/W$ (A/$\mu$m)")
plt.ylabel(r"$g_m/I_D$ (V$^{-1}$)")
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUT / "nfet_05v0_nvt_gmid.pdf",
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Output characteristics
#
# Output file columns:
# 0 : ngspice sweep
# 1 : VDS
# 2 : VGS
# 3 : ID
# ============================================================

out = np.loadtxt(OUTPUT_FILE, skiprows=1)

vds = out[:, 1]
vgs_out = out[:, 2]
id_out = out[:, 3] * 1e3   # A -> mA

gate_values = np.arange(0.0, 5.01, 1.0)


# ============================================================
# 3) ID versus VDS family
# ============================================================

plt.figure(figsize=(6.5, 4.2))

for vg in gate_values:

    mask = np.isclose(vgs_out, vg, atol=1e-6)

    x = vds[mask]
    y = id_out[mask]

    order = np.argsort(x)

    plt.plot(
        x[order],
        y[order],
        label=rf"$V_{{GS}}={vg:.1f}$ V"
    )

plt.xlabel(r"Drain-source voltage $V_{DS}$ (V)")
plt.ylabel(r"Drain current $I_D$ (mA)")
plt.xlim(0, 5.0)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=8)
plt.tight_layout()

plt.savefig(
    OUT / "nfet_05v0_nvt_id_vs_vds.pdf",
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Reference values around VGS = 0
# ============================================================

idx0 = np.argmin(np.abs(vgs))

print()
print("Native NFET reference data")
print("--------------------------")
print(f"VGS              = {vgs[idx0]:.3f} V")
print(f"ID at VGS=0      = {id_[idx0]*1e6:.2f} uA")
print(f"gm at VGS=0      = {gm[idx0]*1e6:.2f} uS")
print(f"gm/ID at VGS=0   = {gmid[idx0]:.2f} 1/V")

print()
print("Generated:")
print(OUT / "nfet_05v0_nvt_id_vs_vgs.pdf")
print(OUT / "nfet_05v0_nvt_gmid.pdf")
print(OUT / "nfet_05v0_nvt_id_vs_vds.pdf")
