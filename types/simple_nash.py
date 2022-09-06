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



E = np.array([[4, 4, 16],
              [16, 4, 4],
              [4, 16, 4]], dtype=pygambit.Rational)

A = E
A = A - np.transpose(A)
print(A)

g = pygambit.Game.from_arrays(A, -np.transpose(A))
print("Solving")
res = pygambit.nash.lcp_solve(g, use_strategic=True)
print("len %d" % len(res))

game_size = len(A)

for i in range(len(res)):
    x = res[i].payoff()
    arr = res[i]
    l = len(arr) / 2
    #if x[0] / 8.0 > 0.05:
    #    continue
    print("============== Equilibrium %d" % i)
    at = np.empty(game_size)
    de = np.empty(game_size)
    for j in range(game_size):
        at[j] = arr[j]
        de[j] = arr[j + game_size]
    print("** Attacker chose")
    for k in range(game_size):
        print("%s: %.3f" % (pokemon_types[k], at[k]))
    print("** Defender chose")
    for k in range(game_size):
        print("%s: %.3f" % (pokemon_types[k], de[k]))
    print("Expected payout:")
    print("Attacker payoff", x[0] / 8.0)
    print("Defender payoff", x[1] / 8.0)
    print(at)
