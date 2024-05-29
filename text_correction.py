from openai import OpenAI

from env import OPENAI_API_KEY

SIMULATE = False

def correct_text(text, client):
    prompt = """
        You are a writing assistant that corrects pieces of text written
        in LaTeX, you always reply with just the corrected text, no explanations
        or other description. You focus on spelling, layout, grammar
        and only if highly advised, small improvements to clarity and word choice.
        You never, under no circumstances, change the meaning of the text
        or replace latex commands.
    """
    # remove \n, multiple spaces and leading spaces
    prompt = " ".join(prompt.split())

    text = text.strip()

    if SIMULATE:
        return text

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content

def correct_file_line_by_line(path, client, out=None):
    out = out or path + "_corr"

    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    corrected_lines = []
    for line in lines:
        if len(line.strip()) < 20:
            corrected_lines.append(line)
            continue

        if line.startswith("%"):
            corrected_lines.append(line)
            continue

        excludeds = "begin, end, label, includegraphics, todo".split(",")
        excludeds = [f"\\{ex.strip()}" for ex in excludeds]
        if any([line.strip().startswith(ex) for ex in excludeds]):
            corrected_lines.append(line)
            continue

        print(line)
        corr = correct_text(line, client)
        # add back trailing spaces, ending newline
        prefix = line[:len(line)-len(line.lstrip())]
        corrected_lines.append(prefix + corr + "\n")
    
    with open(out, "w", encoding="utf-8") as file:
        file.writelines(corrected_lines)

if __name__ == "__main__":
    client = OpenAI(api_key=OPENAI_API_KEY)

    correct_file_line_by_line(
        r"D:\git\mathesis\latex\chapters\1introduction.tex",
        client,
        out = r"D:\git\mathesis\latex\chapters\1introduction_corr.tex"
    )

    # git diff --no-index --word-diff=color --word-diff-regex=. <file1> <file2>