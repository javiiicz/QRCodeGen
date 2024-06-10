def pad_zeroes_left(string, length):
    if length <= len(string):
        return string

    padding = (length - len(string)) * "0"
    string = padding + string
    return string


def pad_zeroes_right(string, length):
    if length <= len(string):
        return string

    padding = (length - len(string)) * "0"
    string = string + padding
    return string


# Separate in groups of k
def splice(string, k):
    groups = []
    for i in range(0, len(string), k):
        groups.append(string[i:i + k])
    return groups


# Interleave numbers
def loop(codewords):
    res = []
    if len(codewords["g2"]):
        max_i = max(len(codewords["g1"][0]), len(codewords["g2"][0]))
    else:
        max_i = len(codewords["g1"][0])

    for i in range(max_i):
        for group in codewords:
            for block in codewords[group]:
                if i >= len(block):
                    continue

                res.append(block[i])

    return res


# Make all possible pairs (with repeats) from given list
def get_pairs(nums):
    pair_num = len(nums) ** 2
    res = [[] for _ in range(pair_num)]

    for i, num1 in enumerate(nums):
        for j in range(len(nums)):
            res[(i * len(nums)) + j].append(num1)

    for i in range(len(res)):
        res[i].append(nums[i % len(nums)])

    return res


# Scores a QR code
def score(matrix):
    total = 0
    total += cond1(matrix)
    total += cond2(matrix)
    total += cond3(matrix)
    total += cond4(matrix)
    return total


def cond1(matrix):
    total = 0

    curr_run_x = 1
    prev_x = None

    curr_run_y = 1
    prev_y = None

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            bit_x = matrix[i][j]
            if bit_x == prev_x:
                curr_run_x += 1
            else:
                curr_run_x = 1
            prev_x = bit_x

            if curr_run_x == 5:
                total += 3
            elif curr_run_x >= 5:
                total += 1

            bit_y = matrix[j][i]
            if bit_y == prev_y:
                curr_run_y += 1
            else:
                curr_run_y = 1
            prev_y = bit_y

            if curr_run_y == 5:
                total += 3
            elif curr_run_y >= 5:
                total += 1

    return total


def cond2(matrix):
    blocks = 0

    for i in range(len(matrix) - 1):
        for j in range(len(matrix) - 1):
            square = 0
            square += matrix[i][j]
            square += matrix[i + 1][j]
            square += matrix[i][j + 1]
            square += matrix[i + 1][j + 1]

            if square == 0 or square == 4:
                blocks += 1

    return blocks * 3


def cond3(matrix):
    total = 0
    patterns = ["10111010000", "00001011101"]
    for i in range(len(matrix)):
        for j in range(len(matrix) - 10):
            string_x = ""
            string_y = ""
            for k in range(11):
                string_x += str(matrix[i][j + k])
                string_y += str(matrix[j + k][i])
            if string_x == patterns[0] or string_x == patterns[1]:
                total += 40
            if string_y == patterns[0] or string_y == patterns[1]:
                total += 40
    return total
                


def cond4(matrix):
    total = 0
    dark = 0

    for row in matrix:
        for col in row:
            total += 1
            if col == 1:
                dark += 1

    percent = dark / total * 100
    percent = int(percent)

    prev = percent - (percent % 5)
    follow = percent + (5 - (percent % 5))

    prev, follow = abs(prev - 50) // 5, abs(follow - 50) // 5

    return min(prev, follow) * 10


def format_print_qr(matrix):
    for row in matrix:
        for col in row:
            if col is None:
                print("_", end="")
            elif col == 1:
                print("⬛ ", end="")
            elif col == 2:
                print("r", end="")
            else:
                print("██", end="")
        print("")
