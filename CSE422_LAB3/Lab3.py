####Problem 1#####
import math
import random


def strength(x):
    return math.log2(x + 1) + x / 10


def utility(maxValue, minValue):
    i = random.randint(0, 1)
    rand_val = random.randint(1, 10)
    return round(strength(maxValue) - strength(minValue) + ((-1) ** i) * (rand_val / 10), 2)


def minmax(depth, maximizing, alpha, beta, maxValue, minValue):
    if depth == 0:
        return utility(maxValue, minValue)

    if maximizing:
        max_score = float('-inf')
        for i in range(2):
            value = minmax(depth - 1, False, alpha, beta, maxValue, minValue)
            max_score = max(max_score, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return max_score
    else:
        min_score = float('inf')
        for _ in range(2):  # karon possible branch 2 ta hote parbe
            value = minmax(depth - 1, True, alpha, beta, maxValue, minValue)
            min_score = min(min_score, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return min_score


def chess_games():
    print("Enter (0 for Carlsen, 1 for Caruana): ", end="")
    start_player = int(input())
    print("Enter base strength for Carlsen: ", end="")
    carlsen_strength = float(input())
    print("Enter base strength for Caruana: ", end="")
    caruana_strength = float(input())

    carlsen_wins = caruana_wins = draws = 0

    for i in range(4):
        if (i + start_player) % 2 == 0:
            maxValue = carlsen_strength
            minValue = caruana_strength
            max_name = "Magnus Carlsen"
            min_name = "Fabiano Caruana"
        else:
            maxValue = caruana_strength
            minValue = carlsen_strength
            max_name = "Fabiano Caruana"
            min_name = "Magnus Carlsen"

        result = minmax(5, True, float('-inf'), float('inf'), maxValue, minValue)

        if result > 0:
            print(f"Game {i + 1} Winner: {max_name} (Max) (Utility value: {result})")
            if "Carlsen" in max_name:
                carlsen_wins += 1
            else:
                caruana_wins += 1
        elif result < 0:
            print(f"Game {i + 1} Winner: {min_name} (Min) (Utility value: {result})")
            if "Carlsen" in min_name:
                carlsen_wins += 1
            else:
                caruana_wins += 1
        else:
            print(f"Game {i + 1} Winner: Draw (Utility value: {result})")
            draws += 1

    print("\nOverall Results:")
    print(f"Magnus Carlsen Wins: {carlsen_wins}")
    print(f"Fabiano Caruana Wins: {caruana_wins}")
    print(f"Draws: {draws}")

    if carlsen_wins > caruana_wins:
        print("Overall Winner: Magnus Carlsen")
    elif caruana_wins > carlsen_wins:
        print("Overall Winner: Fabiano Caruana")
    else:
        print("Overall Winner: Draw")



a = chess_games()







####################################PROBLEM 2#####################################


# import math
# import random
#
#
#
# def strength(x):
#     return math.log2(x + 1) + x / 10
#
#
# def utility(maxValue, minValue):
#     i = random.randint(0, 1)
#     rand_val = random.randint(1, 10)
#     return round(strength(maxValue) - strength(minValue) + ((-1) ** i) * (rand_val / 10), 2)
#
#
# # Helper
# def maximize_player_move(depth, alpha, beta, maxValue, minValue, is_max):
#     max_score = float('-inf')
#     for i in range(2):
#         value = minmax(depth - 1, not is_max, alpha, beta, maxValue, minValue)
#         max_score = max(max_score, value)
#         alpha = max(alpha, value)
#         if beta <= alpha:
#             break
#     return max_score
#
#
# def minmax(depth, is_maximizing, alpha, beta, maxValue, minValue):
#     if depth == 0:
#         return utility(maxValue, minValue)
#
#     if is_maximizing:
#         return maximize_player_move(depth, alpha, beta, maxValue, minValue, True)
#     else:
#         min_score = float('inf')
#         for i in range(2):
#             value = minmax(depth - 1, True, alpha, beta, maxValue, minValue)
#             min_score = min(min_score, value)
#             beta = min(beta, value)
#             if beta <= alpha:
#                 break
#         return min_score
#
#
#
# def magic(depth, is_max, alpha, beta, maxValue, minValue):
#     if depth == 0:
#         return utility(maxValue, minValue)
#
#     if is_max:
#         return maximize_player_move(depth, alpha, beta, maxValue, minValue, True)
#     else:
#
#         value1 = magic(depth - 1, True, alpha, beta, maxValue, minValue)
#         value2 = magic(depth - 1, True, alpha, beta, maxValue, minValue)
#         return max(value1, value2)
#
#
#
# def cheating_chess():
#     start = int(input("Enter who goes first (0 for Light, 1 for L): "))
#     cost = float(input("Enter the cost of using Mind Control: "))
#     light_strength = float(input("Enter base strength for Light: "))
#     l_strength = float(input("Enter base strength for L: "))
#
#     if start == 0:
#         maxValue, minValue = light_strength, l_strength
#         max_name = "Light"
#     else:
#         maxValue, minValue = l_strength, light_strength
#         max_name = "L"
#
#     without_result = minmax(5, True, float('-inf'), float('inf'), maxValue, minValue)
#     with_result = magic(5, True, float('-inf'), float('inf'), maxValue, minValue)
#     final_result = round(with_result - cost, 2)
#
#     print(f"Minimax value without Mind Control: {round(without_result, 2)}")
#     print(f"Minimax value with Mind Control: {round(with_result, 2)}")
#     print(f"Minimax value with Mind Control after incurring the cost: {final_result}")
#
#     if without_result > 0:
#         print(f"{max_name} should NOT use Mind Control as the position is already winning.")
#     elif final_result > without_result and final_result > 0:
#         print(f"{max_name} should use Mind Control.")
#     elif without_result < 0 and final_result < 0:
#         print(f"{max_name} should NOT use Mind Control as the position is losing either way.")
#     elif final_result < without_result and final_result < 0:
#         print(f"{max_name} should NOT use Mind Control as it backfires.")
#     elif final_result < without_result and final_result >= 0:
#         print(f"{max_name} should use Mind Control.")
#
#
# a= cheating_chess()