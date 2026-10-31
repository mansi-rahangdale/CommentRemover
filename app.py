
from flask import Flask, render_template, request
import io
import tokenize

app = Flask(__name__)


def remove_c_comments(source):
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


def remove_python_comments(source):
    tokens = []
    lines = source.splitlines(keepends=True)

    try:
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type == tokenize.COMMENT:
                continue
            tokens.append(token)

        return tokenize.untokenize(tokens)

    except (tokenize.TokenError, IndentationError):
        return "Error: Invalid or incomplete Python code."


@app.route("/", methods=["GET", "POST"])
def home():
    input_code = ""
    output_code = ""
    language = "c"

    if request.method == "POST":
        input_code = request.form.get("code", "")
        language = request.form.get("language", "c")

        if language == "python":
            output_code = remove_python_comments(input_code)
        else:
            output_code = remove_c_comments(input_code)

    return render_template(
        "index.html",
        input_code=input_code,
        output_code=output_code,
        language=language
    )


if __name__ == "__main__":
    app.run(debug=True)
