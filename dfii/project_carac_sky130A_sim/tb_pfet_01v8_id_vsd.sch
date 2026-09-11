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
N 1180 -1460 1260 -1460 {lab=VG}
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
C {vsource.sym} 1180 -1430 0 0 {name=VG value=0 savecurrent=false}
C {vsource.sym} 1380 -1310 0 0 {name=VD value=0.9 savecurrent=true}
C {gnd.sym} 1180 -1270 0 0 {name=l1 lab=0}
C {lab_pin.sym} 1250 -1460 0 0 {name=p2 sig_type=std_logic lab=VG}
C {code_shown.sym} 290 -1870 0 0 {name=s1 only_toplevel=true place=header 
value=".include /foss/designs/project_carac_sky130A/models/reduced/sky130_tt.red

.param WDEV=10
.param LDEV=0.5
.param VSD_BIAS=0.9

"}
C {code_shown.sym} 290 -1710 0 0 {name=s2 only_toplevel=true place=end 
value=".control
save v(VD) 
save v(VG) 
save i(VD)

dc VD 1.8 0 -0.005 VG 1.2 0 -0.2

let id_abs 		= abs(i(VD))
let vsd 		= 1.8 - v(VD)
let vsg 		= 1.8 - v(VG)

write tb_pfet_01v8_id_vsd.raw vsd vsg id_abs

.endc"}
C {sky130_fd_pr/pfet_01v8.sym} 1280 -1460 0 0 {name=M1
W=1
L=0.15
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
C {lab_wire.sym} 1350 -1340 0 0 {name=p3 sig_type=std_logic lab=VD}
