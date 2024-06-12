from glob import glob
import re

from openai import OpenAI

from env import OPENAI_API_KEY
import latexutils

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

    lines = latexutils.read_file(path)

    corrected_lines = []
    for line in lines:
        if not latexutils.contains_relevant_text(line):
            corrected_lines.append(line)
            continue

        print(line)
        corr = correct_text(line, client)
        # add back trailing spaces, ending newline
        prefix = line[:len(line)-len(line.lstrip())]
        corrected_lines.append(prefix + corr + "\n")

    latexutils.write_file(out, corrected_lines)

def summarize_text(text, client):
    prompt = """"
        You summarize the text you are given in a brief and concise manner,
        focus on the main points and the most important, interesting information
        that is relevant beyond the text itself. You never add new information.
    """
    prompt = " ".join(prompt.split())

    text = text.strip()

    if SIMULATE:
        return text
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content

def summarize_file(path, client, out=None):
    out = out or path + "_sum"

    lines = latexutils.read_file(path)
    lines = [line for line in lines if latexutils.contains_relevant_text(line)]
    lines = latexutils.reduce_tokens(lines)
    text = "".join(lines)
    summary = summarize_text(text, client)

    latexutils.write_file(out, summary, by_line=False)

def propose_abstract(paths, client, out=None):
    out = out or "abstract.tex"

    lines = []
    for path in paths:
        lines.extend(latexutils.read_file(path))
    lines = [line for line in lines if latexutils.contains_relevant_text(line)]
    lines = latexutils.reduce_tokens(lines)
    text = "".join(lines)

    latexutils.write_file("text.tex", text, by_line=False)

    prompt = """
        You are an advanced AI writing assistant that writes abstracts for
        papers and master theses. You communicate precise and clearly, do not
        exaggerate or sound too formal. You focus on the main points and are brief.
        Start your abstract in LaTeX code with \chapter*{Abstract}.
    """
    prompt = " ".join(prompt.split())

    print(f"Text has {len(text)} characters and {len(text.split())} words")
    print(paths)

    if SIMULATE:
        abstract = "This is an example abstract"
    else:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        )

        abstract = completion.choices[0].message.content

    latexutils.write_file(out, abstract, by_line=False)


if __name__ == "__main__":
    if not SIMULATE:
        client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        client = None

    task = 2

    files = glob(r"D:\git\mathesis\latex\chapters\*.tex")
    # extract those where name starts with a digit, these are the chapters
    files = [f for f in files if f.split("\\")[-1][0].isdigit()]
    files = sorted(files)

    if task == 0:
        for file in files:
            out = file[:-4] + "_corr.tex"
            correct_file_line_by_line(file, client, out=out)
        # git diff --no-index --word-diff=color --word-diff-regex=. <file1> <file2>

    elif task == 1:
        for file in (files[3:6] + files[1:2]):
            out = file[:-4] + ".tex_sum"
            summarize_file(file, client, out=out)

    elif task == 2:
        propose_abstract(files[3:], client)
    