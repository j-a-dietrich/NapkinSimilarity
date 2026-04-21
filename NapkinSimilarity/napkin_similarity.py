import numpy as np
from numba import njit


@njit
def calc_score(mz1, int1, mz2, int2, ppm):

    i = 0
    j = 0

    spec1_density = 0.0
    spec2_density = 0.0
    spec12_density = 0.0

    nmax = min(len(mz1), len(mz2))

    match_mz = np.empty(nmax, dtype=np.float64)
    match_score = np.empty(nmax, dtype=np.float64)

    k = 0

    for v in int1:
        spec1_density += v

    for v in int2:
        spec2_density += v

    while i < len(mz1) and j < len(mz2):

        mz_a = mz1[i]
        mz_b = mz2[j]

        tol = mz_a * ppm * 1e-6
        diff = mz_a - mz_b

        if abs(diff) <= tol:

            contrib = 0.5 * (int1[i] + int2[j])

            spec12_density += contrib

            match_mz[k] = 0.5 * (mz_a + mz_b)
            match_score[k] = contrib
            k += 1
            
            i += 1
            j += 1

        elif diff < 0:
            spec12_density += int1[i]
            i += 1
        else:
            spec12_density += int2[j]
            j += 1

    while i < len(mz1):
        spec12_density += int1[i]
        i += 1

    while j < len(mz2):
        spec12_density += int2[j]
        j += 1

    if spec1_density == 0.0 and spec2_density == 0.0:
        spec1_density = 0.001

    score = 2.0 * (1.0 - spec12_density / (spec1_density + spec2_density))
    
    return score, match_mz[:k], match_score[:k]


def run(spec1, spec2, ppm=10):
    def sorted_score(mz_a, int_a, mz_b, int_b):
        o1, o2 = np.argsort(mz_a), np.argsort(mz_b)
        return calc_score(mz_a[o1], int_a[o1], mz_b[o2], int_b[o2], ppm)

    peak_score, matched_mz, matched_mz_score = sorted_score(
        spec1.peaks.mz, spec1.peaks.intensities,
        spec2.peaks.mz, spec2.peaks.intensities
    )
    loss_score, matched_loss, matched_loss_score = sorted_score(
        spec1.losses.mz, spec1.losses.intensities,
        spec2.losses.mz, spec2.losses.intensities
    )
    return (peak_score + loss_score)/2, matched_mz, matched_mz_score # losses are ignored for now