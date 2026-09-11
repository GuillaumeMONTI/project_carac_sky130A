
# SKY130A Analog Device Characterization

Basic electrical characterization of the SKY130A 1.8 V core MOS devices
using an open-source analog IC design flow.

## Environment

- IIC-OSIC-TOOLS
- SKY130A open PDK
- Xschem
- ngspice

## Devices

- `sky130_fd_pr__nfet_01v8`
- `sky130_fd_pr__pfet_01v8`

## Characterization

### NMOS

- Id vs Vgs
- Id vs Vds families
- Vth
- Vdsat
- gm
- gds
- ro
- gm/Id
- gm/gds

### PMOS

- |Id| vs Vsg
- |Id| vs Vsd families
- |Vth|
- |Vdsat|
- gm
- gds
- ro
- gm/Id
- gm/gds

## Reference geometry

Initial characterization:

- W = 10 µm
- L = 0.5 µm
- VSB = 0 V
- TT corner
- T = 27 °C

## Notes

The SKY130 model deck was reduced locally using the IIC-OSIC model
reduction utility to reduce ngspice model-loading time.

The generated reduced model deck is intentionally not included in this
repository and must be regenerated locally from the installed SKY130A PDK.

## Repository structure

- `dfii/project_carac_sky130A_sim/` — Xschem characterization testbenches
- `models/` — local model-generation area
- `work/` — temporary simulation/netlist directory
- `scripts/` — optional project utilities
