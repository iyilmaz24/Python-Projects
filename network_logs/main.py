import sys
from collections import defaultdict
import heapq

def read_file(file_name):
    try:
        lines = [] 
        as_edges = []
        graph = defaultdict(set)
        
        with open(file_name, 'r') as file:
            for line in file: 
                lines.append(line.split("|"))
                
            for arr in lines:
                as_edges.append(arr[6].split(" "))
            
            for arr in as_edges:
                for i in range (1, len(arr)):
                    if arr[i][0] == "[":
                        break
                    
                    if arr[i-1] != arr[i]:
                        graph[arr[i-1]].add(arr[i])
                        graph[arr[i]].add(arr[i-1])
            
            heap = []
            for key in graph:
                heapq.heappush(heap, (-len(graph[key]), int(key)))
            
            with open("neighbor_count.txt", "w") as neigh_count, open("top10.txt", "w") as top10:
                i = 0
                while heap:
                    item = heapq.heappop(heap)
                    if i < 10:
                        neighbors = sorted([int(num) for num in graph[str(item[1])]])
                        adj_string = ""
                        for neighbor in neighbors:
                            adj_string += str(neighbor) + "|"
                        adj_string = adj_string[:-1]
                        top10.write(f"{item[1]}: {-item[0]} {adj_string}\n")
                        i += 1
                    neigh_count.write(f"{item[1]}: {-item[0]}\n")
                
                        
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    file_name = sys.argv[1]
    
    read_file(file_name)

if __name__ == "__main__":
    main()
