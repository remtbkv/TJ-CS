
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
