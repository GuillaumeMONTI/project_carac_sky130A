# SKY130A Analog MOS Characterization

Open-source characterization of selected SKY130A MOS devices for practical analog IC design using **Xschem**, **ngspice**, **Python**, and **IIC-OSIC-TOOLS**.

The objective of this project is not to reproduce MOS transistor theory or exhaustively characterize the complete PDK. Instead, it provides a compact set of device-level references that can be reused for transistor selection, biasing, and sizing in future analog IC projects.

---

## PDF Report

### [View the complete characterization report](report/report_project_carac_sky130A.pdf)

The report contains:

- characterization methodology and Xschem testbenches,
- drain-current transfer characteristics,
- output-characteristic families,
- threshold voltage \(V_{TH}\),
- saturation voltage \(V_{DSAT}\),
- \(g_m/I_D\) sizing data,
- MOS gate-capacitance characterization,
- native-NMOS characterization,
- a compact device quick-reference table.

---

## Characterized Devices

The current project focuses on device families that are expected to be useful in subsequent analog designs.

### Standard 1.8-V MOS

- `sky130_fd_pr__nfet_01v8`
- `sky130_fd_pr__pfet_01v8`

Characterized for:

- \(I_D(V_{GS})\)
- \(I_D(V_{DS})\)
- \(V_{TH}\)
- \(V_{DSAT}\)
- \(g_m/I_D\)
- gate capacitance versus bias
- gate-capacitance density versus geometry

### Native NMOS

- `sky130_fd_pr__nfet_03v3_nvt`
- `sky130_fd_pr__nfet_05v0_nvt`

Characterized for:

- transfer characteristics,
- output characteristics,
- near-zero threshold behaviour,
- \(g_m/I_D\).

The `nfet_05v0_nvt` compact model supports only a restricted set of characterized geometries. The reference geometry used in this project is therefore \(W/L = 10/2~\mu m/\mu m\).

---

## Device Quick Reference

Nominal **TT, 27 °C** results:

| Device | Reference W/L (µm/µm) | \|VGS\| model range (V) | \|VDS\| model range (V) | VTH (V) | \|VDSAT\| (V) | \|ID\|/W (mA/µm) |
|---|---:|---:|---:|---:|---:|---:|
| `nfet_01v8` | 10 / 0.5 | 1.95 | 1.95 | +0.611 | 0.573 | 0.220 |
| `pfet_01v8` | 10 / 0.5 | 1.95 | 1.95 | -0.992 | 0.695 | 0.0419 |
| `nfet_03v3_nvt` | 10 / 0.5 | 3.3 | 3.3 | -0.0133 | 1.032 | 0.512 |
| `nfet_05v0_nvt` | 10 / 2 | 5.5 | 5.5 | +0.0529 | 3.159 | 0.341 |

Reference extraction biases:

- `nfet_01v8`: \(V_{GS}=1.8~V,\ V_{DS}=0.9~V\)
- `pfet_01v8`: \(V_{SG}=1.8~V,\ V_{SD}=0.9~V\)
- `nfet_03v3_nvt`: \(V_{GS}=3.3~V,\ V_{DS}=1.65~V\)
- `nfet_05v0_nvt`: \(V_{GS}=5.0~V,\ V_{DS}=2.5~V\)

> The voltage values listed as model ranges correspond to documented SKY130 SPICE-model operating ranges. They should not be interpreted as absolute-maximum device ratings.

For bias-dependent and geometry-dependent results, see the full PDF report.

---

## Why These Characterizations?

The generated data are intended to answer practical design questions.

| Characterization | Design use |
|---|---|
| \(I_D(V_{GS})\) | Gate-bias selection and current capability |
| \(I_D(V_{DS})\) | Output behaviour and saturation region |
| \(V_{TH}\) | Threshold and geometry dependence |
| \(V_{DSAT}\) | Voltage-headroom estimation |
| \(g_m/I_D\) | Analog transistor sizing and inversion-level selection |
| \(C_G\) | Gate-loading and capacitive-cost estimation |

The goal is to reuse these results in future circuit projects rather than restarting device characterization for every design.

---

## Tools

The project uses a fully open-source analog IC design flow:

- **PDK:** SKY130A
- **Schematic capture:** Xschem
- **Simulation:** ngspice
- **Environment:** IIC-OSIC-TOOLS
- **Post-processing:** Python / NumPy / Matplotlib
- **Documentation:** LaTeX

---

## Repository Structure

```text
project_carac_sky130A/
│
├── dfii/
│   └── project_carac_sky130A_sim/
│       ├── tb_nfet_01v8_dc.sch
│       ├── tb_pfet_01v8_dc.sch
│       ├── tb_nfet_01v8_id_vds.sch
│       ├── tb_pfet_01v8_id_vsd.sch
│       ├── tb_mos_01v8_moscap.sch
│       ├── tb_nfet_03v3_nvt_dc.sch
│       ├── tb_nfet_03v3_nvt_id_vds.sch
│       ├── tb_nfet_05v0_nvt_dc.sch
│       └── tb_nfet_05v0_nvt_id_vds.sch
│
├── models/
│   └── reduced/
│       └── sky130_tt.red
│
├── scripts/
│   ├── plot_mos_dc.py
│   ├── plot_mos_length.py
│   ├── plot_mos_output.py
│   ├── plot_mos_vth_vdsat.py
│   ├── plot_moscap.py
│   ├── plot_nfet_03v3_nvt.py
│   └── plot_nfet_05v0_nvt.py
│
├── work/
│   └── simulation data
│
└── report/
    ├── figures/
    ├── sections/
    ├── bibliography/
    ├── report_project_carac_sky130A.tex
    └── report_project_carac_sky130A.pdf
