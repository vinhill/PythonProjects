"""
Example usage:
- Copy some text from onedrive, must be from a single textarea.
- Use save_from_clip() to save the clipboard html format to a file
- Use convert_file() to convert the HTML+OMML to HTML+MathML

https://github.com/plurimath/omml2mathml/blob/master/lib/omml2mathml/convert.rb
https://learn.microsoft.com/en-us/archive/blogs/murrays/mathml-and-ecma-math-omml
"""
import re

import lxml.etree as ET
from bs4 import BeautifulSoup
from bs4 import Comment
from clipboard import Clipboard


OMML_TAGS = [
    'acc', 'accPr', 'aln', 'alnScr', 'argPr', 'argSz', 'bar', 'barPr', 'baseJc', 'begChr', 'borderBox',
    'borderBoxPr', 'box', 'boxPr', 'brk', 'brkBin', 'brkBinSub', 'cGp', 'cGpRule', 'chr', 'count', 'cSp',
    'ctrlPr', 'd', 'defJc', 'deg', 'degHide', 'den', 'diff', 'dispDef', 'dPr', 'e', 'endChr', 'eqArr',
    'eqArrPr', 'f', 'fName', 'fPr', 'func', 'funcPr', 'groupChr', 'groupChrPr', 'grow', 'hideBot', 'hideLeft',
    'hideRight', 'hideTop', 'interSp', 'intLim', 'intraSp', 'jc', 'lim', 'limLoc', 'limLow', 'limLowPr',
    'limUpp', 'limUppPr', 'lit', 'lMargin', 'm', 'mathFont', 'mathPr', 'maxDist', 'mc', 'mcJc', 'mcPr', 'mcs',
    'mPr', 'mr', 'nary', 'naryLim', 'naryPr', 'noBreak', 'nor', 'num', 'objDist', 'oMath', 'oMathPara',
    'oMathParaPr', 'opEmu', 'phant', 'phantPr', 'plcHide', 'pos', 'postSp', 'preSp', 'r', 'rad', 'radPr',
    'rMargin', 'rPr', 'rSp', 'rSpRule', 'scr', 'sepChr', 'show', 'shp', 'smallFrac', 'sPre', 'sPrePr', 'sSub',
    'sSubPr', 'sSubSup', 'sSubSupPr', 'sSup', 'sSupPr', 'strikeBLTR', 'strikeH', 'strikeTLBR', 'strikeV', 'sty',
    'sub', 'subHide', 'sup', 'supHide', 't', 'transp', 'type', 'vertJc', 'wrapIndent', 'wrapRight', 'zeroAsc',
    'zeroDesc', 'zeroWid'
]


def escape_attrs(content: str) -> str:
    # ensure all html attributes are wrapped in quotes
    # use beautiful soup to parse the html and then convert it back to a string
    html = BeautifulSoup(bytes(content, encoding="utf-8"), 'html.parser')
    return str(html)


def cleanup_input(content: str) -> str:
    content = content.replace('<![endif]>', '<!--endif-->').replace('<![endif]-->', '<!--endif-- -->')
    content = content.replace('<![if !msEquation]>', '<!--if !msEquation-->')
    content = escape_attrs(content)

    html = BeautifulSoup(bytes(content, encoding="utf-8"), 'lxml')

    for comment in html.find_all(string=lambda text: isinstance(text, Comment)):
        if '[if gte msEquation 12]' in comment:
            math_content = comment.replace('[if gte msEquation 12]>', '').replace('<!--endif--', '')
            # turn into element to prevent escaping
            math_content = BeautifulSoup(math_content, 'xml')
            comment.replace_with(math_content)
        elif 'if !msEquation' in comment:
            next_node = comment.find_next_sibling()
            if next_node:
                next_node.extract()
            comment.extract()
        else:
            comment.extract()

    return str(html)


def change_ns(html: str, prefix: str, uri: str) -> str:
    # replace any xmlns:prefix="[^"]*" with xmlns:prefix="uri"
    return re.sub(rf'xmlns:{prefix}="[^"]*"', f'xmlns:{prefix}="{uri}"', html)


def clear_one_ns(html: str, prefix: str) -> str:
    # remove any xmlns:prefix="[^"]*"
    if prefix == "":
        return re.sub(r'xmlns="[^"]*"', '', html)
    
    html = re.sub(rf'xmlns:{prefix}="[^"]*"', '', html)
    return re.sub(rf'{prefix}:', '', html)


def clear_ns(html: str, *prefixes: str) -> str:
    for prefix in prefixes:
        html = clear_one_ns(html, prefix)
    return html


def clean_output(html: str) -> str:
    html = clear_ns(html, "", "m", "mml", "w")
    html = html.replace('<?xml-stylesheet type="text/xsl" href="pmathml.xsl"?>', "")
    return html


def convert_mfenced(tree: ET.Element):
    # from <mfenced open="(" close=")" separators=",">...</mfenced>
    # to <mo>(</mo>...<mo>)</mo>
    open_tag = tree.get("open") or "("
    close_tag = tree.get("close") or ")"
    separators = tree.get("separators")

    open_elem = ET.Element("mo")
    open_elem.text = open_tag
    tree.insert(0, open_elem)

    close_elem = ET.Element("mo")
    close_elem.text = close_tag
    tree.append(close_elem)

    if separators:
        # insert separators between each child, if there are #children = #separators + 1
        if len(tree) == len(separators) + 1:
            for i, child in enumerate(tree):
                if i % 2 == 1:
                    separator_elem = ET.Element("mo")
                    separator_elem.text = separators[i // 2]
                    tree.insert(i, separator_elem)

    # move all children to parent node, remove the mfenced
    for child in tree:
        tree.addprevious(child)
    tree.getparent().remove(tree)


def convert_all_mfenced(tree: ET.Element):
    for elem in tree.xpath("//*[local-name()='mfenced']"):
        convert_mfenced(elem)


def convert(content: str) -> str:
    #with open('xhtml-mathml.xsl', 'rb') as f:
    with open('omml2mml.xsl', 'rb') as f:
        xslt = ET.XSLT(ET.parse(f))

    content = cleanup_input(content)
    content = change_ns(content, "m", "http://schemas.openxmlformats.org/officeDocument/2006/math")

    xml = ET.XML(bytes(content, encoding="utf-8"))

    for elem in xml.xpath("//*[local-name()='oMath' or local-name()='oMathPara']"):
        elem_xml = ET.tostring(elem, encoding='unicode')
        input_tree = ET.XML(elem_xml)
        output_tree = xslt(input_tree)
        convert_all_mfenced(output_tree)
        output_str = ET.tostring(output_tree, encoding='unicode', xml_declaration=False)
        output_str = clean_output(output_str)
        elem.getparent().replace(elem, ET.fromstring(f"<math>{output_str}</math>"))

    return ET.tostring(xml, pretty_print=True, encoding='unicode')


def convert_file(fname: str) -> str:
    with open(fname, 'r', encoding='utf-8') as file:
        result = convert(file.read())
    with open("converted.html", "w", encoding='utf-8') as f:
        f.write(result)


def testcase():
    xml = '<div lang=en-GB>-&gt; <!--[if gte msEquation 12]><m:oMath xmlns:m="http://schemas.microsoft.com/office/2004/12/omml"><m:sSup><m:sSupPr><m:ctrlPr/></m:sSupPr><m:e><m:r><m:t>&#119910;</m:t></m:r></m:e><m:sup><m:r><m:t>(0)</m:t></m:r></m:sup></m:sSup><m:r><m:t>=</m:t></m:r><m:r><m:t><m:d>&#119909;</m:d></m:t></m:r><m:d><m:dPr><m:ctrlPr/></m:dPr><m:e/></m:d></m:oMath><![endif]--></div>'
    print(cleanup_input(xml))
    print(convert(xml))


def save_from_clip():
    # copy content from onedrive, get it as utf-8 html from clipboard
    # important to get utf-8, otherwise the text will be corrupted
    # TODO filter out some initial crap before the <html> tag
    with Clipboard() as clip:
        content = clip["html"]
    with open("test.html", "w", encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    #save_from_clip()

    # TODO menclose might not work, as it is a non-standard MathML tag
    convert_file("test.html")

    #testcase()