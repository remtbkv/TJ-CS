from PIL import Image, ImageDraw
import sys, random
from time import perf_counter
global k

# fn = "luxurious_toilet.jpg"
# k = 8

# if len(sys.argv[1:])>0:
fn, k = sys.argv[1], int(sys.argv[2])

img = Image.open(fn).convert("RGB")
width, height = img.size

pix = img.load()

# 27
# for x in range(width):
#     for y in range(height):
#         new_color = []
#         color = pix[x, y]
#         for n in color:
#             if n<255//3:
#                 new_color.append(0)
#             elif n>255*2//3:
#                 new_color.append(255)
#             else:
#                 new_color.append(127)
#         pix[x,y] = tuple(new_color)

# img.save("out.png")
# 8
# for x in range(width):
#     for y in range(height):
#         new_color = []
#         color = pix[x, y]
#         for n in color:
#             if n < 128:
#                 new_color.append(0)
#             else:
#                 new_color.append(255)
#         pix[x, y] = tuple(new_color)
# means = [(0, 0, 0), (255, 255 , 255)]


def sdist(color1, color2):
    return sum((s-m)**2 for s, m in zip(color1, color2))


def plusplus_means(all_colors):
    means = [random.choice(all_colors)]
    while len(means) < k:
        # create distribution
        probs = [min(sdist(color1, color2) for color2 in means) for color1 in all_colors]
        sum_probs = sum(probs)
        distribution = [p / sum_probs for p in probs]
        # weighted choice
        cum_dist, total = [], 0
        for p in distribution:
            total += p
            cum_dist.append(total)
        r, i = random.random()*cum_dist[-1], 0
        while r>=cum_dist[i]: # break if r<cp
            i+=1
        means.append(all_colors[i])
    return means


def normal_means():
    starting, sxy, sc = [], set(), set()
    while len(starting) < k:
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        color = pix[x, y]
        while (x, y) in sxy or color in sc:
            x, y = random.randint(0, width+1), random.randint(0, height+1)
            color = pix[x, y]
        sc.add(color)
        sxy.add(coord := (x, y))
        starting.append(coord)
    return [pix[i] for i in starting]


def kmeans(n=0):
    color_counts = {}
    for x in range(width):
        for y in range(height):
            color = pix[x, y]
            if color in color_counts:
                color_counts[color] += 1
            else:
                color_counts[color] = 1
    means = plusplus_means(list(color_counts))
    associations = [[] for _ in range(k)]
    while True:
        n+=1
        print("gen",n)
        new = [[] for _ in range(k)]
        for color, count in color_counts.items():
            dists = [sdist(color, mean_color) for mean_color in means]
            new[dists.index(min(dists))].append((color, count))
        associations, new_means = new, []
        
        for color_count in associations:
            weighted, total_colors = [0]*3, 0
            for color, count in color_count:
                total_colors += count
                for i, c in enumerate(color):
                    weighted[i] += c*count
            avg_color = tuple(weighted[i] / total_colors for i in range(3))
            new_means.append(avg_color)
        int_mn, int_mo= [[int(i) for i in c] for c in new_means], [[int(i) for i in c] for c in means]

        if all(sum(old)-sum(new) == 0 for old, new in zip(int_mo, int_mn)):
            break
        means = new_means.copy()
    return means, associations


def dithering(means):   
    new_img = Image.new("RGB", (width, height), 0)
    new_pix = new_img.load()
    for y in range(height):
        for x in range(width):  
            tmp = pix[x,y]
            old = tuple(min(255, max(0, n)) for n in tmp)
            new = min(means, key=lambda c: sdist(old, c))
            new_pix[x,y] = new
            e = tuple(o-n for o, n in zip(old, new))
            for dx, dy, ratio in [(1, 0, 7/16), (-1, 1, 3/16), (0, 1, 5/16), (1, 1, 1/16)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    curr = pix[nx, ny]
                    adjusted = tuple(curr[i] + e[i]*ratio for i in range(3)) # clips automatically with pix
                    adjusted = tuple(min(255, max(0, n)) for n in adjusted)
                    pix[nx, ny] = tuple(map(int, adjusted))
    return new_img


start = perf_counter()
means, associations = kmeans()
print(perf_counter()-start)

means = [tuple(int(j) for j in i) for i in means]

def save_img(means, associations):
    color_mean = {}
    for i, info in enumerate(associations):
        for color, _ in info:
            color_mean[color] = means[i]

    img = dithering(means)
    # for x in range(width):
    #     for y in range(height):
    #         pix[x,y] = color_mean[pix[x,y]]

    sq_w = width//k
    sq_h = sq_w

    strip_img = Image.new('RGB', (width, sq_h))
    draw = ImageDraw.Draw(strip_img)
    for i, color in enumerate(means):
        draw.rectangle([i*sq_w, 0, (i+1)*sq_w, sq_h], fill=color)
    new_img = Image.new('RGB', (width, height+sq_h), 0)
    new_img.paste(img, (0, 0))
    new_img.paste(strip_img, (0, height))
    new_img.save("kmeansout.png")

save_img(means, associations)
