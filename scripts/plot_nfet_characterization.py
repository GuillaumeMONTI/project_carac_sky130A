#!/usr/bin/env python3

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# Project paths

IP_PATH = Path("/foss/designs/project_carac_sky130A")

DATA_FILE = ( 
	IP_PATH
	/ "results/mos/nfet_01v8/tt/data"
	/ "nfet_01v8_tt_L0p5_VDS0p9.dat"
)

PLOT_DIR = ( 
	IP_PATH
	/ "results/mos/nfet_01v8/tt/data"
	/ "nfet_01v8_tt_L0p5_VDS0p9.dat"
)

PLOT_DIR = (
	IP_PATH
	/ "results/mos/nfet_01v8/tt/plots"
)

PLOT_DIR.mkdir(parents=True, exist_ok=True)

# Device information

DEVICE = "sky130_fd_pr__nfet_01v8"
W_UM = 10.0
L_UM = 0.5
VDS = 0.9
CORNER = "TT"
TEMP_C = 27

# Load ngspice data output

data = np.loadtxt(DATA_FILE, skiprows=1)

vgs    = data[:, 1]
ids    = data[:, 2]
gm     = data[:, 3]
gds    = data[:, 4]
vth    = data[:, 5]
gm_id  = data[:, 6]
gm_gds = data[:, 7]
id_w   = data[:, 8]

# Remove near zero current points

valid = (
	np.isfinite(ids)
	& np.isfinite(gm)
	& np.isfinite(gds)
	& np.isfinite(gm_id)
	& np.isfinite(gm_gds)
	& (ids > 1e-10)
	& (gm > 0)
	& (gds > 0)
)

vgs_f = vgs[valid]
ids_f = ids[valid]
gm_id_f = gm_id[valid]
gm_gds_f = gm_gds[valid]
id_w_f = id_w[valid]

description = (
	f"{DEVICE}, w={W_UM:g} µm, L={L_UM:g} µm, "
	f"VDS={VDS:g} V, {CORNER}, {TEMP_C} °C"
)

# Id vs Vgs

plt.figure(figsize=(8, 5))

plt.plot(vgs, ids * 1e3)

plt.xlabel("VGS [V]")
plt.ylabel("ID [mA]")
plt.title("SKY130 NFET - ID vs VGS")

plt.grid(True)
plt.tight_layout()

plt.savefig(
	PLOT_DIR / "id_vs_vgs.png",
	dpi = 200,
)

plt.close()

# gm/Id vs Id/W

plt.figure(figsize=(8, 5))

plt.semilogx(id_w_f, gm_id_f)

plt.xlabel("ID/W [A/m]")
plt.ylabel("gm/ID [V^-1]")
plt.title("SKY130 NFET - gm/ID vs ID/W")

plt.grid(True)
plt.tight_layout()

plt.savefig(
        PLOT_DIR / "gmid_vs_idw.png",
        dpi = 200,
)

plt.close()

# gm/gds vs gm/Id

plt.figure(figsize=(8, 5))

plt.plot(gm_id_f, gm_gds_f)

plt.xlabel("gm/ID [V^⁻1]")
plt.ylabel("gm/gds [V/V]")
plt.title("SKY130 NFET - Gain vs gm/Id")

plt.grid(True)
plt.tight_layout()

plt.savefig(
        PLOT_DIR / "gmgds_vs_gmid.png",
        dpi = 200,
)

plt.close()

print(f"Loaded: {DATA_FILE}")
print(f"Valid characterization points: {valid.sum()} / {len(valid)}")
print(f"Plots written to: {PLOT_DIR}")
print(description)
