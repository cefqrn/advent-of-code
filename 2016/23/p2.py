from sys import argv

def main(argc: int, argv: list[str]):
    if argc != 2:
        return 1

    try:
        a = int(argv[1])
    except ValueError:
        return 1
    
    with open(0) as f:
        data = f.readlines()

    code = [f"LABEL{i}:"]
    for line in data:
        c
    
    with open("code.c", "w") as f:
        f.write(
            "#include <stdio.h>\n"
            "int main() {"
            "int a, b, c, d;"
            f"a = {a};"
            "b = c = d = 0;"
            "LABEL0:"
            "}"
        )
    
    return 0
    

if __name__ == "__main__":
    raise SystemExit(main(len(argv), argv))