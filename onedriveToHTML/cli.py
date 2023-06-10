from clip import get_clip_format_name, get_clipboard_data
from dwml import omml, ET

CF_HTML = 49322

def extractHTML(data):
    """
    Extract the HTML from the clipboard data
    """
    start = data.find("<html")
    if start == -1:
        return None
    end = data.find("</html>", start)
    if end == -1:
        return None
    return data[start:end + len("</html>")]

def removeMathImgs(data):
    """
    Remove all <![if !msEquation]>...<![endif]> fragments
    """
    start = data.find("<![if !msEquation]>")
    while start != -1:
        end = data.find("<![endif]>", start)
        if end == -1:
            break
        data = data[:start] + data[end + len("<![endif]>"):]
        start = data.find("<![if !msEquation]>")
    return data

def change_ns(data):
    """
    Change xmlns:m="http://schemas.microsoft.com/office/2004/12/omml" to 
    http://schemas.openxmlformats.org/officeDocument/2006/math
    """
    return data.replace("http://schemas.microsoft.com/office/2004/12/omml", "http://schemas.openxmlformats.org/officeDocument/2006/math")

def add_mathjax(data):
    """
    Add an import of mathjax to the html
    """
    pref = """
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""
    start = data.find("<head>")
    if start == -1:
        return data
    return data[:start + len("<head>")] + pref + data[start + len("<head>"):]

def convertEquations(data):
    """
    Convert all <!--[if gte msEquation 12]>...<![endif]--> via owml to <latex>...</latex>
    """
    data = change_ns(data)
    data = add_mathjax(data)
    start = data.find("<!--[if gte msEquation 12]>")
    while start != -1:
        end = data.find("<![endif]-->", start)
        if end == -1:
            break
        omml_data = data[start + len("<!--[if gte msEquation 12]>") : end]
        omml_data = ET.fromstring(omml_data)
        latex = omml.oMath2Latex(omml_data)
        latex_data = f"\({latex.latex}\)"
        data = data[:start] + latex_data + data[end + len("<![endif]-->"):]
        start = data.find("<!--[if gte msEquation 12]>")
    return data

if __name__ == "__main__":
    cf_name = get_clip_format_name(CF_HTML)
    print(f"Getting clipboard data for format {cf_name}")
    data = get_clipboard_data(CF_HTML)
    print(f"Got {len(data)} bytes of data")
    data = data.decode("utf-8")

    data = extractHTML(data)
    data = removeMathImgs(data)
    data = convertEquations(data)

    print(data)