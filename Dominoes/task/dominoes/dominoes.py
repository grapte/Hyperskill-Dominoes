# Write your code here
import itertools
import random
import collections

doubles = {(i, i) for i in range(7)}
while True:
    stock = set(itertools.combinations(range(7), 2)) | doubles

    player = set(random.sample(list(stock), 7))
    stock = stock - player

    computer = set(random.sample(list(stock), 7))
    stock = stock - computer

    if stock >= doubles:
        continue
    else:
        break

max_double = max((computer | player) & doubles)

if max_double in player:
    status = "computer"
else:
    status = "player"

player = player - {max_double}
computer = computer - {max_double}

snake = [max_double]


def game_stat():
    print(f"Stock pieces {[list(e) for e in stock]}")
    print(f"Computer pieces {[list(e) for e in computer]}")
    print(f"Player pieces {[list(e) for e in player]}")
    print(f"Domino snake {[list(e) for e in snake]}")
    print(f"Status {status}")


player = list(player)
computer = list(computer)
stock = list(stock)
random.shuffle(stock)
while True:
    # game_stat()
    print("======================================================================")
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}")
    if len(snake) < 7:
        print("\n%s\n" % ''.join(f"{list(e)}" for e in snake))
    else:
        print("\n%s...%s\n" % (''.join(f"{list(e)}" for e in snake[:3]),
                               ''.join(f"{list(e)}" for e in snake[-3:])))
    print("Your pieces:")
    for i, e in enumerate(player):
        print(f"{i+1}: {list(e)}")
    print()
    match status:
        case "computer":
            print("Status: Computer is about to make a move. Press Enter to continue...")
        case "player":
            print("Status: It's your turn to make a move. Enter your command.")
    while True:
        move = input()
        l, r = snake[0][0], snake[-1][1]
        match status:
            case "computer":
                if move != '':
                    print("Invalid input. Please try again.")
                    continue
                valid = [(pl, pr) for pl, pr in computer if pr in (l, r) or pl in (l, r)]
                if not valid:
                    # bug: previous stage didn't check if the stock is empty
                    if len(stock) != 0:
                        computer.append(stock.pop())
                else:
                    play = random.choice(valid)
                    pl, pr = play
                    if l == pl:
                        snake.insert(0, (pr, pl))
                    elif l == pr:
                        snake.insert(0, play)
                    elif r == pl:
                        snake.append(play)
                    else:  # r == pr:
                        snake.append((pr, pl))
                    computer.remove(play)

            case "player":
                try:
                    move = int(move)
                except ValueError:
                    print("Invalid input. Please try again.")
                    continue
                if -len(player) > move or move > len(player):
                    print("Invalid input. Please try again.")
                    continue
                if move == 0:
                    # bug: previous stage didn't check if the stock is empty
                    if len(stock) != 0:
                        player.append(stock.pop())
                else:
                    idx = abs(move) - 1
                    play = player[idx]
                    pl, pr = play
                    if l == pl:
                        snake.insert(0, (pr, pl))
                    elif l == pr:
                        snake.insert(0, play)
                    elif r == pl:
                        snake.append(play)
                    elif r == pr:
                        snake.append((pr, pl))
                    else:
                        print("Illegal move. Please try again.")
                        continue
                    del player[idx]

        status = "computer" if status == "player" else "player"
        break

    if len(player) == 0:
        print("Status: The game is over. You won!")
        break
    elif len(computer) == 0:
        print("Status: The game is over. The computer won!")
        break
    counts = collections.Counter([n for pair in snake for n in pair])  # flatten pairs
    break_to_exit = False
    for k, v in counts.items():
        if v > 8 and l == r:
            print("Status: The game is over. It's a draw!")
            break_to_exit = True
            break
    if break_to_exit:
        break
