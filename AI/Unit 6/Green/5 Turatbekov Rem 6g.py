import sys, math

stars, stars_dct, n = [], {}, 0

indices = [int(i) for i in sys.argv[1:]]

with open("star_data.csv") as f:
    for i, l in enumerate(f):
        if i>0:
            data = l.strip().split(",")[:-2]
            stars.append([math.log(float(i)) for i in data[:-2]]+[float(data[-2])])
            stars_dct[tuple([math.log(float(i)) for i in data[:-2]]+[float(data[-2])])] = data[-1]

stars_copy = [star.copy() for star in stars]

def sdist(star, mean):
    return sum((s-m)**2 for s, m in zip(star, mean))

def kmeans(stars, k=6):
    global n
    # means = [random.sample(stars, k)[i] for i in range(k)]
    means = [stars[i].copy() for i in indices]
    while True:
        n += 1
        associated = [[] for _ in range(k)]
        for star in stars:
            dists = [sdist(star, s) for s in means]
            associated[dists.index(min(dists))].append(star)
        new_means = []
        for star_group in associated:
            avg_star = [sum(i)/len(i) for i in zip(*star_group)]
            new_means.append(avg_star)
        if all(sdist(old, new) < 1e-10 for old, new in zip(means, new_means)):
            break
        means = [i.copy() for i in new_means]
        
    return means, associated

means, associated = kmeans(stars)

for i, star_group in enumerate(associated):
    print("Mean:",means[i])
    for star in star_group:
        print(stars_dct[tuple(star)], star)
    print()

print("Iterations:",n)
