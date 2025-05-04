import heapq

def load_graph_and_heuristic(filename, city_map):

    heuristic = {}
    graph = {}

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            city_code = city_map.get(parts[0])
            if city_code is None:
                continue

            heuristic[city_code] = int(parts[1])
            neighbors = {
                city_map[parts[i]]: int(parts[i + 1])
                for i in range(2, len(parts), 2) if i + 1 < len(parts) and parts[i] in city_map
            }

            graph[city_code] = neighbors

    return graph, heuristic


def A_star_Search(acost, hval, start, end):

    a_star_list = []
    heapq.heappush(a_star_list, (hval[start], 0, start, [start]))
    visited = {start: 0}

    while a_star_list:
        f_current, g_current, current, path = heapq.heappop(a_star_list)

        if current == end:
            print("Path:"," -> ".join(path))
            print("Total distance:", g_current, "Km")
            return

        if g_current > visited.get(current, float('inf')):
            continue

        for neighbor, distance in acost[current].items():
            tentative_g = g_current + distance
            if neighbor not in visited or tentative_g < visited[neighbor]:
                visited[neighbor] = tentative_g
                f_score = tentative_g + hval[neighbor]
                heapq.heappush(a_star_list, (f_score, tentative_g, neighbor, path + [neighbor]))

    return "No path found"


def run_a_star_search(filename):

    city_map = {
        'Arad': 'A', 'Bucharest': 'Z', 'Craiova': 'S', 'Eforie': 'T', 'Fagaras': 'O',
        'Dobreta': 'V', 'Hirsova': 'N', 'lasi': 'Q', 'Neamt': 'F', 'Oradea': 'B',
        'Pitesti': 'P', 'RimnicuVilcea': 'R', 'Timisoara': 'C', 'Urziceni': 'D',
        'Vaslui': 'H', 'Zerind': 'E', 'Lugoj': 'G', 'Mehadia': 'L', 'Sibiu': 'I', 'Giurgiu': 'M'
    }

    start_node = input("Enter start city: ")
    goal_node = input("Enter goal city: ")

    if start_node not in city_map or goal_node not in city_map:
        print("Invalid city name. Please try again.")
        return

    graph, heuristic = load_graph_and_heuristic(filename, city_map)
    start_code = city_map[start_node]
    goal_code = city_map[goal_node]

    A_star_Search(graph, heuristic, start_code, goal_code)



input_file = "input.txt"
run_a_star_search(input_file)
