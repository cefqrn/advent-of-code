from re import compile

quintuple = compile(r"(.)\1{4,}")
triple = compile(r"(.)\1{2,}")

print(quintuple.search("asdghfaksjdaaaaafbbbbbh").group(1))