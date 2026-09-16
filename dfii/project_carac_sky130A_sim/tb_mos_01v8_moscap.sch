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
N 1180 -1390 1260 -1390 {lab=vg_n}
N 1260 -1390 1300 -1390 {lab=vg_n}
N 1300 -1390 1300 -1360 {lab=vg_n}
N 1330 -1320 1330 -1280 {lab=0}
N 1270 -1320 1270 -1280 {lab=0}
N 1300 -1320 1300 -1280 {lab=0}
N 1300 -1280 1330 -1280 {lab=0}
N 1270 -1280 1300 -1280 {lab=0}
N 1180 -1340 1180 -1330 {lab=vg_n}
N 1180 -1390 1180 -1340 {lab=vg_n}
N 1570 -1420 1570 -1390 {lab=vg_p}
N 1600 -1500 1600 -1460 {lab=#net1}
N 1540 -1500 1540 -1460 {lab=#net1}
N 1570 -1500 1570 -1460 {lab=#net1}
N 1570 -1500 1600 -1500 {lab=#net1}
N 1540 -1500 1570 -1500 {lab=#net1}
N 1460 -1340 1460 -1330 {lab=vg_p}
N 1460 -1390 1460 -1340 {lab=vg_p}
N 1560 -1390 1570 -1390 {lab=vg_p}
N 1550 -1390 1560 -1390 {lab=vg_p}
N 1540 -1390 1550 -1390 {lab=vg_p}
N 1530 -1390 1540 -1390 {lab=vg_p}
N 1520 -1390 1530 -1390 {lab=vg_p}
N 1510 -1390 1520 -1390 {lab=vg_p}
N 1500 -1390 1510 -1390 {lab=vg_p}
N 1490 -1390 1500 -1390 {lab=vg_p}
N 1480 -1390 1490 -1390 {lab=vg_p}
N 1470 -1390 1480 -1390 {lab=vg_p}
N 1460 -1390 1470 -1390 {lab=vg_p}
N 1680 -1530 1680 -1510 {lab=#net1}
N 1570 -1530 1680 -1530 {lab=#net1}
N 1570 -1530 1570 -1500 {lab=#net1}
C {sky130_fd_pr/nfet_01v8.sym} 1300 -1340 1 0 {name=M1
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
C {vsource.sym} 1180 -1310 0 0 {name=VACN value="0 AC 1" savecurrent=false}
C {lab_pin.sym} 1250 -1390 0 0 {name=p2 sig_type=std_logic lab=vg_n}
C {code_shown.sym} 380 -1920 0 0 {name=s1 only_toplevel=true place=header 
value=".include /foss/designs/project_carac_sky130A/models/reduced/sky130_tt.red

.param WDEV=10
.param LDEV=0.5

.param VDD_CAP=1.8

.param VGN_BIAS=1.8
.param VGP_BIAS=0
"}
C {code_shown.sym} 380 -1710 0 0 {name=s2 only_toplevel=true place=end 
value=".control

* ============================================================
* A) Cg versus gate potential
* Reference geometry: W=10um, L=0.5um
* D=S=B=0
* ============================================================

* ============================================================
* A) Cg versus capacitor voltage
* Reference geometry: W=10um, L=0.5um
* ============================================================

setplot const

let k = 0
let npts = 36
let vcap_step = 0.05

echo Vcap_V Cg_N_F Cg_P_F > tb_mos_01v8_moscap_cv.dat

while k le npts

    let vcap_val = k * vcap_step
    let vgp_val  = 1.8 - vcap_val

    alter VDCN $&vcap_val
    alter VDCP $&vgp_val

    ac lin 1 1Meg 1Meg

    let cgn_now = abs(imag(i(VACN))) / (2*pi*frequency)
    let cgp_now = abs(imag(i(VACP))) / (2*pi*frequency)

    echo $&vcap_val $&cgn_now $&cgp_now >> tb_mos_01v8_moscap_cv.dat

    setplot const
    let k = k + 1

end


* ============================================================
* B) Cg versus geometry
* Fixed capacitor bias: VGB = 1.8V
* ============================================================

* ============================================================
* B) Cg versus geometry
* Fixed |VGB| = 1.8V
* ============================================================

setplot const

let w_val   = 1
let w_stop  = 20
let w_step  = 1

let l_start = 0.5
let l_stop  = 10
let l_step  = 0.5

echo W_um L_um Cg_N_F Cg_Ndens_fF_um2 Cg_P_F Cg_Pdens_fF_um2 > tb_mos_01v8_moscap_geometry.dat

while w_val le w_stop

    let l_val = l_start

    while l_val le l_stop

        alterparam WDEV = $&w_val
        alterparam LDEV = $&l_val

        reset

        ac lin 1 1Meg 1Meg

        let cgn_now = abs(imag(i(VACN))) / (2*pi*frequency)
        let cgp_now = abs(imag(i(VACP))) / (2*pi*frequency)

        let cgn_density = cgn_now*1e15 / ($&w_val*$&l_val)
        let cgp_density = cgp_now*1e15 / ($&w_val*$&l_val)

        echo $&w_val $&l_val $&cgn_now $&cgn_density $&cgp_now $&cgp_density >> tb_mos_01v8_moscap_geometry.dat

        setplot const
        let l_val = l_val + l_step

    end

    let w_val = w_val + w_step

end

.endc"}
C {gnd.sym} 1300 -1280 0 0 {name=l2 lab=0}
C {gnd.sym} 1180 -1220 0 0 {name=l3 lab=0}
C {vsource.sym} 1180 -1250 0 0 {name=VDCN value=\{VGN_BIAS\} savecurrent=false}
C {vsource.sym} 1460 -1310 0 0 {name=VACP value="0 AC 1" savecurrent=false}
C {lab_pin.sym} 1530 -1390 0 0 {name=p1 sig_type=std_logic lab=vg_p}
C {gnd.sym} 1460 -1220 0 0 {name=l4 lab=0}
C {vsource.sym} 1460 -1250 0 0 {name=VDCP value=\{VGP_BIAS\} savecurrent=false}
C {sky130_fd_pr/pfet_01v8.sym} 1570 -1440 3 0 {name=M2
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
C {vsource.sym} 1680 -1480 0 0 {name=VDDCAP value=1.8 savecurrent=false}
C {gnd.sym} 1680 -1450 0 0 {name=l1 lab=0}
