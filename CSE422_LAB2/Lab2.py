import random

def read_input(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    
    initial_capital = int(lines[0].split("=")[1].strip())
    price_data = lines[1].split("=")[1].strip().strip("[]")
    historical_prices = []
    for num_str in price_data.split(","):
        final_num = num_str.strip()
        historical_prices.append(float(final_num))
    
    in_population = []
    for line in lines[2:]:
        if line.startswith("{"):
            parts = line.strip("{} \n").split(", ")
            chromosome = {}
            for part in parts:
                key, value = part.split(": ")
                chromosome[key.strip('"')] = float(value) if "." in value else int(value)
            in_population.append(chromosome)
    
    return initial_capital, historical_prices, in_population


def chromosome_to_string(chromosome):
    stop_loss = f"{chromosome['stop_loss']:.1f}" 
    take_profit = f"{chromosome['take_profit']:.1f}"  
    trade_size = f"{chromosome['trade_size']:.1f}"  
    return f"{stop_loss}|{take_profit}|{trade_size}"  

def str_to_chromosome(s):
    parts = s.split("|")  
    return {
        "stop_loss": float(parts[0]),
        "take_profit": float(parts[1]),
        "trade_size": float(parts[2])
    }

def calculate_fitness(chromosome, prices, initial_capital):
    capital = initial_capital
    for price_change in prices:
        
        trade_size = capital * (chromosome["trade_size"] / 100)
        
        if price_change <= -chromosome["stop_loss"]:
             capital -= trade_size * (chromosome["stop_loss"] / 100)
        elif price_change >= chromosome["take_profit"]:
            capital += trade_size * (chromosome["take_profit"] / 100)
        else:
            capital += trade_size * (price_change / 100)
    

    return capital - initial_capital


def crossover(parent1, parent2):
    parent1_str = chromosome_to_string(parent1)
    
    parent2_str = chromosome_to_string(parent2)
    
    p1_genes = parent1_str.split("|")
    
    p2_genes = parent2_str.split("|")
    
    point = random.randint(1, len(p1_genes) - 1)
    
   
    child1_genes = p1_genes[:point] + p2_genes[point:]
    child2_genes = p2_genes[:point] + p1_genes[point:]
    
    child1_str = "|".join(child1_genes)
    #print(child1_str)
    child2_str = "|".join(child2_genes)
    #print(child2_str)
    
    return str_to_chromosome(child1_str), str_to_chromosome(child2_str),point


def mutate(chromosome, mutation_rate=0.05, mutation_boundary=0.05):
   
    key_to_mutate = random.choice(list(chromosome.keys()))
    
    if random.random() < mutation_rate:
        mutation_amount = chromosome[key_to_mutate] * mutation_boundary
        
        
        if random.choice([True, False]):
            chromosome[key_to_mutate] += mutation_amount  
        else:
            chromosome[key_to_mutate] -= mutation_amount  
        
        chromosome[key_to_mutate] = max(1, min(99, chromosome[key_to_mutate]))
    
    return chromosome


def genetic_algorithm(initial_capital, historical_prices, population, generations=10):
    for generation in range(generations):
        
        
        fitness_scores = [calculate_fitness(chromosome, historical_prices, initial_capital) for chromosome in population]
        
        parents = random.sample(population, 2)
        
        child1, child2, point = crossover(parents[0], parents[1])
        
        child1 = mutate(child1)
        child2 = mutate(child2)
        
        best_chromosome = population[fitness_scores.index(max(fitness_scores))]
        new_population = [best_chromosome, child1, child2]
        

        new_population.append(generate_chromosome())
        
        population = new_population
    
    best_chromosome = max(population, key=lambda x: calculate_fitness(x, historical_prices, initial_capital))
    return best_chromosome

def generate_chromosome():
    stop_loss = round(random.uniform(1, 99), 1)  
    take_profit = round(random.uniform(1, 99), 1)  
    trade_size = round(random.uniform(1, 99), 1)  
    return {"stop_loss": stop_loss, "take_profit": take_profit, "trade_size": trade_size}


initial_capital, historical_prices, population = read_input("Lab-2 input.txt")


best_strategy = genetic_algorithm(initial_capital, historical_prices, population, generations=10)
print("\nBest Strategy:", best_strategy)




#######################PART 2######################


def two_point_crossover(parent1, parent2):
    child1, child2, point1 = crossover(parent1, parent2)
    f_child1, f_child2, point2 = crossover(child1, child2)
    #print(point1,point2)
    return f_child1, f_child2
 
initial_capital, historical_prices, population = read_input("Lab-2 input.txt")

parent1 = random.choice(population)
parent2 = random.choice(population)

child1, child2 = two_point_crossover(parent1, parent2)


print("Parent 1:", parent1)
print("Parent 2:", parent2)
print("Child 1:", child1)
print("Child 2:", child2)
