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
            if char not in Tables.kanji:
                modes["kanji"] = 0

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
        characters = len(self.plaintext)
        lookup = Tables.versions
        ec_level = {"L": 0, "M": 1, "Q": 2, "H": 3}.get(self.level)
        mode = {"numeric": 0, "alphanumeric": 1, "byte": 2, "kanji": 3}.get(self.mode)

        if ec_level is None or mode is None:
            raise Exception("Mode or Error Correction Level not determined.")

        for i in range(40):
            if lookup[i][ec_level][mode] >= characters:
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
        padding = (count_indicator_len - len(count)) * "0"
        indicator = padding + count
        self.bits += indicator

# Step 3: Error Correction

# Step 4: Structure Final Message

# Step 5: Module Placement in Matrix

# Step 6: Data Masking

# Step 7: Format and Version Information
