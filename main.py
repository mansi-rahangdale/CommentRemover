
def remove_comments(source):
    result = []
    i = 0
    n = len(source)

    while i < n:
        if source[i:i+2] == "//":
            while i < n and source[i] != "\n":
                i += 1

        elif source[i:i+2] == "/*":
            i += 2
            while i < n and source[i:i+2] != "*/":
                i += 1
            i = min(i + 2, n)

        else:
            result.append(source[i])
            i += 1

    return "".join(result)


with open("input.c", "r") as file:
    source_code = file.read()

clean_code = remove_comments(source_code)

with open("output.c", "w") as file:
    file.write(clean_code)

print("Comments removed!")
print("Clean code saved in output.c")
