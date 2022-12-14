import scipy.stats


def test(seq, name, quantile):
    print("Testing `" + name + "` RNG, with quantile:", quantile)
    print("Equal Distribution:")
    res, empiric, theoretic = equal_distribution(seq, quantile)
    print("result:", res, "with empiric:", empiric, "and theoretic:", theoretic, "quantiles")
    print("Independence:")
    res, empiric, theoretic = independence(seq, quantile)
    print("result:", res, "with empiric:", empiric, "and theoretic:", theoretic, "quantiles")
    print("Homogeneity:")
    res, empiric, theoretic = homogeneity(seq, quantile)
    print("result:", res, "with empiric:", empiric, "and theoretic:", theoretic, "quantiles")
    print("\n")


def equal_distribution(dist, alpha):
    dist_list = [dist[i:i + 8] for i in range(0, len(dist), 8)]
    m = len(dist_list)
    n = m / 256

    count_map = {}
    for item in dist_list:
        count_map[item] = count_map.get(item, 0) + 1

    chi_square = 0

    for count in count_map.values():
        chi_square += ((count - n) ** 2) / n

    q = scipy.stats.chi2.ppf(1 - alpha, df=(n - 1))

    return chi_square < q, chi_square, q


def independence(dist, alpha):
    dist_list = [dist[i:i + 8] for i in range(0, len(dist), 8)]
    m = len(dist_list)
    n = m / 2
    chi_square, s, k = chi2sum(dist_list)
    chi_square = (chi_square - 1) * n

    q = scipy.stats.chi2.ppf(1 - alpha, (s - 1) * (k - 1))

    return chi_square < q, chi_square, q


def homogeneity(dist, alpha):
    dist_list = [dist[i:i + 8] for i in range(0, len(dist), 8)]
    m = len(dist_list)
    r = 10
    m2 = m // r
    n = m2 / 2

    new_dist_list = [dist_list[i:i + m2] for i in range(0, len(dist_list), m2)]

    count_map = {}
    count_map_2 = {}
    for i in range(r):
        sub_list = new_dist_list[i]
        for k in range(len(sub_list) - 1):
            item = sub_list[k]
            # v_ij
            count_map[(i, item)] = count_map.get((i, item), 0) + 1
            # v_i
            count_map_2[item] = count_map_2.get(item, 0) + 1

    s = len(count_map_2)
    chi_square = 0

    for double in count_map.keys():
        list_index, item = double
        chi_square += (count_map[(list_index, item)]**2 / (count_map_2[item] * m2))

    chi_square -= 1
    chi_square *= n
    q = scipy.stats.chi2.ppf(1 - alpha, (s - 1) * r)

    return chi_square < q, chi_square, q


def chi2sum(dist):
    count_map_first = {}
    count_map_second = {}
    count_map_double = {}

    for i in range(0, len(dist) - 1, 2):
        item = dist[i]
        item_next = dist[(i + 1)]

        count_map_first[item] = count_map_first.get(item, 0) + 1
        count_map_second[item_next] = count_map_second.get(item_next, 0) + 1
        count_map_double[(item, item_next)] = count_map_double.get((item, item_next), 0) + 1

    chi_square = 0

    for double in count_map_double.keys():
        item, item_next = double
        chi_square += (count_map_double[double] ** 2 / (count_map_first[item] * count_map_second[item_next]))

    return chi_square, len(count_map_first), len(count_map_second)
