import os

def limpeza():
    remove_files = ['Found.txt', 'KFound.txt', 'startcollider.bat', 'in.txt']
    removed_files = []
    for file in remove_files:
        if os.path.exists(file):
            removed_files.append(file)
            os.remove(file)
    if removed_files:
        print(f'Efetuado Limpeza dos arquivos: {", ".join(removed_files)}')

def interrompido(signum, frame):
    limpeza()
    exit(0)