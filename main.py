import math
import numpy

# Mateusz Niestrój 259487
# Data prezentacji 08.03.2023
S = 8  # dB
f = 4.87  # GHz
lambd = 3e8 / 4.87e9  # m

# d - odległość pomiędzy otworami, należy do przedziału <lambd / 10, lambd>
d_min = lambd / 10  # m
d_max = lambd

# l - wielkość otworów (najdłuższy odcinek w otworze), należy do przedziału <0.001, lambd / 2)
l_min = 0.001  # m
l_max = lambd / 2

# x - bok ekranu
shield_side = 0.5  # m


def triangle_side(l):
    return l * math.sqrt(2) / 2


def cal_shielding(l, n):
    if n > 0:
        return 20 * math.log10(lambd / (2 * l)) - 20 * math.log10(math.sqrt(n))
    else:
        return 20 * math.log10(lambd / (2 * l))


shielding = []
l_len = []
d_len = []
holes_num = []
neighbors = []
holes_surface = []

if __name__ == "__main__":

    for d in numpy.arange(d_min, d_max, 0.001):
        for l in numpy.arange(l_min, l_max, 0.001):
            row_len = 0  # długośc rzędu jaka się zmieści na ekranie, bok trójkąta prostokątnego równoramiennego (czyli przeciwprostokątna (wyliczona na podstawie l, czyli l * sqrt(2)) + odległość d
            n = 0  # ilość otworów w rzędzie
            side = triangle_side(l)  # obliczona przyprostokątna

            while row_len + side < shield_side:
                row_len += side
                n += 1
                if (row_len + d) < shield_side:
                    row_len += d
                else:
                    n_2 = 0  # ilość sąsiadów mieszcących się w rzędzie na odcinku lambda
                    row_len_2 = 0  # długość rzędu, przyprostokątna + d, aż nie mieści cię na odcinku lambda
                    while True:
                        if row_len_2 + side <= lambd:
                            row_len_2 += side
                            n_2 += 1
                        else:
                            break
                        if row_len_2 + d <= lambd:
                            row_len_2 += d
                        else:
                            break

                    if 8.5 >= cal_shielding(l, n_2 - 1) >= S:
                        print(cal_shielding(l, n_2 - 1))
                        print(l)
                        print(d)
                        print(n * n)
                        print(side * 100 * side * 100 / 2 * n * n)
                        print(n_2 - 1)
                        print()
                        shielding.append(cal_shielding(l, n_2 - 1))
                        l_len.append(l)
                        d_len.append(d)
                        holes_num.append(n * n)
                        neighbors.append(n_2 - 1)
                        holes_surface.append(side * 100 * side * 100 / 2 * n * n)
                        break

    print(f'Największa wartość l: {max(l_len) * 100}cm')
    print(f'Największa ilość otworów: {max(holes_num)}')
    print(f'Największa całkowita powierzchnia otworów: {round(max(holes_surface), 2)}cm^2')
    print(f'Stosunek największej powierzchni otworów do powierzchni ekranu: {round(max(holes_surface) / ((shield_side ** 2) * 10000), 4)}')
    print(f'Najmniejsza wartość l: {round(min(l_len) * 100, 2)}cm')
    print(f'Najmniejsza ilość otworów: {min(holes_num)}')
    print(f'Najmniejsza całkowita powierzchnia otworów: {round(min(holes_surface), 2)}cm^2')
    print(f'Stosunek najmniejszej powierzchni otworów do powierzchni ekranu: {round(min(holes_surface) / ((shield_side ** 2) * 10000), 4)}')
