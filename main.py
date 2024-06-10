from QRGen import Message

def main():
    string = input("Please enter the message you wish to be encoded: ")
    
    isValid = False
    while not isValid:
        ec = input("Choose error correction level:\n(0) L 'Low'          | 7% of data can be recovered\n(1) M 'Medium'       | 15% of data can be recovered\n(2) Q 'Quartile'     | 25% of data can be recovered\n(3) H 'High'         | 30% of data can be recovered\n")
        if ec in {"0", "1", "2", "3"}:
            isValid = True
            ec = {"0": "L", "1": "M", "2": "Q", "3": "H"}.get(ec)
        else:
            print("Character not valid")
    
    m = Message(string, ec)
    
    print(f"Success!\nMode: {m.mode} | Version: {m.version} | Level: {m.level}")
    print("Code saved in images/code.png")

if __name__ == "__main__":
    main()