#!/usr/bin/env python
import os
import glob
import re
import xml.etree.ElementTree as ET
import numpy as np
from io_package import read_cell_and_pos_auto

# Ha2eV = 27.2113834
# Ry2eV = Ha2eV / 2


def read_pos_and_etot_ratio(folder=None):
    '''
    Read ratio-***/scf.out from given directory

    Return a list of ratio/atoms/etot, and vecR (which should be the same for all structures)
    '''
    if (folder is None):
        folder = os.getcwd()

    # check for folders/files
    if not glob.glob('%s/ratio-*' % folder):
        raise FileNotFoundError("folders %s/ratio-* do not exist" % folder)
    elif not glob.glob("%s/ratio-*/OUTCAR" % folder):
        raise FileNotFoundError("files %s/ratio-*/OUTCAR do not exist" % folder)
    elif not glob.glob("%s/ratio-*/CONTCAR" % folder):
        if not glob.glob("%s/ratio-*/POSCAR" % folder):
            raise FileNotFoundError("files %s/ratio-*/CONTCAR and /ratio-*/POSCAR do not exist" % folder)

    # elif not glob.glob("%s/ratio-*/scf.out" % folder):
    #     raise FileNotFoundError("files %s/ratio-*/scf.out do not exist" % folder)

    list_data = []
    for filename in glob.glob("%s/ratio-*/OUTCAR" % folder):
        ratio = float(re.match(".*ratio-(.+)/OUTCAR", filename).group(1))
        
        # Read structure
        if (os.path.exists(filename.replace("OUTCAR", "CONTCAR"))):
            (vecR, list_pos), prog = read_cell_and_pos_auto(filename.replace("OUTCAR", "CONTCAR"))
        elif (os.path.exists(filename.replace("OUTCAR", "POSCAR"))):
            (vecR, list_pos), prog = read_cell_and_pos_auto(filename.replace("OUTCAR", "POSCAR"))
    
        # Remove numbers in species and convert to cartesian
        for atom in list_pos:
            atom["species"] = filter(lambda x: x.isalpha(), atom["species"])
            atom["posxyz"] = np.dot(vecR, atom["pos"])

        # Read energy
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines[::-1]:
                if "free  energy   TOTEN" in line:
                    # Extract the Energy:
                    match0 = re.search(r"[-+]?\d*\.?\d+", line)
                    if match0:
                        etot = float(match0.group()) # etot in eV

        list_data.append({"ratio": ratio, "pos": list_pos, "etot": etot})

    list_data.sort(key=lambda x: x["ratio"])
    return list_data, vecR


def read_eig(folder):
    '''
    Read eigenvalues from save folder

    :return: Array in ik, ispin, ib, 1/2 (for eigenvalues and occupations numbers)
    '''
    t1 = ET.parse(os.path.join(folder, "vasprun.xml")).getroot()
    nk_root = t1.find("kpoints//varray[@name='kpointlist']")
    kpoints = []
    for v in nk_root.findall("v"):
        kpoints.append([float(x) for x in v.text.split()])
    nk = len(kpoints)

    spin_root = t1.find("parameters//separator[@name='electronic spin']/i[@name='ISPIN']")
    list_spin = [1, 2] if int(spin_root.text.strip()) == 2 else [""]

    nbands_element = t1.find("parameters//separator[@name='electronic']/i[@name='NBANDS']")
    nbands = int(nbands_element.text.strip())
    
    ar = None
    for ik in range(1, nk+1):
        for ispin, stspin in enumerate(list_spin):
            eigenvals_root = t1.find("calculation/eigenvalues/array/set/set[@comment='spin %s']/set[@comment='kpoint %i']" % (stspin, ik)) #/set[@comment='kpoint %i'])
            data = []
            occ = []
            for pair in eigenvals_root.findall("r"):
                data.append(float(pair.text.split()[0]))
                occ.append(float(pair.text.split()[1]))
            data = np.asarray(data)
            occ = np.asarray(occ)

            if (ar is None):
                ar = np.zeros((nk, len(list_spin), nbands, 2), dtype=np.float64)
            ar[ik-1, ispin, :, 0] = data
            ar[ik-1, ispin, :, 1] = occ

    return ar

# This is the new calc_wif function for VASP inputs
def calc_wif(dir_i, dir_f, ix_defect, ix_bandmin, ix_bandmax, dQ, de=None, spinname="down"):

    if (ix_bandmin > ix_bandmax):
        raise ValueError("Band max must be equal or larger than band min")

    [list_data1, vecR], prog = read_pos_and_etot_ratio(dir_i)
    [list_data2, vecR], prog = read_pos_and_etot_ratio(dir_f)

    dE = de
    dic_band_overlap = dict((ix, []) for ix in range(ix_bandmin, ix_bandmax+1))

    # Collect all eigenvalues
    ix_plotmin = min(ix_bandmin, ix_defect) - 1
    ix_plotmax = max(ix_bandmax, ix_defect) + 1

    # Two state and two spin seperately
    dic_eig_all = {("i", 1): [],
                   ("i", 2): [],
                   ("f", 1): [],
                   ("f", 2): []
                   }

    # Read all eigenvalues
    for statename, list_data, dir0 in [
            ("i", list_data1, dir_i),
            ("f", list_data2, dir_f),
    ]:
        for data in list_data:
            ratio = data["ratio"]
            if prog == "qe":
                folder = get_save_folder(os.path.join(dir0, get_ratio_folder(ratio)))
            elif prog == "vasp":
                folder = os.path.join(dir0, get_ratio_folder(ratio))
            if folder is None:
                print("Unable to read from ratio folder!!! printing error information")
                print(f"ratio = {ratio}")
                print(f"dir0 = {dir0}")
                print(f"ratio_folder = {get_ratio_folder(ratio)}")
                raise ValueError("Unable to get ratio folder")
            ar_eig1 = read_eig(folder)

            for spin in (1, 2):
                dic_eig_all[(statename, spin)].append(
                    [ratio, ar_eig1[0, spin-1, ix_plotmin - 1:ix_plotmax, 0],
                        ar_eig1[0, spin-1, ix_plotmin-1:ix_plotmax, 1]]
                )


'''
bulkband_index: [428,431]
defectband_index: 432
folder_final_state: ../lin-gs/
folder_init_state: ../lin-es/
ratio_final: 0.0
ratio_init: 1.0

calc_wif(
        dinput['folder_init_state'], dinput['folder_final_state'], dinput['defectband_index'],
        dinput['bulkband_index'][0],
        dinput['bulkband_index'][1],
        data['dQ'],
        de=None,
        spinname=dinput['defectband_spin'])
'''

# wavecars: [(dQ, path_to/cc_files/lin1/WAVECAR)] -> [(-0.00955884671398863, 'cc_files/lin1/ratio--0.0080/WAVECAR'), (0.0, 'cc_files/lin1/ratio-0.0000/WAVECAR'),
# init_wavecar_p
Wifs = get_Wif_from_wavecars(wavecars, str(ground_files / 'WAVECAR'), 864, [860, 861, 862, 863], spin=0, fig=fig)

def get_Wif_from_wavecars(wavecars: list, init_wavecar_path: str, def_index: int, bulk_index: Union[np.ndarray, Sequence[int]], spin: int = 0, kpoint: int = 1, fig=None) -> list:

    """Compute the electron-phonon matrix element using the WAVECARs.

    This function reads in the pseudo-wavefunctions from the WAVECAR files and
    computes the overlaps necessary.
    ***************

    Parameters
    ----------
    wavecars : list((Q, wavecar_path))
        a list of tuples where the first value is the Q and the second is the
        path to the WAVECAR file
    init_wavecar_path : string
        path to the initial wavecar for computing overlaps
    def_index : int
        index corresponding to the defect wavefunction (1-based indexing)
    bulk_index : int, list(int)
        index or list of indices corresponding to the bulk wavefunction
        (1-based indexing)
    spin : int
        spin channel to read from (0 - up, 1 - down)
    kpoint : int
        kpoint to read from (defaults to the first kpoint)
    fig : matplotlib.figure.Figure
        optional figure object to plot diagnostic information

    Returns
    -------
    list((bulk_index, Wif))
        electron-phonon matrix element Wif in units of
        eV amu^{-1/2} Angstrom^{-1} for each bulk_index
    """
    bulk_index = np.array(bulk_index, ndmin=1)
    initial_wavecar = Wavecar(init_wavecar_path)
    if initial_wavecar.spin == 2:
        psi_i = initial_wavecar.coeffs[spin][kpoint-1][def_index-1]
    else:
        psi_i = initial_wavecar.coeffs[kpoint-1][def_index-1]

    Nw, Nbi = (len(wavecars), len(bulk_index))
    Q, matels, deig = (np.zeros(Nw+1), np.zeros((Nbi, Nw+1)), np.zeros(Nbi))

    # first compute the Q = 0 values and eigenvalue differences
    for i, bi in enumerate(bulk_index):
        if initial_wavecar.spin == 2:
            psi_f = initial_wavecar.coeffs[spin][kpoint-1][bi-1]
            deig[i] = initial_wavecar.band_energy[spin][kpoint-1][bi-1][0] - \
                initial_wavecar.band_energy[spin][kpoint-1][def_index-1][0]
        else:
            psi_f = initial_wavecar.coeffs[kpoint-1][bi-1]
            deig[i] = initial_wavecar.band_energy[kpoint-1][bi-1][0] - \
                initial_wavecar.band_energy[kpoint-1][def_index-1][0]
        matels[i, Nw] = _compute_matel(psi_i, psi_f)
    deig = np.abs(deig)

    # now compute for each Q
    for i, (q, fname) in enumerate(wavecars):
        Q[i] = q
        final_wavecar = Wavecar(fname)
        for j, bi in enumerate(bulk_index):
            if final_wavecar.spin == 2:
                psi_f = final_wavecar.coeffs[spin][kpoint-1][bi-1]
            else:
                psi_f = final_wavecar.coeffs[kpoint-1][bi-1]
            matels[j, i] = _compute_matel(psi_i, psi_f)

    if fig is not None:
        ax = fig.subplots(1, Nbi)
        ax = np.array(ax, ndmin=1)
        for a, i in zip(ax, range(Nbi)):
            a.scatter(Q, matels[i, :])
            a.set_title(f'{bulk_index[i]}')

    return [(bi, deig[i] * np.mean(np.abs(np.gradient(matels[i, :], Q))))
            for i, bi in enumerate(bulk_index)]


def calc_wif(dir_i, dir_f, ix_defect, ix_bandmin, ix_bandmax, dQ, de=None, spinname="down"):
    '''
    Compute Wif from a series of SCF calculations; Check Phys. Rev. B 90, 075202(2014) for definition.
    Each SCF calculation must be in ratio-* folder and contains a *.save folder as result

    :param dir_i: Folder contains ratio-* for initial state (hole in VB), only the ratio=0 will be used
    :param dir_f: Folder contains ratio-* for final state (hole in defect, or the lower energy of two)
    :param defect: Defect band index (1-base)
    :param bandmin: Valence hole band index minimum(1-based)
    :param bandmax: Valence hole band index maximum(1-based)
    :param de: energy difference for two levels; if not specified,
        use energy difference at Q=0 (ratio=0) of the final stat
    :param spin: compute the overlap of wavefunction of given spin channel, can be either "up" or "down".
        For a defect  all filled initial state and a hole in spin down channel final state (PRB 90, 075202),
        the "down" spin should be investigate. For a defect-defect transition the selected defect
        level spin should be used.

    :return: dic_eig : dic(intial/final) = array of [ratio, eigenvalues for different bands],
        array of [ratio, occupations numbers for different bands]
    '''
    if (ix_bandmin > ix_bandmax):
        raise ValueError("Band max must be equal or larger than band min")

    list_data1, vecR = read_pos_and_etot_ratio(dir_i)
    list_data2, vecR = read_pos_and_etot_ratio(dir_f)

    dE = de
    dic_band_overlap = dict((ix, []) for ix in range(ix_bandmin, ix_bandmax+1))

# Collect all eigenvalues
    ix_plotmin = min(ix_bandmin, ix_defect) - 1
    ix_plotmax = max(ix_bandmax, ix_defect) + 1

# Two state and two spin seperately
    dic_eig_all = {("i", 1): [],
                   ("i", 2): [],
                   ("f", 1): [],
                   ("f", 2): []
                   }

# Read all eigenvalues
    for statename, list_data, dir0 in [
            ("i", list_data1, dir_i),
            ("f", list_data2, dir_f),
    ]:
        for data in list_data:
            ratio = data["ratio"]
            folder = get_save_folder(os.path.join(dir0, get_ratio_folder(ratio)))
            if folder is None:
                print("Unable to read from ratio folder!!! printing error information")
                print(f"ratio = {ratio}")
                print(f"dir0 = {dir0}")
                print(f"ratio_folder = {get_ratio_folder(ratio)}")
                raise ValueError("Unable to get ratio folder")
            ar_eig1 = read_eig(folder)

            for spin in (1, 2):
                dic_eig_all[(statename, spin)].append(
                    [ratio, ar_eig1[0, spin-1, ix_plotmin - 1:ix_plotmax, 0],
                        ar_eig1[0, spin-1, ix_plotmin-1:ix_plotmax, 1]]
                )

# Organize data
    dic_eig_occ = {}
    for key, val in dic_eig_all.items():
        dic_eig_occ[key] = {"eig": np.asarray([[x[0]] + x[1].tolist() for x in val]),
                            "occ": np.asarray([[x[0]] + x[2].tolist() for x in val])}

# Compute dE
    # The hole is always spin-down as in QE number of electrons is always more in spin up
    spin = {"up": 1, "down": 2}[spinname]

    folder_q0 = get_save_folder(os.path.join(dir_f, get_ratio_folder(0)))
    ar_eig1_q0 = read_eig(folder_q0)

    '''
    loop through bands and compute overlap
    '''
    dic_band_overlap = {}
    print("%sGathering :  band ratio" % (indent*2))
    for iband in range(ix_bandmin, ix_bandmax+1):
        list_overlap = []
#       print(spin, iband, ix_defect, ar_eig1_q0[0,spin-1,iband-1,0], + ar_eig1_q0[0, spin-1, ix_defect-1,0])
        dE = float(-ar_eig1_q0[0, spin-1, iband-1, 0] + ar_eig1_q0[0, spin-1, ix_defect-1, 0])
# Read wavefunction of a perturbed bulk state in final state
# (This and defect wavefunction should be same Hamiltonian to be meaningful)
        evc1 = read_wave(folder_q0, ispin=spin, ik=1, ib=iband)

        # list_ratio = []
        for data in list_data2:
            ratio = data["ratio"]
            folder2 = get_save_folder(os.path.join(dir_f, get_ratio_folder(ratio)))

            if (folder2 is None):
                print("Skip ratio %.4f as missing .save folder %s" % (ratio, os.path.join(dir_f, "ratio-%.4f" % ratio)))
                continue
            print("%sOverlap: %i  %.4f" % (indent*3, iband, ratio))
            # print("%sCompute overlap for band %i ratio %.4f" % (indent*2, iband, ratio))

# Read wavefunction of a defect state of final state
            evc2 = read_wave(folder2, spin, 1, ix_defect)
# Note : if QE is gamma only (wavefunction is real), the evc contains only positive G
# And evc^2 = 0.5
# If QE is not gamma only then all G are included, evc^2 = 1
# Note G=0 is doubled ; but error very small in general
            s = np.dot(np.conj(evc1), evc2)
            if evc1.dtype == np.float64:
                s *= 2
            list_overlap.append([ratio, abs(s)])

        list_overlap.sort(key=lambda x: x[0])

        dic_band_overlap[iband] = np.asarray(list_overlap)

    list_wif = []
    for iband, ar0 in dic_band_overlap.items():
        # Only fit first several

        # find index with ratio = 0
        index0 = np.argwhere(np.isclose(ar0[:, 0], 0, atol=1e-6)).flatten()
        assert len(index0) == 1, "Should be 1 and only one index with ratio 0"
        index0 = index0[0]

        # convert to Q
        ar_Q = ar0[:, 0] * dQ

        # only use a few begginning where ratio=0
        ar_overlap = ar0[index0:, 1]
        nq = 3
#       print("Fitting %i points: Q=[%.3f, %.3f]" % (nq, ar_Q[0], ar_Q[nq-1]))
        p = np.polyfit(ar_Q[:nq], ar_overlap[:nq],  deg=1)
#       print("Band %i dS/dQ %.2e Wif %.2e" % (iband, p[0], p[0] * dE))
        list_wif.append((iband, float(p[0] * dE)))

# Find the maxium
    list_wif.sort(key=lambda x: x[1])
    ixband_wifmax, wif = list_wif[-1]
    dic_wif = dict(list_wif)

    return dic_eig_occ, dE, dic_band_overlap, dic_wif, ixband_wifmax, wif