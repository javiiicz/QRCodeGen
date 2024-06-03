from charTables import Tables

class Message:
    def __init__(self, plaintext):
        self.plaintext = plaintext
        self.mode = ""
    
    # Step 1: Data Analysis
    # Analyze the types of characters used in the message and get the best mode for encoding. 
    # (numeric, alphanumeric, byte, kanji)
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

# Step 3: Error Correction

# Step 4: Structure Final Message

# Step 5: Module Placement in Matrix

# Step 6: Data Masking

# Step 7: Format and Version Information