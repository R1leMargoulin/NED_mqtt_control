

barycenters = [(1,2),(2,2), (2,1),(3,1),(4,1),(3,2),(4,2),(1,1)]

sorted_by_y = sorted(barycenters, key=lambda tup: tup[1])

line1 = sorted_by_y[0:int(len(sorted_by_y)/2)]
line2 = sorted_by_y[int(len(sorted_by_y)/2): len(sorted_by_y)]

    

matrix = [line1, line2]

#on tri les lignes de notre matrice en fonction de l'axe x cette fois
for l in range(len(matrix)):
    matrix[l] = sorted(matrix[l], key=lambda tup: tup[0])

print(matrix)