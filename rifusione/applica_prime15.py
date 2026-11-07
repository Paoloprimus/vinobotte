# Sovrascrive in dati/ le schede arricchite delle prime cantine in ordine alfabetico (fonti numerate, vini, presenza online).
import json, glob, os, shutil
QUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = 0
for f in sorted(glob.glob(os.path.join(QUI, 'arricchimenti', 'prime15', '*.json'))):
    dest = os.path.join(QUI, 'dati', os.path.basename(f))
    if os.path.exists(dest):
        shutil.copyfile(f, dest); n += 1
print('prime15:', n, 'schede')
