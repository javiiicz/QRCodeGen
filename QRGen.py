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
    def errorCLevel(self, level):
        if level in ["L", "M", "Q", "H"]:
            self.level = level
            
    def determineVersion(self):
        characters = len(self.plaintext)
        lookup = Tables.versions
        ecLevel = {"L": 0, "M": 1, "Q": 2, "H": 3}.get(self.level)
        mode = {"numeric": 0, "alphanumeric": 1, "byte": 2, "kanji": 3}.get(self.mode)
        
        if ecLevel is None or mode is None:
            raise Exception("Mode or Error Correction Level not determined.")
        
        for i in range(40):
            if lookup[i][ecLevel][mode] >= characters:
                self.version = i + 1
                return
        
        raise Exception("String is too big, no version can fit it.")
    
# Step 3: Error Correction

# Step 4: Structure Final Message

# Step 5: Module Placement in Matrix

# Step 6: Data Masking

# Step 7: Format and Version Information
