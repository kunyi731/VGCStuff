import numpy as np
import pygambit

from type_chart import pokemon_types, damage_array

# A 2 Dimenstional Numpy Array Of Damage Multipliers For Attacking Pokemon:
D = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 0, 8, 8, 4, 8],
             [8, 4, 4, 8, 16, 16, 8, 8, 8, 8, 8, 16, 4, 8, 4, 8, 16, 8],
             [8, 16, 4, 8, 4, 8, 8, 8, 16, 8, 8, 8, 16, 8, 4, 8, 8, 8],
             [8, 8, 16, 4, 4, 8, 8, 8, 0, 16, 8, 8, 8, 8, 4, 8, 8, 8],
             [8, 4, 16, 8, 4, 8, 8, 4, 16, 4, 8, 4, 16, 8, 4, 8, 4, 8],
             [8, 4, 4, 8, 16, 4, 8, 8, 16, 16, 8, 8, 8, 8, 16, 8, 4, 8],
             [16, 8, 8, 8, 8, 16, 8, 4, 8, 4, 4, 4, 16, 0, 8, 16, 16, 4],
             [8, 8, 8, 8, 16, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 0, 16],
             [8, 16, 8, 16, 4, 8, 8, 16, 8, 0, 8, 4, 16, 8, 8, 8, 16, 8],
             [8, 8, 8, 4, 16, 8, 16, 8, 8, 8, 8, 16, 4, 8, 8, 8, 4, 8],
             [8, 8, 8, 8, 8, 8, 16, 16, 8, 8, 4, 8, 8, 8, 8, 0, 4, 8],
             [8, 4, 8, 8, 16, 8, 4, 4, 8, 4, 16, 8, 8, 4, 8, 16, 4, 4],
             [8, 16, 8, 8, 8, 16, 4, 8, 4, 16, 8, 16, 8, 8, 8, 8, 4, 8],
             [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 16, 8, 8, 16, 8, 4, 8, 8],
             [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 16, 8, 4, 0],
             [8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 16, 8, 8, 16, 8, 4, 8, 4],
             [8, 4, 4, 4, 8, 16, 8, 8, 8, 8, 8, 8, 16, 8, 8, 8, 4, 16],
             [8, 4, 8, 8, 8, 8, 16, 4, 8, 8, 8, 8, 8, 8, 16, 16, 4, 8]], dtype=pygambit.Rational)

#D = np.array([[8, 8, 4],
#              [4, 8, 16],
#              [8, 4, 4]], dtype=pygambit.Rational)

A = D

# 2-D array of including STAB.
# Row or col [18x + y] means "attack with type x and defend with type y"
size = len(A)
A = np.empty((size*size, size), dtype=pygambit.Rational)
game_size = len(A[0])

# Calculate the block with attack type x
stab = pygambit.Rational(150, 100)
for x in range(size):
    col_at = np.identity(size)
    col_at[x][x] = stab
    A[(size*x):(size*(x+1))] = np.matmul(col_at, D)

# Convert to Rational type
for i in range(len(A)):
    for j in range(len(A[0])):
        A[i][j] = pygambit.Rational(int(A[i][j]))

print("Intemediate", A)

# Minus transpose
B = A
for i in range(size - 1):
    B = np.concatenate((B,A),axis=1)
B = B - np.transpose(B)
print("Concat", B)
A = B


g = pygambit.Game.from_arrays(A, -np.transpose(A))
print("Solving")
res = pygambit.nash.lcp_solve(g, rational=False, use_strategic=True)
print("len %d" % len(res))

prob = np.empty(size)
for i in range(len(res)):
    print("============== Equilibrium %d" % i)
    arr = res[i]
    l = int(len(arr) / 2)
    s = game_size * game_size
    # Verify the sum of probability
    at = np.empty(s)
    for ran in range(l):
        at[ran] = arr[ran]
    print(len(at), sum(at))
    for j in range(game_size):
        for k in range(game_size):
            f = j * game_size + k
            if at[f] >= 0.00001:
                prob[j] = at[f]
                print("   ****** Attack/Depend Prob")
                print("%s: %s: %f" % (pokemon_types[j], pokemon_types[k], at[f]))
    print("Expected payout:")
    x = res[i].payoff()
    print("Attacker payoff", x[0] / 8.0)
    print("Defender payoff", x[1] / 8.0)

#for i in range(len(prob)):
#    print("** Attacker/Def chose")
#    print("%s: %f" % (pokemon_types[i], prob[i]))

print(prob)

