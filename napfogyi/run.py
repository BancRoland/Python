from input import fizetesek
import numpy as np



resztvevok = ["Roland", "Balint", "Dominik", "Eniko"]

def print_head():
    for i in range(4):
        print(f"\t{resztvevok[i]}nek",end="")
    print()

def print_matrix(mtrx):
    print_head()
    for i in range(4):
        print(f"{resztvevok[i]}",end="\t")
        for j in range(4):
            print(f"{mtrx[i,j]:8.0f}",end="\t")
        print()


given=0
rec = 0
tartozom_balintnak = 0
tartozom_dominiknak = 0
tartozom_encinek = 0

adtam_balintnak = 0
adtam_dominiknak = 0
adtam_encinek = 0

tartozási_mátrix = np.zeros([4,4])
print(tartozási_mátrix)


for tetel in fizetesek:
    tartozás = tetel["osszeg"]/len(tetel["resztvevok"])
    neki_tartozik_idx = resztvevok.index(tetel["fizeto"])

    for resztvevo in tetel["resztvevok"]:
        tartozó_idx = resztvevok.index(resztvevo)
        tartozási_mátrix[tartozó_idx,neki_tartozik_idx] += tartozás



print_matrix(tartozási_mátrix)

def clear_mtrx(tartozasi_matrix):
    for i in range(4):
        for j in range(4):
            tartozasi_matrix[j,i]-=tartozasi_matrix[i,j]
            tartozasi_matrix[i,j] = 0

    tartozasi_matrix = tartozasi_matrix - np.transpose(tartozasi_matrix)
    return tartozasi_matrix

print()
clean = clear_mtrx(tartozási_mátrix)



print_matrix(clean)