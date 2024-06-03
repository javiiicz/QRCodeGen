class Tables:
    numeric = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    
    alphanumeric = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                       "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                       "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                       "U", "V", "W", "X", "Y", "Z", " ", "$", "%", "*",
                       "+", "-", ".", "/", ":"])
    
    # Follows ISO 8859-1
    byte = set([chr(i) for i in range(256)])
    
    kanji = set([chr(i) for i in range(0x8140, 0x9FFC)] + [chr(i) for i in range(0xE040, 0xEBBF)])
    
    
