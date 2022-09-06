from type_chart import pokemon_types, damage_array
import numpy as np

prob1 = np.array([2.20222269e-314, 8.98181670e-002, 1.64015783e-001, 9.06724159e-002,
 9.82386202e-002, 5.82109588e-002, 2.54714696e-314, 4.40548346e-002,
 8.65232071e-002, 4.69836879e-002, 2.54715463e-314, 2.54715465e-314,
 2.54715468e-314, 6.17499898e-002, 1.03974291e-001, 1.46849449e-002,
 7.93231095e-002, 6.17499898e-002])

prob2 = np.array([0.,        0.08981817,0.16401578,0.09067242,0.09823862,0.05821096,
 0.       ,  0.04405483, 0.08652321 ,0.04698369 ,0.  ,       0.,
 0.       ,  0.06174999, 0.10397429 ,0.01468494 ,0.07932311, 0.06174999])

prob3 = np.array([0.,        0.,        0.16057294,0.08254806,0.07010931,0.,
 0.0011308, 0.,        0.12664908,0.06784772,0.,         0.,
 0.      ,  0.03957784,0.17527328,0.00150773,0.23633622,0.03844704])

prob = (prob2 + prob3) / 2
print(prob)
size = len(prob)

for i in range(size):
    print("Type ", pokemon_types[i], " prob %0.2f" % (prob[i] * 100))
    print("  attack : ", np.dot(prob,  damage_array[i]))
    print("  defense: ", 1 / np.dot(prob,  damage_array[:, i]))

# Calculate best double types for defense

for i in range(size):
    for j in range(i+1, size):
        rating = 1 / np.dot(prob, damage_array[i] * damage_array[j])
        if rating > 1.1:
            print("Type %s / %s: rating %0.3f" % (pokemon_types[i], pokemon_types[j], rating))

