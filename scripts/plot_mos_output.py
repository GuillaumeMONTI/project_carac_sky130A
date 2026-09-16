import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NFET_FILE = ROOT / "work/tb_nfet_01v8_id_vds.dat"
PFET_FILE = ROOT / "work/tb_pfet_01v8_id_vsd.dat"

OUT = ROOT / "report/figures/mos_dc"
OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# Load data
#
# NFET:
# col 0 = ngspice sweep variable
# col 1 = VDS
# col 2 = VGS
# col 3 = ID
#
# PFET:
# col 0 = ngspice sweep variable
# col 1 = VSD
# col 2 = VSG
# col 3 = |ID|
# ============================================================

n = np.loadtxt(NFET_FILE, skiprows=1)
p = np.loadtxt(PFET_FILE, skiprows=1)

vds = n[:, 1]
vgs = n[:, 2]
id_n = n[:, 3] * 1e3     # A -> mA

vsd = p[:, 1]
vsg = p[:, 2]
id_p = p[:, 3] * 1e3     # A -> mA

gate_values = np.arange(0.6, 1.81, 0.2)


# ============================================================
# NMOS output characteristics
# ============================================================

plt.figure(figsize=(6.5, 4.2))

for vg in gate_values:
    mask = np.isclose(vgs, vg, atol=1e-6)

    x = vds[mask]
    y = id_n[mask]

    order = np.argsort(x)

    plt.plot(
        x[order],
        y[order],
        label=rf"$V_{{GS}}={vg:.1f}$ V"
    )

plt.xlabel(r"Drain-source voltage $V_{DS}$ (V)")
plt.ylabel(r"Drain current $I_D$ (mA)")
plt.xlim(0, 1.8)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=8)
plt.tight_layout()

plt.savefig(
    OUT / "id_vs_vds_01v8_nmos.pdf",
    bbox_inches="tight"
)
plt.close()


# ============================================================
# PMOS output characteristics
# ============================================================

plt.figure(figsize=(6.5, 4.2))

for vg in gate_values:
    mask = np.isclose(vsg, vg, atol=1e-6)

    x = vsd[mask]
    y = id_p[mask]

    order = np.argsort(x)

    plt.plot(
        x[order],
        y[order],
        label=rf"$V_{{SG}}={vg:.1f}$ V"
    )

plt.xlabel(r"Source-drain voltage $V_{SD}$ (V)")
plt.ylabel(r"Drain current magnitude $|I_D|$ (mA)")
plt.xlim(0, 1.8)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=8)
plt.tight_layout()

plt.savefig(
    OUT / "id_vs_vsd_01v8_pmos.pdf",
    bbox_inches="tight"
)
plt.close()


print("Generated:")
print(OUT / "id_vs_vds_01v8_nmos.pdf")
print(OUT / "id_vs_vsd_01v8_pmos.pdf")
