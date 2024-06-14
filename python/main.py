from QRGen import Message


def main():
    is_valid = False
    string = input("Please enter the message to be encoded: ")
    ec = ""
    while not is_valid:
        ec = input(
            "Choose error correction level:\n(0) L 'Low'          | 7% of data can be recovered\n(1) M 'Medium'"
            "| 15% of data can be recovered\n(2) Q 'Quartile'     | 25% of data can be recovered\n(3) H 'High'"
            " | 30% of data can be recovered\n")
        if ec in {"0", "1", "2", "3"}:
            is_valid = True
            ec = {"0": "L", "1": "M", "2": "Q", "3": "H"}.get(ec)
        else:
            print("Character not valid")

    m = Message(string, ec)
    m.create_image()

    print(f"Success!\nMode: {m.mode} | Version: {m.version} | Level: {m.level}")
    print("Code saved in images/code.png")


if __name__ == "__main__":
    main()
