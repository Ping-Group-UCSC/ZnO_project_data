#!/usr/bin/env python3
import numpy as np
import os
import re

cwd = os.getcwd()
f = open(os.path.join(cwd, "casscf.out"), "r")
lines = f.readlines()

num_lines = len(lines)

def get_soc(line):
    cm2GHz = 29979245.8e-6
    re_soc = float(line.split()[8])
    im_soc = float(line.split()[9])
    soc = np.sqrt(re_soc**2 + im_soc**2)
    soc *= cm2GHz
    return soc

# |Block Root  S >
triplet_3A2="0     0  1.0 " #triplet gs
other3E_r1="0     1  1.0 "#triplet 3E 1a1->e, root1
other3E_r2="0     2  1.0 "#triplet 3E 1a1->e, root2
triplet_3E_r1="0     3  1.0 " #triplet 3E e->2a1, root1
triplet_3E_r2="0     4  1.0 " #triplet 3E e->2a1, root2

singlet_1E_r1="1    0  0.0 " #singlet 1E root1
singlet_1E_r2="1    1  0.0 " #singlet 1E root2
singlet_1A1="1    2  0.0 " # singlet 1A1

for i, line in enumerate(lines):
# Block 0 for triplet, Block 1 for singlet
# Root starts from 0 (ground state)
#              Bra                       Ket
#   <Block Root  S    Ms  | HSOC |  Block Root  S    Ms>
    #1E->3A2
    if f"{singlet_1E_r1} 0.0              {triplet_3A2} 0.0" in line:
        soc = get_soc(line)
        print("root1 1E(ms=0) -> 3A2(ms=0), lambda z= ",np.round(soc,3), "GHz")
    if f"{singlet_1E_r1} 0.0              {triplet_3A2} 1.0" in line:
        soc = get_soc(line)
        print("root1 1E(ms=0) -> 3A2(ms=0), lambda x= ",np.round(soc,3), "GHz")
    if f"{singlet_1E_r1} 0.0              {triplet_3A2}-1.0" in line:
        soc = get_soc(line)
        print("root1 1E(ms=0) -> 3A2(ms=0), lambda y= ",np.round(soc,3), "GHz")

    if f"{singlet_1E_r2} 0.0              {triplet_3A2} 0.0" in line:
        soc = get_soc(line)
        print("root2 1E(ms=0) -> 3A2(ms=0), lambda z= ",np.round(soc,3), "GHz")
    if f"{singlet_1E_r2} 0.0              {triplet_3A2} 1.0" in line:
        soc = get_soc(line)
        print("root2 1E(ms=0) -> 3A2(ms=0), lambda x= ",np.round(soc,3), "GHz")
    if f"{singlet_1E_r2} 0.0              {triplet_3A2}-1.0" in line:
        soc = get_soc(line)
        print("root2 1E(ms=0) -> 3A2(ms=0), lambda y= ",np.round(soc,3), "GHz")  

    #3E->1A1:
    if f"{singlet_1A1} 0.0              {triplet_3E_r1} 0.0" in line:
        soc = get_soc(line)
        print("(e->2a1)root1 3E(ms=0) -> 1A1(ms=0), lambda z= ",np.round(soc,3), "GHz")
    if f"{singlet_1A1} 0.0              {triplet_3E_r1} 1.0" in line:
        soc = get_soc(line)
        print("(e->2a1)root1 3E(ms=1) -> 1A1(ms=0), lambda x= ",np.round(soc,3), "GHz")
    if f"{singlet_1A1} 0.0              {triplet_3E_r1}-1.0" in line:
        soc = get_soc(line)
        print("(e->2a1)root1 3E(ms=-1) -> 1A1(ms=0), lambda y= ",np.round(soc,3), "GHz")
    
    if f"{singlet_1A1} 0.0              {triplet_3E_r2} 0.0" in line:
        soc = get_soc(line)
        print("(e->2a1)root2 3E(ms=0) -> 1A1(ms=0), lambda z= ",np.round(soc,3), "GHz")
    if f"{singlet_1A1} 0.0              {triplet_3E_r2} 1.0" in line:
        soc = get_soc(line)
        print("(e->2a1)root2 3E(ms=1) -> 1A1(ms=0), lambda x= ",np.round(soc,3), "GHz")
    if f"{singlet_1A1} 0.0              {triplet_3E_r2}-1.0" in line:
        soc = get_soc(line)
        print("(e->2a1)root2 3E(ms=-1) -> 1A1(ms=0), lambda y= ",np.round(soc,3), "GHz")

    #3E(related to a1e,not prefered) ->1A1:
    if f"{singlet_1A1} 0.0              {other3E_r1} 0.0" in line:
        soc = get_soc(line)
        print("(1a1->e)root1 3E(ms=0) -> 1A1(ms=0), lambda z= ",np.round(soc,3), "GHz")
    if f"{singlet_1A1} 0.0              {other3E_r1} 1.0" in line:
        soc = get_soc(line)
        print("(1a1->e)root1 3E(ms=1) -> 1A1(ms=0), lambda x= ",np.round(soc,3), "GHz")
    if f"{singlet_1A1} 0.0              {other3E_r1}-1.0" in line:
        soc = get_soc(line)
        print("(1a1->e)root1 3E(ms=-1) -> 1A1(ms=0), lambda y= ",np.round(soc,3), "GHz")

    if f"{singlet_1A1} 0.0              {other3E_r2} 0.0" in line:
        soc = get_soc(line)
        print("(1a1->e)root2 3E(ms=0) -> 1A1(ms=0), lambda z= ",np.round(soc,3), "GHz")
    if f"{singlet_1A1} 0.0              {other3E_r2} 1.0" in line:
        soc = get_soc(line)
        print("(1a1->e)root2 3E(ms=1) -> 1A1(ms=0), lambda x= ",np.round(soc,3), "GHz")
    if f"{singlet_1A1} 0.0              {other3E_r2}-1.0" in line:
        soc = get_soc(line)
        print("(1a1->e)root2 3E(ms=-1) -> 1A1(ms=0), lambda y= ",np.round(soc,3), "GHz")

