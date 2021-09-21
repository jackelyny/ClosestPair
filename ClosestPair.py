import sys
import math


def by_x(points):
    return points[0]


def by_y(points):
    return points[1]


# Euclidean formula
def get_distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def distance_from_pair(points):
    return get_distance(points[0], points[1])


def brute_euclidean(points):
    if len(points) == 1:
        return points
    min = (points[0], points[1])
    for i in range(1, len(points)-1):
        for j in range(i+1, len(points)):
            calc = get_distance(points[i], points[j])
            if calc <= get_distance(min[0], min[1]):
                min = (points[i], points[j])
    return min


def dq_euclidean(section):
    if len(section) <= 80:
        return brute_euclidean(section)
    else:
        partition_index = int(len(section)/2)
        l_points = dq_euclidean(section[:partition_index])
        r_points = dq_euclidean(section[partition_index:])
        if get_distance(l_points[0], l_points[1]) > get_distance(r_points[0], r_points[1]):
            return r_points
        else:
            return l_points


def bin_search(points, target):
    l = 0
    r = len(points)-1
    while l < r:
        m = int((l+r)/2)
        if points[m] < target:
            l = m+1
        else:
            r = m-1
    return l


input = open(sys.argv[1], 'r')
data = input.read().strip().split('\n')
n = int(data[0])
points = []
for i in range(1, n+1):
    line = data[i].split(' ')
    points.append((float(line[0]), float(line[1])))
points.sort(key=by_x)

partition_index = math.ceil(n/2)
all_l = points[:int(partition_index)]
all_r = points[int(partition_index):]
best_l = dq_euclidean(all_l)
best_r = dq_euclidean(all_r)
if distance_from_pair(best_l) <= distance_from_pair(best_r):
    best_pair = best_l
else:
    best_pair = best_r
best_delta = distance_from_pair(best_pair)
x_middle = (all_l[-1][0] + all_r[0][0]) / 2
# Call binary search and only look at the points' x-values
l_cutoff = bin_search([x[0] for x in all_l], x_middle-best_delta)
r_cutoff = bin_search([x[0] for x in all_r], x_middle+best_delta) + 1  # Add 1 to include last index
subset = points[int(l_cutoff):int(r_cutoff+partition_index)]
right_slice = subset[int(len(subset) / 2):]
right_slice.sort(key=by_y)
for p in subset[:int(len(subset)/2)]:
    bot_cutoff = bin_search([y[1] for y in right_slice], p[1]-best_delta)
    top_cutoff = bin_search([y[1] for y in right_slice], p[1]+best_delta) + 1
    for q in right_slice[bot_cutoff:top_cutoff]:
        if get_distance(p, q) < best_delta:
            best_pair = (p, q)
            best_delta = distance_from_pair(best_pair)

print('============= OPTIMAL =============')
print('Closest Pair: \n(%.3f, %.3f)\n (%.3f, %.3f)' % (best_pair[0][0], best_pair[0][1], best_pair[1][0], best_pair[1][1]))
print('Distance: %.4f' % get_distance(best_pair[0], best_pair[1]))
input.close()