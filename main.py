import numpy as np
import math
import matplotlib.pyplot as plt
import random
from repair_team import RepairTeam
from element import Element

N = 30000
n = 5
l = 1.1
m = 1.2
T = 7
step = 0.1
elements = np.zeros(n, dtype=Element)
E = np.zeros(int(T / step + 1))


def time_model(e):
    tmp_tw = -math.log(random.random()) / l
    tmp_tr = -math.log(random.random()) / m
    e.Tw = tmp_tw
    e.Tr = tmp_tr


def is_working(e, t, r1, r2, r3, r4):
    tmp = math.floor(t / (e.Tw + e.Tr))
    if (t - (tmp * (e.Tw + e.Tr))) <= e.Tw:
        e.is_working = True
    else:
        e.is_working = False
        if r1.repair_num == e.index:
            if r1.ending <= t + step:
                e.Tr -= step * e.wait
                e.wait = 0
                r1.free()
            return
        if r2.repair_num == e.index:
            if r2.ending <= t + step:
                e.Tr -= step * e.wait
                e.wait = 0
                r2.free()
            return
        if r3.repair_num == e.index:
            if r3.ending <= t + step:
                e.Tr -= step * e.wait
                e.wait = 0
                r3.free()
            return
        if r4.repair_num == e.index:
            if r4.ending <= t + step:
                e.Tr -= step * e.wait
                e.wait = 0
                r4.free()
            return
    if r1.status:
        r1.start_repairing(False, (tmp + 1) * (e.Tw + e.Tr), e.index)
    elif r2.status:
        r2.start_repairing(False, (tmp + 1) * (e.Tw + e.Tr), e.index)
    elif r3.status:
        r3.start_repairing(False, (tmp + 1) * (e.Tw + e.Tr), e.index)
    elif r4.status:
        r4.start_repairing(False, (tmp + 1) * (e.Tw + e.Tr), e.index)
    else:
        e.Tr += step
        e.wait += 1


def one_experiment():
    for i in range(n):
        tmp = Element()
        tmp.index = i
        tmp.wait = 0
        tmp.is_working = False
        elements[i] = tmp
    for i in range(n):
        time_model(elements[i])
    rep1 = RepairTeam()
    rep2 = RepairTeam()
    rep3 = RepairTeam()
    rep4 = RepairTeam()
    ndx = 0
    t = 0
    while t < T:
        for i in range(n):
            is_working(elements[i], t, rep1, rep2, rep3, rep4)
        if elements[0].is_working and (elements[1].is_working or elements[2].is_working or elements[3].is_working) and \
            elements[4].is_working:
            E[ndx] += 1
        ndx += 1
        t += step
    clear()


def clear():
    for i in range(n):
        elements[i].is_working = False


def upper_bound():
    k11 = m / (m + l)
    k = (k11 ** 2) * (1 - (1 - k11) ** 3)
    arr = []
    t = 0
    k_ar = []
    while t <= T:
        arr.append(t)
        k_ar.append(k)
        t += step
    return k_ar, arr


def lower_bound():
    k11 = m / (m + l)
    k21 = ((2 * m * l) + m ** 2) / (2 * l ** 2 + 2 * m * l + m ** 2)
    k1 = k11 ** 2 * (1 - (1 - k21) * (1 - k11))
    k2 = k11 ** 2 * (1 - (1 - k11) ** 2)
    arr = []
    t = 0
    k1_ar = []
    k2_ar = []
    while t <= T:
        arr.append(t)
        k1_ar.append(k1)
        k2_ar.append(k2)
        t += step
    return k1_ar, k2_ar, arr


def modeling():
    k_ar, t_ar = upper_bound()
    k_ar1, k_ar2, t_ar1 = lower_bound()
    for i in range(N):
        one_experiment()
    ndx = 0
    t = 0
    Kr = []
    tr = []
    while t < T:
        tr.append(t)
        Kr.append(E[ndx] / N)
        t += step
        ndx += 1
    plt.title('Kr(t)')
    plt.grid()
    plt.plot(tr, Kr, label='Kr(t)')
    plt.plot(t_ar, k_ar, label='Верхняя граница')
    plt.plot(t_ar1, k_ar1, label='Нижняя граница (распределение бригад)')
    plt.plot(t_ar1, k_ar2, label='Нижняя граница (исключение систем)')
    plt.legend()
    plt.savefig('func.png')
    plt.show()


def main():
    one_experiment()
    modeling()


if __name__ == '__main__':
    main()
