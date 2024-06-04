from Tables import Tables

class Message:
    def __init__(self, plaintext, level = "L"):
        self.plaintext = plaintext
        self.mode = ""
        self.level = level
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
        pass
    
# Step 3: Error Correction

# Step 4: Structure Final Message

# Step 5: Module Placement in Matrix

# Step 6: Data Masking

# Step 7: Format and Version Information