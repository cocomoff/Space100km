import pickle
import dill
from sklearn import neighbors
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def main(th=100):
    multi_poly = dill.load(open("data/japan-res-5.pickle", "rb"))

    # 0~3の島を描画する
    lXall, lYall = [], []
    for k in range(4):
        lXk, lYk = multi_poly[k].exterior.coords.xy
        f = plt.figure()
        a = f.gca()
        a.plot(lXk, lYk, lw=2, c="k")
        lXall += list(lXk)
        lYall += list(lYk)
        plt.savefig(f"output/{k}.png", bbox_inches="tight", facecolor="w")

    # 全部描画する
    f = plt.figure()
    a = f.gca()
    for k in range(4):
        lXk, lYk = multi_poly[k].exterior.coords.xy
        a.plot(lXk, lYk, lw=2, c="k")
    plt.savefig("output/japan.png", bbox_inches="tight", facecolor="w")


    # 候補地点
    lX, lY = pickle.load(open("data/xy.pickle", "rb"))

    # KDTreeを使いつつ調べる
    data = list(zip(lXall, lYall))
    tree = neighbors.KDTree(data)
    indices = []
    for i in range(len(lX)):
        xi, yi = lX[i], lY[i]
        di, ii = tree.query([[xi, yi]], k=1)
        ii = ii[0]
        max_dij = 0
        for k, j in enumerate(ii):
            dij = haversine(xi, yi, lXall[j], lYall[j])
            max_dij = max(max_dij, dij)
        if max_dij >= th:
            indices.append(i)

    # 可視化
    f = plt.figure(figsize=(8, 6))
    a = f.gca()
    ppX = [lX[j] for j in indices]
    ppY = [lY[j] for j in indices]
    for k in range(4):
        a.plot(*multi_poly[k].exterior.coords.xy, c="k")
    a.scatter(lX, lY, c="r", alpha=0.3, s=30)
    a.scatter(ppX, ppY, c="r", s=30)
    plt.savefig(f"output/japan-{th}km.png", bbox_inches="tight", facecolor="w")
    plt.close()

    

if __name__ == '__main__':
    main()
    main(th=80)
    main(th=50)