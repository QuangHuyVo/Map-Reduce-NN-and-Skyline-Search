import time

# Function to load a dataset from a text file
def load_dataset(file_path):
    dataset = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            home_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            dataset.append((home_id, x, y))
    return dataset

# Function to check if one point (q) is dominated by another point (p)
def is_dominated(p, q):
    return p[1] <= q[1] and p[2] <= q[2] and (p[1] < q[1] or p[2] < q[2])

# Sequential Scan Based Method
def sequential_scan_skyline(homes):
    skyline = []
    for p in homes:
        dominated = False
        to_remove = []
        for q in skyline:
            if p != q and is_dominated(q, p):
                dominated = True
                break
            if is_dominated(p, q):
                to_remove.append(q)

        if not dominated:
            skyline.append(p)
            for q in to_remove:
                skyline.remove(q)

    return skyline

def write_output(filename, skyline, execution_time):
    with open(filename, 'w') as file:
        for point in skyline:
            file.write(f"{point[0]} {point[1]} {point[2]}\n")
        file.write(f"Execution Time: {execution_time:.4f} seconds\n")

def main():
    # Load dataset
    dataset = load_dataset('city1.txt')

    # Sequential Scan Based Method
    start_time = time.time()
    skyline_sequential = sequential_scan_skyline(dataset)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Skyline using Sequential Scan:")
    for home in skyline_sequential:
        print(home)
    print(f"Time taken for Sequential Scan: {end_time - start_time:.6f} seconds")
    write_output('skyline_sequential_scan.txt', skyline_sequential, execution_time)

if __name__ == "__main__":
    main()