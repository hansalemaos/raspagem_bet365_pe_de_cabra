from time import sleep
import psutil
import pymem
import numpy as np
from pdmemedit import Pdmemory
from cythonsequencefinder import np_search_sequence
from seleniumbase import Driver
from exceptdrucker import errwrite
import ujson

driver = Driver(uc=True)
driver.get("https://br.betano.com")
sleep(15)
allprocs = []

for q in psutil.process_iter():
    try:
        if q.name().lower() == "chrome.exe":
            allprocs.append(q)
    except Exception:
        pass
allmems = []
for q in allprocs:
    allmems.append(Pdmemory(pid=q.pid, filename=None))


def search_memory(
    string,
    encoding="utf-8",  # utf-8 / utf-16-le / latin1 / cp1252
    outencodingreplace="ignore",
):
    seqarra = np.array(list(string.encode(encoding)), dtype=np.uint8)
    resultsfound = []
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
            for numara in range(len(la.regiondf.aa_dump_numpy_uint8)):
                try:
                    if np.any(
                        np_search_sequence(
                            la.regiondf.aa_dump_numpy_uint8.iloc[numara],
                            seqarra,
                            distance=1,
                        )
                    ):
                        resultsfound.append(
                            (la.regiondf.aa_dump_S1.iloc[numara]).copy()
                        )
                except Exception:
                    errwrite()
        except Exception:
            errwrite()
    return resultsfound


resxa = search_memory(
    string="displayOrder",
    encoding="utf-8",
    outencodingreplace="ignore",
)


# 6[{"sports":1
for a in resxa:
    # if a.size < 1000000:
    print("--------------------------------------------------------")
    try:
        stri = (b"".join(a)).split(b'[{"sports":', maxsplit=1)[1]
        stri = stri.rsplit(b"]", maxsplit=1)[0]
        stri = b'[{"sports":' + stri + b"]"
        print(ujson.loads(stri))
    except Exception:
        errwrite()
