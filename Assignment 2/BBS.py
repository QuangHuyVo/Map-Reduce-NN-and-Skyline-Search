import time
from rtree import *
from Sequential import *


def mindist_to_origin(point):
    return (point['x'] ** 2 + point['y'] ** 2) ** 0.5

# Branch and Bound Skyline (BBS) Algorithm
def bbs_skyline(homes):
    start = time.time()
    index = RTree()
    for home in homes:
        index.insert(index.root, {'x': home[1], 'y': home[2]})
    
    index_rtree_time = time.time()
    skyline = []
    heap = [child for child in index.root.child_nodes]
    heap = sorted(heap, key=lambda x: mindist_to_origin({"x": x.MBR['x1'], "y": x.MBR['y1']}))

    while heap:

        n = heap.pop(0)
        if isinstance(n, Node):
            dominate = False
            for point in skyline:
                if is_dominated((0, point["x"], point["y"]), (0, n.MBR['x1'], n.MBR['y1'])):
                    dominate = True
                    break
            if not dominate:
                if n.is_leaf():
                    heap.extend(n.data_points)
                else:
                    heap.extend(n.child_nodes)
                heap = sorted(heap, key=lambda x: mindist_to_origin({"x": x.MBR['x1'], "y": x.MBR['y1']}) if isinstance(x, Node) else mindist_to_origin(x))
        else:
            dominate = False
            for point in skyline:
                if is_dominated((0, point["x"], point["y"]), (0, n['x'], n['y'])):
                    dominate = True
                    break
            if not dominate:
                skyline.append(n)
    return skyline, index_rtree_time - start, time.time() - index_rtree_time
   
def write_output_to_file(filename, skyline, execution_time):
    with open(filename, 'w') as file:
        file.write("Skyline Points:\n")
        for point in skyline:
            file.write(f"({point['x']}, {point['y']})\n")
        file.write(f"Total Execution Time: {execution_time:.6f} seconds\n")

# Main function
def main():
    # Load dataset
    dataset = load_dataset('city1.txt')

    # Branch and Bound Skyline (BBS) Algorithm
    skyline_bbs, rtree_time, bbs_time = bbs_skyline(dataset)
    print("\nSkyline using BBS Algorithm:")
    for home in skyline_bbs:
        print(home)
    print(f"Time taken for R-tree construction: {rtree_time:.6f} seconds")
    print(f"Time taken for BBS Algorithm: {bbs_time:.6f} seconds")
    print(f"Total time for BBS Algorithm: {rtree_time + bbs_time:.6f} seconds")
    write_output_to_file('skyline_bbs.txt', skyline_bbs, bbs_time)

if __name__ == "__main__":
    main()
