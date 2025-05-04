import random
#part-1
# File paths
input_network_file = "Lab-2 input.txt"
output_file_path = "Lab-2 output.txt"

# Function to read input from a file
def read_input_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    
    initial_capital = int(lines[0].split("=")[1].strip())
    historical_prices = list(map(float, lines[1].split("=")[1].strip().strip("[]").split(",")))
    
    initial_population = []
    for line in lines[2:]:
        if line.startswith("{"):
            parts = line.strip("{} \n").split(", ")
            chromosome = {}
            for part in parts:
                key, value = part.split(": ")
                chromosome[key.strip('"')] = float(value) if "." in value else int(value)
            initial_population.append(chromosome)
    
    return initial_capital, historical_prices, initial_population

# Function to write output to a file
def write_output_file(filename, best_strategy, final_profit, parents=None, child1=None, child2=None):
    with open(filename, "w") as file:
        # Best Strategy Output
        file.write(f'Best Strategy:\n')
        file.write(f'stop_loss = {best_strategy["stop_loss"]}\n')
        file.write(f'take_profit = {best_strategy["take_profit"]}\n')
        file.write(f'trade_size = {best_strategy["trade_size"]}\n')
        file.write(f'\nFinal Profit: {final_profit}\n')

        # Two-Point Crossover Output
        if parents and child1 and child2:
            file.write(f'\nParents: {parents}\n')
            file.write(f'1st child: {child1}\n')
            file.write(f'2nd child: {child2}\n')

# Chromosome representation functions
def chromosome_to_string(chromosome):
    return f"{int(chromosome['stop_loss']*10):02d}{int(chromosome['take_profit']*10):02d}{int(chromosome['trade_size']):02d}"

def string_to_chromosome(chromosome_str):
    return {
        "stop_loss": int(chromosome_str[:2]) / 10,
        "take_profit": int(chromosome_str[2:4]) / 10,
        "trade_size": int(chromosome_str[4:6])
    }

# Fitness function
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

# Read input parameters
initial_capital, historical_prices, population = read_input_file(input_network_file)


# Part 2 - Two-Point Crossover
# Select two random parents
parents = random.sample(population, 2)
parent1_str = chromosome_to_string(parents[0])
parent2_str = chromosome_to_string(parents[1])

# Ensure the two crossover points are valid
point1 = random.randint(1, 4)  # First crossover point (1-4)
point2 = random.randint(point1 + 1, 5)  # Second crossover point (must be after point1)

# Perform two-point crossover
child1_str = parent1_str[:point1] + parent2_str[point1:point2] + parent1_str[point2:]
child2_str = parent2_str[:point1] + parent1_str[point1:point2] + parent2_str[point2:]

best_chromosome = max(population, key=lambda x: calculate_fitness(x, historical_prices, initial_capital))
best_fitness = calculate_fitness(best_chromosome, historical_prices, initial_capital)
write_output_file(output_file_path, best_chromosome, best_fitness, parents=(parent1_str, parent2_str), child1=child1_str, child2=child2_str)

#print("Best strategy and crossover results saved to Lab-1 output.txt")
