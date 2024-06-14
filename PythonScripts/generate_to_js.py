from sys import argv
from QRGen import Message


def generate():
    if len(argv) <= 1:
        print("Please provide the message as an argument and an (optional) error correction level.")
        return

    string = argv[1]
    ec = "L"

    if len(argv) == 3:
        ec = argv[2]
        if ec not in {"L", "M", "Q", "H"}:
            print("Please provide a valid error correction level.")

    m = Message(string, ec)

    print(f"Success!\nMode: {m.mode} | Version: {m.version} | Level: {m.level}")
    print("Code saved in images/code.png")


if __name__ == "__main__":
    generate()
