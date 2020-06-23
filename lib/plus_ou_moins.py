import numpy as np
import matplotlib.pyplot as plt


def create_pack(color):

    card_number = np.arange(0, 13).tolist()
    pack = []

    for col in color:
        for i in card_number:

            pack.append([col, i])

    return pack


def shuffle_pack(a_pack):

    for i in range(1000):

        j = int(np.random.randint(0, 52, 1))
        k = int(np.random.randint(0, 52, 1))
        a_pack[j], a_pack[k] = a_pack[k], a_pack[j]

    return a_pack


def begin_game(board_size=5):

    global normal_pack, shuffled_pack

    border = True
    board = []

    while border:

        board = []
        for i in range(board_size):
            card_to_add = shuffled_pack.pop(-1)
            board.append(card_to_add)

        border = check_border(board)

        if border:
            shuffled_pack = shuffle_pack(normal_pack.copy())
    return board


def check_border(board):

    border = False

    for card in board:

        if card[1] == (0 or 12):

            border = True

    return border


def new_turn(board, index_board):

    global shuffled_pack

    decision = plus_ou_moins(board[index_board][1])
    new_card = shuffled_pack.pop(-1)
    win_or_loose_bool = check_decision(decision, new_card[1], board[index_board][1])
    board[index_board] = new_card

    return win_or_loose_bool, board


def plus_ou_moins(card_number, best_choice=6):
    #
    # if card_number > best_choice:
    #
    #     my_dec = "moins"
    #
    # elif card_number <= best_choice:
    #
    #     my_dec = "plus"

    my_dec = "egalité"

    return my_dec


def check_decision(choice, n_number, o_number):


    # if o_number < n_number and choice == "plus":
    #
    #     win = True
    #
    # elif o_number > n_number and choice == "moins":
    #
    #     win = True

    if o_number == n_number and choice == "egalité":

        win = True
    else:

        win = False

    return win


ref = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "V", "D", "R", "A"]
couleur = ["trefle", "coeur", "pique", "carreaux"]

all_sips = []

for i in range(5000):
    sips = 0
    i_board = 0
    normal_pack = create_pack(couleur)
    shuffled_pack = shuffle_pack(normal_pack.copy())
    board = begin_game()

    while i_board != 5:
        # print(board)
        if len(shuffled_pack) == 0:
            shuffled_pack = shuffle_pack(normal_pack.copy())

        W_L, board = new_turn(board, i_board)
        if W_L:
            # print("Correct !")
            break
            # i_board += 1

        else:
            # print("Wrong !")
            sips += (i_board + 1)
            # print(sips)
            i_board = 0

        if sips == 0 and i_board == 5:

            i_board = 0

    all_sips.append(sips)


plt.hist(all_sips, bins=20)
mean_value = np.array(all_sips).mean()
my_max = np.array(all_sips).max()
plt.title("Nombre de partie joué : 5000, nombre moyen de gorgé: {:2} ".format(mean_value) + ", nombre de gorgé max: {}".format(my_max))
plt.ylabel("Occurence de ce nombre de gorgé bu")
plt.xlabel("Nombre de gorgé bu")
plt.show()