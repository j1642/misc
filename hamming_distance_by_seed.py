"""Plot 8 Hamming distance histograms, with respective averages, for a set
of consecutive pseudorandom number generator seeds.

Accepts one optional command line argument for the first seed integer.
"""
import random
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt


def find_hamming_distances(seed):
    """Return list of Hamming distances for all pairs of 64 bit
    pseudorandom numbers.
    """
    print(f'Calculating seed {seed}...')
    random.seed(seed)
    nums = [random.randint(0, 2 ** 64 - 1) for i in range(781)]
    hamming_distances = []
    for i, num1 in enumerate(nums[:-1]):
        for num2 in nums[i+1:]:
            hamming_distances.append(str(num1 ^ num2).count('1'))
            if num1 ^ num2 == 0:
                print(f'xor to 0: {num1}, {num2}')

    return hamming_distances


if len(sys.argv) > 1:
    start_seed = int(sys.argv[1])
else:
    start_seed = 100

seeds = list(range(start_seed, start_seed + 8))
fig, axs = plt.subplots(2, 4, figsize=(8, 5))

for i in range(8):
    if i < 4:
        ax = axs[0, i]
    else:
        ax = axs[1, i - 4]
    hamming_distances = find_hamming_distances(seeds[i])
    ax.hist(hamming_distances)
    avg = sum(hamming_distances) / len(hamming_distances)
    ax.axvline(avg, color='red', linewidth=1.5)
    ax.set_title('Seed {}, avg={:.5}'.format(seeds[i], avg), size='medium')

fig.suptitle('Hamming Distance Histograms for Pseudorandom Integers')
plt.tight_layout()
plt.show()
