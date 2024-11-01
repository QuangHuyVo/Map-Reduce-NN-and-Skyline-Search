import time
from Sequential import load_dataset, is_dominated
from BBS import write_output_to_file, bbs_skyline


def merge_skylines(left_skyline, right_skyline):
    merged_skyline = []
    i, j = 0, 0

    while i < len(left_skyline) and j < len(right_skyline):
        if left_skyline[i]['x'] < right_skyline[j]['x']:
            merged_skyline.append(left_skyline[i])
            i += 1
        elif left_skyline[i]['x'] > right_skyline[j]['x']:
            merged_skyline.append(right_skyline[j])
            j += 1
        else:
            if left_skyline[i]['y'] < right_skyline[j]['y']:
                merged_skyline.append(left_skyline[i])
                i += 1
            else:
                merged_skyline.append(right_skyline[j])
                j += 1

    while i < len(left_skyline):
        merged_skyline.append(left_skyline[i])
        i += 1

    while j < len(right_skyline):
        merged_skyline.append(right_skyline[j])
        j += 1

    final_skyline = []
    for point in merged_skyline:
        dominated = False
        for sk_point in final_skyline:
            if is_dominated((0, sk_point['x'], sk_point['y']), (0, point['x'], point['y'])):
                dominated = True
                break
        if not dominated:
            final_skyline.append(point)
    
    return final_skyline

def divide_and_conquer_bbs(homes):
    if len(homes) <= 1:
        return homes, 0, 0

    # Divide the dataset into two subspaces based on the X dimension
    homes.sort(key=lambda x: x[1])
    mid = len(homes) // 2
    left_homes = homes[:mid]
    right_homes = homes[mid:]

    start_dc_time = time.time()
    # Construct R-trees and apply BBS algorithm
    left_skyline, left_insertion_time, left_bbs_time = bbs_skyline(left_homes)
    right_skyline, right_insertion_time, right_bbs_time = bbs_skyline(right_homes)
    end_dc_time = time.time()

    merge_time = end_dc_time - start_dc_time
    insertion_time = left_insertion_time + right_insertion_time
    bbs_time = left_bbs_time + right_bbs_time

    # Merge the skylines
    final_skyline = merge_skylines(left_skyline, right_skyline)
    return final_skyline, insertion_time, merge_time, bbs_time

def main():
    # Load dataset
    dataset = load_dataset('city1.txt')
    
    # Divide and Conquer BBS Algorithm
    start_time = time.time()
    skyline_dnc, insertion_time, merge_time, bbs_time = divide_and_conquer_bbs(dataset)
    end_time = time.time()
    execution_time_dnc = end_time - start_time
    
    print("Skyline using Divide and Conquer BBS:")
    for home in skyline_dnc:
        print(home)
    print(f"Time taken for Divide and Conquer BBS: {execution_time_dnc:.6f} seconds")
    print(f"R-tree Insertion Time: {insertion_time:.6f} seconds")
    print(f"Divide and Conquer Time: {merge_time:.6f} seconds")
    print(f"BBS Time: {bbs_time:.6f} seconds")
    
    # Write output to file
    write_output_to_file('skyline_dc.txt', skyline_dnc,bbs_time)

if __name__ == "__main__":
    main()
