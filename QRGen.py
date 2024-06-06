from Tables import Tables


class Message:
    def __init__(self, plaintext, level="L"):
        self.plaintext = plaintext
        self.mode = ""
        self.level = level
        self.version = 0
        self.bits = ""

    # Step 1: Data Analysis
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

    # Step 2: Data Encoding
    def errorc_level(self, level):
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
        self.bits += pad_zeroes(count, count_indicator_len)

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

    def numeric_encode(self):
        data = ""
        # Separate in groups of 3
        groups = []
        for i in range(0, len(self.plaintext), 3):
            groups.append(self.plaintext[i:i+3])

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
            binary = pad_zeroes(binary, length)
            data += binary

        self.bits += data

    def alphanumeric_encode(self):
        data = ""
        # Separate in groups of 2
        groups = []
        for i in range(0, len(self.plaintext), 2):
            groups.append(self.plaintext[i:i+2])

        # Covnert to binary
        for pair in groups:
            if len(pair) == 1:
                num = Tables.alphanumeric[pair]
                binary = str(bin(num))[2:]
                binary = pad_zeroes(binary, 6)
            else:
                first = Tables.alphanumeric[pair[0]]
                second = Tables.alphanumeric[pair[1]]
                num = (45 * first) + second
                binary = str(bin(num))[2:]
                binary = pad_zeroes(binary, 11)
            data += binary

        self.bits += data

    def byte_encode(self):
        data = ""
        for char in self.plaintext:
            binary = str(bin(ord(char)))[2:]
            binary = pad_zeroes(binary, 8)
            data += binary

        self.bits = data

    def kanji_encode(self):
        raise Exception("Kanji mode not implemented.")


# Step 3: Error Correction

# Step 4: Structure Final Message

# Step 5: Module Placement in Matrix

# Step 6: Data Masking

# Step 7: Format and Version Information


def pad_zeroes(string, length):
    if length <= len(string):
        return string

    padding = (length - len(string)) * "0"
    string = padding + string
    return string
