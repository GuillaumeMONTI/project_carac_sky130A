v {xschem version=3.4.8RC file_version=1.3
* Copyright 2021 Stefan Frederik Schippers
* 
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.

}
G {}
K {}
V {}
S {}
F {}
E {}
N 1180 -1460 1260 -1460 {lab=vsg}
N 1180 -1400 1180 -1350 {lab=0}
N 1180 -1270 1380 -1270 {lab=0}
N 1180 -1280 1180 -1270 {lab=0}
N 1300 -1460 1310 -1460 {lab=VDD}
N 1380 -1280 1380 -1270 {lab=0}
N 1180 -1350 1180 -1280 {lab=0}
N 1300 -1430 1300 -1340 {lab=VSD}
N 1300 -1340 1380 -1340 {lab=VSD}
N 1120 -1530 1120 -1270 {lab=0}
N 1120 -1270 1180 -1270 {lab=0}
N 1120 -1660 1120 -1590 {lab=VDD}
N 1120 -1660 1300 -1660 {lab=VDD}
N 1300 -1660 1300 -1490 {lab=VDD}
N 1310 -1660 1310 -1460 {lab=VDD}
N 1290 -1660 1310 -1660 {lab=VDD}
C {vsource.sym} 1180 -1430 0 0 {name=VSG value=0 savecurrent=false}
C {vsource.sym} 1380 -1310 0 0 {name=VSD value=0.9 savecurrent=true}
C {gnd.sym} 1180 -1270 0 0 {name=l1 lab=0}
C {lab_pin.sym} 1250 -1460 0 0 {name=p2 sig_type=std_logic lab=vsg}
C {code_shown.sym} 290 -1870 0 0 {name=s1 only_toplevel=true place=header 
value=".include /foss/designs/project_carac_sky130A/models/reduced/sky130_tt.red

.param WDEV=10
.param LDEV=0.5
.param VSD_BIAS=0.9

"}
C {code_shown.sym} 290 -1710 0 0 {name=s2 only_toplevel=true place=end 
value=".control
save v(VSG) 
save v(VSD) 
save i(VSD)

save @m.xm1.msky130_fd_pr__pfet_01v8[gm]
save @m.xm1.msky130_fd_pr__pfet_01v8[gds]
save @m.xm1.msky130_fd_pr__pfet_01v8[vth]
save @m.xm1.msky130_fd_pr__pfet_01v8[vdsat]

dc VSG 1.8 0 -0.005 

let id_abs 		= abs(i(VSD))
let gm_abs 		= abs(@m.xm1.msky130_fd_pr__pfet_01v8[gm])
let gds_abs 		= abs(@m.xm1.msky130_fd_pr__pfet_01v8[gds])
let vth_abs 		= abs(@m.xm1.msky130_fd_pr__pfet_01v8[vth])
let vdsat_abs 		= abs(@m.xm1.msky130_fd_pr__pfet_01v8[vdsat])
let vsg 		= 1.8 - v(VSG)

let ro		= 1/gds_abs
let gm_id 	= gm_abs/id_abs
let gm_gds 	= gm_abs/gds_abs

set wr_singlescale
set wr_vecnames

wrdata tb_pfet_01v8_dc.dat vsg id_abs gm_abs gds_abs ro gm_id gm_gds vth_abs vdsat_abs

* ============================================================
* C) Channel-length sweep
* Fixed W = 10um
* ============================================================

echo v_sweep L_um ID_A gm_S gds_S gm_id_Vinv gm_gds VTH_V VDSAT_V > tb_pfet_01v8_length.dat

set wr_singlescale
unset wr_vecnames

foreach l_val 0.18 0.25 0.5 1 2 4 8 10

    alterparam LDEV = $l_val
    reset

    save i(VSD)
    save @m.xm1.msky130_fd_pr__pfet_01v8[gm]
    save @m.xm1.msky130_fd_pr__pfet_01v8[gds]
    save @m.xm1.msky130_fd_pr__pfet_01v8[vth]
    save @m.xm1.msky130_fd_pr__pfet_01v8[vdsat]

    dc VSG 1.8 0 -0.005

    let id_abs    = abs(i(VSD))
    let gm_abs    = abs(@m.xm1.msky130_fd_pr__pfet_01v8[gm])
    let gds_abs   = abs(@m.xm1.msky130_fd_pr__pfet_01v8[gds])
    let vth_abs   = abs(@m.xm1.msky130_fd_pr__pfet_01v8[vth])
    let vdsat_abs = abs(@m.xm1.msky130_fd_pr__pfet_01v8[vdsat])

    let gm_id  = gm_abs/id_abs
    let gm_gds = gm_abs/gds_abs

    let l_um = id_abs*0 + $l_val

    set appendwrite
    wrdata tb_pfet_01v8_length.dat l_um id_abs gm_abs gds_abs gm_id gm_gds vth_abs vdsat_abs

end

unset appendwrite

alterparam LDEV = 0.5
reset

.endc"}
C {sky130_fd_pr/pfet_01v8.sym} 1280 -1460 0 0 {name=M1
W=WDEV
L=LDEV
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {vsource.sym} 1120 -1560 0 0 {name=VDD value=1.8 savecurrent=false}
C {lab_wire.sym} 1240 -1660 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 1350 -1340 0 0 {name=p3 sig_type=std_logic lab=VSD}
