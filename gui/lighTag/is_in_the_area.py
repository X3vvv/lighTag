import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

triangle = [(1, 2), (2, 4), (4, 3)]
polygon = [(1, 1), (5, 4), (2, 5), (4, 2)]


def is_in_tria(x, y):
    cross_n = 0
    cross_edge_n = 0

    for i in range(len(triangle)):
        is_crossed, crossed_on_edge = has_crossed(
            x, y, *triangle[i], *triangle[(i + 1) % len(triangle)]
        )
        if is_crossed:
            cross_n += 1
            if crossed_on_edge:
                cross_edge_n += 1

    if cross_edge_n > 0:
        cross_n = cross_n - cross_edge_n + 1

    # print("Cross time:", cross_n)
    # return (cross_n % 2) == 1
    if (cross_n % 2) != 1:
        return False

    # 2nd time
    cross_n = 0
    cross_edge_n = 0

    for i in range(len(triangle)):
        is_crossed, crossed_on_edge = has_crossed(
            x, y, *triangle[i], *triangle[(i + 1) % len(triangle)], -1
        )
        if is_crossed:
            cross_n += 1
            if crossed_on_edge:
                cross_edge_n += 1

    if cross_edge_n > 0:
        cross_n = cross_n - cross_edge_n + 1

    # print("Cross time:", cross_n)
    # return (cross_n % 2) == 1
    if (cross_n % 2) != 1:
        return False

    return True


def is_in_poly(x, y):
    pass


def has_crossed(xt, yt, x1, y1, x2, y2, k=1):
    if yt < min(y1, y2) or yt > max(y1, y2):  # or xt < min(x1, x2) or xt > max(x1, x2):
        # print(
        #     "y={} cannot cross with line ({}, {})-({}, {})".format(yt, x1, y1, x2, y2)
        # )
        return False, False

    x = (yt - y2) * (x1 - x2) / (y1 - y2) + x2
    crossed_on_edge = (x == x1 and yt == y1) or (x == x2 and yt == y2)
    # print(
    #     "x = (yt-y2) * (x1-x2) / (y1-y2) + x2 = {} x {} / {} + {} = {}  --->  crossed at ({}, {})".format(
    #         (yt - y2), (x1 - x2), (y1 - y2), x2, x, x, yt
    #     )
    # )
    return (
        (x >= xt) if k == 1 else (x <= xt),
        crossed_on_edge,
    )  # count in on-edge situations


def draw_graph(graph_dot_list):
    for i in range(len(graph_dot_list)):
        dot1, dot2 = graph_dot_list[i], graph_dot_list[(i + 1) % len(graph_dot_list)]
        plt.plot(np.array([dot1[0], dot2[0]]), np.array([dot1[1], dot2[1]]))


# dots = ((2, 3), (5, 3), (2, 0.5))
dots = ((0, 3), (2, 10), (3, 3))
# for dot in dots:
#     print(
#         "Whether {} is in the triangle ({}): {}".format(dot, triangle, is_in_tria(*dot))
#     )
# print("Whether {} is in the polygon ({}): {}".format(dot, polygon, is_in_poly(*dot)))

for x in tqdm(np.arange(0, 5, 0.05)):
    for y in np.arange(0, 5, 0.05):
        color = "mo" if is_in_tria(x, y) else "co"
        plt.plot(x, y, color, markersize=1)

draw_graph(triangle)

plt.show()
