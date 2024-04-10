from time import sleep
import regex as re
import sys, psutil, pymem, subprocess
import numpy as np
from pdmemedit import Pdmemory
from a_pandas_ex_sequence_search import pd_add_find_sequence
import pandas as pd
import ctypes
from cythonsequencefinder import find_seq

bravebro = subprocess.Popen(
    [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "https://www.bet365.com/#/IP/B1",
    ]
)
ctypes.pythonapi.PyMemoryView_FromMemory.argtypes = (
    ctypes.c_char_p,
    ctypes.c_ssize_t,
    ctypes.c_int,
)
ctypes.pythonapi.PyMemoryView_FromMemory.restype = ctypes.py_object
pd_add_find_sequence()
allmapped = []
sleep(5)
allpids = []
allprocs = []

for q in psutil.process_iter():
    try:
        if q.name() == "brave.exe":
            allprocs.append(q)
    except Exception:
        pass
resi = []
allmems = []
memmi = []
np8stuff = np.array([79, 0, 68, 0, 61], dtype=np.uint8)
for q in allprocs:
    print("---------------------")
    allmems.append(Pdmemory(pid=q.pid, filename=None))
hlist = []
allresults = []
try:
    while True:
        allresults.append([])
        hlist.clear()
        memmi.clear()
        for la in allmems:
            try:
                la.update_region_df(
                    limitfunction=lambda x: True,
                    dtypes=(
                        "S1",
                        np.uint8,
                    ),
                    allowed_protections=(
                        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
                    ),
                )

                indigood = la.regiondf.loc[
                    (la.regiondf.aa_type == "MEM_PRIVATE")
                    & (la.regiondf.aa_state == "MEM_COMMIT")
                ].index.__array__()
                indibad = np.setdiff1d(la.regiondf.index.__array__(), indigood)
                la.regiondf.drop(indibad, inplace=True)
                la.regiondf.aa_dump_numpy_uint8 = la.regiondf.aa_dump_numpy_uint8.apply(
                    lambda px: ctypes.pythonapi.PyMemoryView_FromMemory(
                        px.ctypes.data_as(ctypes.c_char_p), px.size, 0x200
                    )
                )
                la.regiondf.aa_dump_numpy_uint8 = la.regiondf.aa_dump_numpy_uint8.apply(
                    lambda x: np.frombuffer(x, dtype=np.uint8)
                )

                memmi.append(
                    la.regiondf.loc[
                        (
                            la.regiondf.aa_dump_numpy_uint8.apply(
                                lambda arax: find_seq(arax, np8stuff, distance=1)
                            ).apply(lambda x: len(x) > 0)
                        )
                    ]
                )
                for h in pd.concat(memmi, ignore_index=True).aa_dump_S1.apply(
                    lambda x: b"".join(x).decode("utf-8", "ignore")
                ):
                    hlist.append(h)

                for h in hlist:
                    for hh in h.split("|"):
                        h2 = hh.strip()
                        if not h2.endswith(";") or not re.search(
                            r"^[A-Z]+", h2.strip()
                        ):
                            continue
                        # allresults[-1].append(hh)
                        print(hh)
                sys.stderr.write("\nEND END END END XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                sys.stderr.flush()
            except Exception as e:
                sys.stderr.write(str(e) + "\n")
                sys.stderr.flush()
except KeyboardInterrupt:
    try:
        sleep(1)
    except:
        pass
print(memmi)
