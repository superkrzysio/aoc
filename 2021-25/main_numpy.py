import time
import numpy
from matplotlib import pyplot as plt
import matplotlib.cm as cm

# "running fast" version, optimized and animated

def create_board(file):
    with open(file, "r") as fp:
        txtboard = fp.readlines()

    board = numpy.ndarray([len(txtboard), len(txtboard[0].strip())], dtype=numpy.uint8)

    mapping = {".": 0, ">": 1, "v": 2}

    for y in range(len(txtboard)):
        row = txtboard[y].strip()
        for x in range(len(row)):
            board[y,x] = mapping[row[x]]
    return board


def board_step(board):
    [height, width] = board.shape
    moved_anything = False
    for herd in [1, 2]:
        cucumbers = numpy.where(board == herd)
        target_cucumbers = []
        if herd == 2:
            target_cucumbers = (cucumbers[0]+1, cucumbers[1])
            target_cucumbers[0][target_cucumbers[0] >= height] = 0  # wrap around
        if herd == 1:
            target_cucumbers = (cucumbers[0], cucumbers[1]+1)
            target_cucumbers[1][target_cucumbers[1] >= width] = 0

        # limit cucumbers only to those who have empty target_cucumbers and will move
        empty = numpy.where(board == 0)
        empty = list(zip(*empty))
        target_cucumbers = list(zip(*target_cucumbers))

        # this is not optimal, takes 700ms for sample aoc data
        # movable_cucumbers = [index for index in range(len(target_cucumbers)) if target_cucumbers[index] in empty]

        # transform array of tuples into array of hashcodes to avoid searching by tuple
        empty_hashes = numpy.array(list(map(lambda x: x[0] + 2**16*x[1], empty)))
        target_hashes = numpy.array(list(map(lambda x: x[0] + 2**16*x[1], target_cucumbers)))

        # despite working on integers, this is still slow
        # movable_cucumbers = [index for index in range(len(target_cucumbers)) if target_cucumbers[index] in empty]

        # blazing fast!
        # intersect and fetch indexes
        movable_cucumbers = numpy.intersect1d(target_hashes, empty_hashes, return_indices=True, assume_unique=True)[1]
        if len(movable_cucumbers) == 0:
            continue

        cucumbers = list(zip(*cucumbers))
        cucumbers = list(map(lambda x: cucumbers[x], movable_cucumbers))
        target_cucumbers = list(map(lambda x: target_cucumbers[x], movable_cucumbers))
        cucumbers = list(zip(*cucumbers))
        cucumbers = (numpy.array(cucumbers[0]), numpy.array(cucumbers[1]))  # clumsy
        target_cucumbers = list(zip(*target_cucumbers))
        target_cucumbers = (numpy.array(target_cucumbers[0]), numpy.array(target_cucumbers[1]))

        # move
        time.time()
        board[cucumbers] = 0
        board[target_cucumbers] = herd
        moved_anything = True

    return moved_anything


def display_board(board):
    plt.clf()
    plt.imshow(board, cm.get_cmap("Spectral"), interpolation='nearest')
    plt.show(block=False)
    plt.pause(0.001)


MAX_FPS = 20

max_frame_interval = 1/MAX_FPS
last_frame = time.time()

board = create_board("input2.txt")

board_active = True
while board_active:
    # fps handling
    this_frame_time = time.time() - last_frame
    if max_frame_interval - this_frame_time > 0:
        time.sleep(max_frame_interval - this_frame_time)
    last_frame = time.time()

    display_board(board)

    board_active = board_step(board)

plt.pause(10)
