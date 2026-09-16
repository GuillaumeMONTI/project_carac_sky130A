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
N 1180 -1390 1260 -1390 {lab=vgs}
N 1300 -1520 1300 -1420 {lab=vds}
N 1300 -1520 1380 -1520 {lab=vds}
N 1380 -1520 1380 -1500 {lab=vds}
N 1180 -1330 1180 -1280 {lab=0}
N 1180 -1270 1380 -1270 {lab=0}
N 1180 -1280 1180 -1270 {lab=0}
N 1380 -1440 1380 -1270 {lab=0}
N 1300 -1360 1300 -1270 {lab=0}
N 1300 -1390 1310 -1390 {lab=0}
N 1310 -1390 1310 -1270 {lab=0}
C {sky130_fd_pr/nfet_01v8.sym} 1280 -1390 0 0 {name=M1
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
model=nfet_01v8
spiceprefix=X
}
C {vsource.sym} 1180 -1360 0 0 {name=VGS value=0 savecurrent=false}
C {vsource.sym} 1380 -1470 0 0 {name=VDS value=0 savecurrent=false}
C {gnd.sym} 1180 -1270 0 0 {name=l1 lab=0}
C {lab_pin.sym} 1300 -1520 0 0 {name=p1 sig_type=std_logic lab=vds}
C {lab_pin.sym} 1250 -1390 0 0 {name=p2 sig_type=std_logic lab=vgs}
C {code_shown.sym} 520 -1870 0 0 {name=s1 only_toplevel=true place=header 
value=".include /foss/designs/project_carac_sky130A/models/reduced/sky130_tt.red

.param WDEV=10
.param LDEV=0.5
"}
C {code_shown.sym} 520 -1710 0 0 {name=s2 only_toplevel=true place=end 
value=".control

save v(vds)
save v(vgs)
save i(VDS)

dc VDS 0 1.8 0.005 VGS 0.6 1.8 0.2

let id = -i(VDS)

set wr_singlescale
set wr_vecnames

wrdata tb_nfet_01v8_id_vds.dat v(vds) v(vgs) id

.endc"}
