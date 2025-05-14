import csv, time, math

# Swap elements based on the sorting direction
def compare_and_swap(arr, i, j, d):
    if (d and arr[i]["TotalReviews"] > arr[j]["TotalReviews"]) or (not d and arr[i]["TotalReviews"] < arr[j]["TotalReviews"]):
        arr[i], arr[j] = arr[j], arr[i]

# Merge two halves in a bitonic manner
def bitonic_merge(arr, low, cnt, d):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k): compare_and_swap(arr, i, i + k, d)
        bitonic_merge(arr, low, k, d)
        bitonic_merge(arr, low + k, k, d)

# Recursively perform bitonic sort
def bitonic_sort(arr, low, cnt, d):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort(arr, low, k, 1)  # Sort first half in ascending orderasc
        bitonic_sort(arr, low + k, k, 0)  # Sort second half in descending order
        bitonic_merge(arr, low, cnt, d)  # Merge the entire sequence

# Function to read, sort, and write mobile data
def sort_mobile_data():
    start_time = time.time()
    try:
        # Read the CSV file
        with open("Updated_Mobile_Dataset.csv", encoding="utf-8") as file:
            data = list(csv.DictReader(file))
        if not data or "TotalReviews" not in data[0]:
            raise ValueError("Column 'TotalReviews' not found.")
        
        # Convert TotalReviews column to integer values
        for row in data: row["TotalReviews"] = int(row["TotalReviews"].replace(",", "").strip() or 0)
        
        # Get sorting order from user
        order = input("Sort by total reviews (asc/desc): ").strip().lower()
        if order not in {"asc", "desc"}: return print("Invalid input! Use 'asc' or 'desc'.")
        
        # Pad array size to next power of 2 for Bitonic sort
        n = len(data)
        pow2 = 1 << (math.ceil(math.log2(n)))
        data.extend([{ "TotalReviews": float('inf') }] * (pow2 - n))
        
        # Perform bitonic sort
        bitonic_sort(data, 0, len(data), order == "asc")
        
        # Remove padding
        data = [x for x in data if x["TotalReviews"] != float('inf')]
        
        # Write sorted data to a new CSV file
        with open("SortedDataset.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader(), writer.writerows(data)
        
        print("Dataset sorted successfully! Saved as SortedDataset.csv")
    except Exception as e:
        print(f"Error: {e}")
    
    # Display execution time
    print(f"Execution time: {time.time() - start_time:.4f} seconds")

if __name__ == "__main__":
    sort_mobile_data()
