from Tables import Tables
from Polynomials import Polynomial, to_exp
from Patterns import Patterns
from Helpers import *
from copy import deepcopy
from PIL import Image


class Message:
    def __init__(self, plaintext, level="L"):
        self.plaintext = plaintext
        self.mode = ""
        self.level = level
        self.version = 0
        self.bits = ""
        self.blocks = None
        self.ec_codewords = None
        self.final = []
        self.size = 0
        self.matrix = []
        self.data_matrix = []
    
    def create_qr_code(self):
        self.analyze()
        self.encode()
        self.generate_ec_codewords()
        self.strucutre_message()
        self.module_placement()
        self.mask_data()
        self.finalize_code()
        self.create_image()
        format_print_qr(self.matrix)

    #
    # Step 1: Data Analysis
    #
    def analyze(self):
        modes = {"numeric": 1, "alphanumeric": 1, "byte": 1, "kanji": 1}

        for char in self.plaintext:
            if char not in Tables.numeric:
                modes["numeric"] = 0
            if char not in Tables.alphanumeric:
                modes["alphanumeric"] = 0
            if char not in Tables.byte:
                modes["byte"] = 0
            # if char not in Tables.kanji:    Not going to be implemented for now...
            #     modes["kanji"] = 0

        for mode in modes:
            if modes[mode] == 1:
                self.mode = mode
                return

        raise Exception("No suitable mode found for the message.")

    #
    # Step 2: Data Encoding
    #
    def encode(self):
        self.determine_version()
        self.add_indicators()
        match self.mode:
            case "numeric":
                self.numeric_encode()
            case "alphanumeric":
                self.alphanumeric_encode()
            case "byte":
                self.byte_encode()
            case "kanji":
                self.kanji_encode()
            case _:
                raise Exception("Mode does not exist or has not been determined.")
        self.align_bytes()

    def set_errorc_level(self, level):
        if level in {"L", "M", "Q", "H"}:
            self.level = level

    def determine_version(self):
        lookup = Tables.versions
        ec_level = {"L": 0, "M": 1, "Q": 2, "H": 3}.get(self.level)
        mode = {"numeric": 0, "alphanumeric": 1, "byte": 2, "kanji": 3}.get(self.mode)

        if ec_level is None or mode is None:
            raise Exception("Mode or Error Correction Level not determined.")

        for i in range(40):
            if lookup[i][ec_level][mode] >= len(self.plaintext):
                self.version = i + 1
                return

        raise Exception("String is too big, no version can fit it.")

    def add_indicators(self):
        # Mode Indicator
        indicator = {"numeric": "0001", "alphanumeric": "0010", "byte": "0100", "kanji": "1000"}
        self.bits += indicator[self.mode]

        # Character Count Indicator
        count = str(bin(len(self.plaintext)))[2:]
        if self.version <= 9:
            padding_lookup = 0
        elif self.version <= 26:
            padding_lookup = 1
        else:
            padding_lookup = 2
        mode = {"numeric": 0, "alphanumeric": 1, "byte": 2, "kanji": 3}.get(self.mode)
        count_indicator_len = Tables.padding[padding_lookup][mode]
        self.bits += pad_zeroes_left(count, count_indicator_len)

    def numeric_encode(self):
        data = ""
        # Separate in groups of 3
        groups = splice(self.plaintext, 3)

        # Convert to binary
        for trio in groups:
            num = int(trio)
            binary = str(bin(num))[2:]
            if num > 99:
                length = 10
            elif num > 9:
                length = 7
            else:
                length = 4
            binary = pad_zeroes_left(binary, length)
            data += binary

        self.bits += data

    def alphanumeric_encode(self):
        data = ""
        # Separate in groups of 2
        groups = splice(self.plaintext, 2)

        # Covnert to binary
        for pair in groups:
            if len(pair) == 1:
                num = Tables.alphanumeric[pair]
                binary = str(bin(num))[2:]
                binary = pad_zeroes_left(binary, 6)
            else:
                first = Tables.alphanumeric[pair[0]]
                second = Tables.alphanumeric[pair[1]]
                num = (45 * first) + second
                binary = str(bin(num))[2:]
                binary = pad_zeroes_left(binary, 11)
            data += binary

        self.bits += data

    def byte_encode(self):
        data = ""
        for char in self.plaintext:
            binary = str(bin(ord(char)))[2:]
            binary = pad_zeroes_left(binary, 8)
            data += binary

        self.bits += data

    def kanji_encode(self):
        raise Exception("Kanji mode not implemented.")

    def align_bytes(self):
        # Add Terminator
        bits_necessary = self.determine_bits()
        diff = bits_necessary - len(self.bits)
        if diff > 4:
            self.bits = pad_zeroes_right(self.bits, len(self.bits) + 4)
        else:
            self.bits = pad_zeroes_right(self.bits, len(self.bits) + diff)

        # Make multiple of 8
        if len(self.bits) % 8 != 0:
            self.bits = pad_zeroes_right(self.bits, (8 - (len(self.bits) % 8)) + len(self.bits))

        # Add pad bytes
        pad_bytes = "1110110000010001"
        pad_bytes_needed = (bits_necessary - len(self.bits)) // 8
        if pad_bytes_needed % 2 == 0:
            self.bits += pad_bytes * (pad_bytes_needed // 2)
        else:
            self.bits += pad_bytes * ((pad_bytes_needed - 1) // 2)
            self.bits += pad_bytes[0:8]

    def determine_bits(self):
        ec_level = {"L": 0, "M": 1, "Q": 2, "H": 3}.get(self.level)
        return 8 * Tables.codewords[self.version - 1][ec_level][0]

    #
    # Step 3: Error Correction
    #
    def generate_ec_codewords(self):
        self.blocks = self.break_into_blocks()
        self.ec_codewords = self.get_division_remainder(self.blocks)

    def break_into_blocks(self):
        segments = {"g1": [], "g2": []}
        ec_level = {"L": 0, "M": 1, "Q": 2, "H": 3}.get(self.level)

        blocks_g1 = Tables.codewords[self.version - 1][ec_level][2]
        codewords_per_block_g1 = Tables.codewords[self.version - 1][ec_level][3]
        codewords_g1 = codewords_per_block_g1 * blocks_g1

        blocks_g2 = Tables.codewords[self.version - 1][ec_level][4]
        codewords_per_block_g2 = Tables.codewords[self.version - 1][ec_level][5]

        segments["g1"] = splice(self.bits[:codewords_g1 * 8], codewords_per_block_g1 * 8)
        if blocks_g2 != 0:
            segments["g2"] = splice(self.bits[codewords_g1 * 8:], codewords_per_block_g2 * 8)

        for group in segments:
            for i, block in enumerate(segments[group]):
                ints = splice(block, 8)

                for j, byte in enumerate(ints):
                    # Convert to integer value
                    ints[j] = eval("0b" + byte)

                segments[group][i] = ints

        return segments

    def get_division_remainder(self, blocks):
        ec_level = {"L": 0, "M": 1, "Q": 2, "H": 3}.get(self.level)
        ec_per_block = Tables.codewords[self.version - 1][ec_level][1]
        ec_codewords = {"g1": [], "g2": []}

        for group in blocks:
            for block in blocks[group]:
                # Alpha notation
                message_p = to_exp(block.copy())
                gen_p = Tables.gen_p[ec_per_block]

                # Expand message polynomial
                message_p += [None] * ec_per_block

                message_p = Polynomial(message_p)
                gen_p = Polynomial(gen_p)

                # Recall Message Polynomial is degree codewords_per_block + ec_codewords
                # Generator polynomial is degree ec_codewords
                ec_codewords[group].append(message_p.gf256_divide_by(gen_p))

        return ec_codewords

    #
    # Step 4: Structure Final Message
    #
    def strucutre_message(self):
        self.final += loop(self.blocks)
        self.final += loop(self.ec_codewords)

        # Binary Conversion
        self.bits = ""
        for n in self.final:
            binary = bin(n)
            binary = str(binary)[2:]
            binary = pad_zeroes_left(binary, 8)
            self.bits += binary

        # Add Remainder bits in required
        if self.version in range(2, 7):
            self.bits = pad_zeroes_right(self.bits, len(self.bits) + 7)
        elif (self.version in range(14, 21)) or (self.version in range(28, 35)):
            self.bits = pad_zeroes_right(self.bits, len(self.bits) + 3)
        elif self.version in range(21, 28):
            self.bits = pad_zeroes_right(self.bits, len(self.bits) + 4)

    #
    # Step 5: Module Placement in Matrix
    #
    def module_placement(self):
        self.create_matrix()
        self.add_finder_patterns()  # and separators
        self.add_alignment_patterns()
        self.add_timing_patterns()
        self.add_reserved_areas()  # and dark spot
        self.add_data()

    def create_matrix(self):
        self.size = ((self.version - 1) * 4) + 21
        self.matrix = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.data_matrix = [[None for _ in range(self.size)] for _ in range(self.size)]

    def add_finder_patterns(self):
        self.place_finder(0)
        self.place_finder(1)
        self.place_finder(2)

    def place_finder(self, kind):
        coords = {0: (0, 0), 1: (0, self.size - 8), 2: (self.size - 8, 0)}
        pattern = Patterns.finders[kind]
        row, col = coords[kind]
        self.place_pattern(pattern, row, col)

    def add_alignment_patterns(self):
        coords = Tables.locations[self.version - 1]

        if coords is None:
            return

        pairs = get_pairs(coords)
        good_pairs = []
        for i, pair in enumerate(pairs):
            if pair[0] <= 8 and pair[1] <= 8:
                continue
            elif pair[0] <= 8 and pair[1] >= (self.size - 8):
                continue
            elif pair[0] >= (self.size - 8) and pair[1] <= 8:
                continue
            good_pairs.append(pair)

        for pair in good_pairs:
            self.place_alignment(pair[0], pair[1])

    def place_alignment(self, row, col):
        # Convert to corner
        row, col = row - 2, col - 2
        pattern = Patterns.alignment
        self.place_pattern(pattern, row, col)

    def place_pattern(self, pattern, row, col):
        for i, r in enumerate(pattern):
            for j, c in enumerate(r):
                self.matrix[row + i][col + j] = pattern[i][j]

    def add_timing_patterns(self):
        bw = 1
        for i in range(8, self.size - 8):
            if bw:
                module = 1
                bw = 0
            else:
                module = 0
                bw = 1

            self.matrix[6][i] = module
            self.matrix[i][6] = module

    def add_reserved_areas(self):
        # Dark spot
        self.matrix[(4 * self.version) + 9][8] = 1

        # Format information
        for i in range(0, self.size):
            if i <= 8 or i >= self.size - 8:
                if self.matrix[8][i] is None:
                    self.matrix[8][i] = 2
                if self.matrix[i][8] is None:
                    self.matrix[i][8] = 2

        # Version information
        if self.version >= 7:
            for i in range(0, 6):
                end = self.size - 9
                self.matrix[i][end] = 2
                self.matrix[i][end - 1] = 2
                self.matrix[i][end - 2] = 2
                self.matrix[end][i] = 2
                self.matrix[end - 1][i] = 2
                self.matrix[end - 2][i] = 2

    def add_data(self):
        bits = self.bits
        up_direction = True
        last = 0  # 0: vert, 1: hor
        start = self.size - 1, self.size - 1

        i, j = start
        for bit in bits:
            while self.matrix[i][j] is not None:
                i, j, last, up_direction = self.find_next(i, j, last, up_direction)
            self.matrix[i][j] = int(bit)
            self.data_matrix[i][j] = int(bit)

    def find_next(self, row, col, last, up_direction):
        if up_direction:
            if last == 0:
                row, col = row, col - 1
                last = 1
            elif last == 1:
                row, col = row - 1, col + 1
                last = 0

            # Reached top, switch downwards
            if row < 0:
                row, col, last, up_direction = row + 1, col - 2, 0, False

        else:
            if last == 0:
                row, col = row, col - 1
                last = 1
            elif last == 1:
                row, col = row + 1, col + 1
                last = 0

            # Reached end
            if row == self.size:
                row, col, last, up_direction = row - 1, col - 2, 0, True

        if col == 6:
            col -= 1

        return row, col, last, up_direction

    #
    # Step 6: Data Masking
    #
    def mask_data(self):
        scores = {}
        for i in range(8):
            scores[i] = self.mask_and_score(i)
        best_mask = min(scores, key=scores.get)
        self.matrix = self.mask(best_mask)

    def mask_and_score(self, mask_num):
        matrix = self.mask(mask_num)
        return score(matrix)

    def mask(self, mask_num):
        data = deepcopy(self.data_matrix)
        match mask_num:
            case 0:
                for i, row in enumerate(data):
                    for j, col in enumerate(data[i]):
                        if col is None:
                            continue
                        if (i + j) % 2 == 0:
                            data[i][j] = col ^ 1
            case 1:
                for i, row in enumerate(data):
                    for j, col in enumerate(data[i]):
                        if col is None:
                            continue
                        if i % 2 == 0:
                            data[i][j] = col ^ 1
            case 2:
                for i, row in enumerate(data):
                    for j, col in enumerate(data[i]):
                        if col is None:
                            continue
                        if j % 3 == 0:
                            data[i][j] = col ^ 1
            case 3:
                for i, row in enumerate(data):
                    for j, col in enumerate(data[i]):
                        if col is None:
                            continue
                        if (i + j) % 3 == 0:
                            data[i][j] = col ^ 1
            case 4:
                for i, row in enumerate(data):
                    for j, col in enumerate(data[i]):
                        if col is None:
                            continue
                        if ((i // 2) + (j // 3)) % 2 == 0:
                            data[i][j] = col ^ 1
            case 5:
                for i, row in enumerate(data):
                    for j, col in enumerate(data[i]):
                        if col is None:
                            continue
                        if ((i * j) % 2) + ((i * j) % 3) == 0:
                            data[i][j] = col ^ 1
            case 6:
                for i, row in enumerate(data):
                    for j, col in enumerate(data[i]):
                        if col is None:
                            continue
                        if (((i * j) % 2) + ((i * j) % 3)) % 2 == 0:
                            data[i][j] = col ^ 1
            case 7:
                for i, row in enumerate(data):
                    for j, col in enumerate(data[i]):
                        if col is None:
                            continue
                        if (((i + j) % 2) + ((i * j) % 3)) % 2 == 0:
                            data[i][j] = col ^ 1
            case _:
                raise Exception("Mask Number must be in range(0,8)")

        matrix = deepcopy(self.matrix)
        for i, row in enumerate(data):
            for j, col in enumerate(data[i]):
                if col is not None:
                    matrix[i][j] = col

        matrix = self.add_format_bits(matrix, mask_num)
        return matrix

    #
    # Step 7: Format and Version Information
    #
    def add_format_bits(self, m, mask_num):
        ec_level = {"L": 0, "M": 1, "Q": 2, "H": 3}.get(self.level)
        format_string = Tables.format_strings[mask_num][ec_level]

        # Horizontal Format string
        for i in range(15):
            num = eval(format_string[i])
            if i <= 6:
                if i == 6:
                    m[8][i + 1] = num
                else:
                    m[8][i] = num
                m[self.size - 1 - i][8] = num
            else:
                m[8][self.size - 15 + i] = num
                if i <= 8:
                    m[14 - i + 1][8] = num
                else:
                    m[14 - i][8] = num

        # Version string
        if self.version >= 7:
            version_string = Tables.version_strings[self.version - 7]
            version_string = version_string[::-1]

            for i in range(0, 6):
                end = self.size - 9
                m[i][end - 2] = int(version_string[3 * i])
                m[i][end - 1] = int(version_string[(3 * i) + 1])
                m[i][end] = int(version_string[(3 * i) + 2])

                m[end - 2][i] = int(version_string[3 * i])
                m[end - 1][i] = int(version_string[(3 * i) + 1])
                m[end][i] = int(version_string[(3 * i) + 2])

        return m

    def finalize_code(self):
        matrix = [[0 for _ in range(self.size + 8)] for _ in range(self.size + 8)]
        for i in range(self.size):
            for j in range(self.size):
                matrix[i + 4][j + 4] = self.matrix[i][j]
        self.matrix = matrix
        
    
    #
    # 8: Create Image File
    #
    def create_image(self):
        side = self.size + 8
        image = Image.new('1', (side, side))
        
        pixels = image.load()
        
        for i in range(side):
            for j in range(side):
                pixels[j, i] = self.matrix[i][j] ^ 1
        
        image.show()
        image.save("examples/code.png")
