from dataclasses import dataclass
import os
import re
import shutil
import sys


@dataclass
class WikiText(object):

    def to_json(self):
        obj = {
            'type': self.__class__.__name__,
            'fields': {}
        }
        for k, v in self.__dict__.items():
            if isinstance(v, WikiText):
                obj['fields'][k] = v.to_json()
            elif isinstance(v, list):
                obj['fields'][k] = [x.to_json() for x in v]
            else:
                obj['fields'][k] = v
        return obj

    def to_html(self):
        return '\n'.join(self.to_html_lines())


@dataclass
class Article(WikiText):
    name: str
    parts: list

    def to_html_lines(self):
        return [
            '<!DOCTYPE html>',
            '<html lang="en-US" dir="ltr">',
            '  <head>',
            f'    <base href="{BASE_URL}">',
            '    <meta charset="utf-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <link rel="stylesheet" href="style.css">',
            '  </head>',
            '  <body>',
            '    <div class="page">',
            '      <h1>',
            '        <img src="wiki.gif" />',
            f'        {self.name}',
            '      </h1>'
        ] + [
            f'      {line}'
            for part in self.parts
            for line in part.to_html_lines()
        ] + [
            '    </div>',
            '  </body>',
            '</html>'
        ]


###
### Multiline constructs
###

@dataclass
class Paragraph(WikiText):
    lines: list

    def to_html_lines(self):
        return [
            '<p>',
        ] + [
            f'  {line.to_html()}' for line in self.lines
        ] + [
            '</p>'
        ]


@dataclass
class OrderedList(WikiText):
    items: list

    def to_html_lines(self):
        return [
            '<ol>'
        ] + [
            f'  {line}'
            for item in self.items
            for line in item.to_html_lines()
        ] + [
            '</ol>'
        ]


@dataclass
class UnorderedList(WikiText):
    items: list

    def to_html_lines(self):
        return [
            '<ul>'
        ] + [
            f'  {line}'
            for item in self.items
            for line in item.to_html_lines()
        ] + [
            '</ul>'
        ]


@dataclass
class MonospaceBlock(WikiText):
    lines: list

    def to_html_lines(self):
        return [
            '<code>'
        ] + [
            f'  {line.to_html()}<br/>'
            for line in self.lines
        ] + [
            '</code>'
        ]

###
### Line level constructs
###


@dataclass
class ParagraphBreak(WikiText):
    def to_html_lines(self):
        return []


@dataclass
class HorizontalRule(WikiText):
    def to_html_lines(self):
        return ['<hr/>']


@dataclass
class Line(WikiText):
    parts: list

    def to_html(self):
        return ''.join([ part.to_html() for part in self.parts ])

    def to_html_lines(self):
        return [ self.to_html() ]


@dataclass
class MonospaceLine(WikiText):
    indent: str
    parts: str

    def to_html(self):
        return ''.join([ part.to_html() for part in self.parts ])

@dataclass
class UnorderedListItem(WikiText):
    indent: int
    stars: int
    parts: list

    def to_html_lines(self):
        return [
            '<li>'
        ] + [
            f'  {line}'
            for part in self.parts
            for line in part.to_html_lines()
        ] + [
            '</li>'
        ]


@dataclass
class OrderedListItem(WikiText):
    indent: str
    parts: list

    def to_html_lines(self):
        return [
            '<li>'
        ] + [
            f'  {line}'
            for part in self.parts
            for line in part.to_html_lines()
        ] + [
            '</li>'
        ]


@dataclass
class Definition(WikiText):
    term: list
    definition: list

    def to_html_lines(self):
        return [
            '<dl>',
            f'  <dt>{"".join([ part.to_html() for part in self.term ])}</dt>',
            f'  <dd>{"".join([ part.to_html() for part in self.definition ])}</dd>',
            '</dl>'
        ]

def separate_paragraphs(lines):

    par_lines = paragraph_lines(lines)

    return par_lines


# detect each kind of line and parse it
def paragraph_lines(lines):
    lines = [*lines]
    par_lines = []

    while lines:
        l = lines[0]
        lines = lines[1:]

        # detect paragraph breaks by whitspace lines
        if re.match(r'^\s*$', l):
            par_lines.append(ParagraphBreak())
            continue

        # detect horizontal rules
        m = re.match(r'^-----*([^-]*)$', l)
        if m:
            par_lines.append(HorizontalRule())
            rest = m.group(1)
            if rest != '':
                lines = [rest] + lines
            continue

        # detect unordered list items
        m = re.match(r'^(\s*)(\*+)([^\*].*)$', l)
        if m:
            indent = len(m.group(1))
            stars = len(m.group(2))
            text = m.group(3)
            par_lines.append(UnorderedListItem(indent, stars, [Line(convert_text(text))]))
            continue

        # detect ordered list items
        m = re.match(r'^(\s*)\d+\.?([^\*].*)$', l)
        if m:
            indent = len(m.group(1))
            text = m.group(2)
            par_lines.append(OrderedListItem(indent, [Line(convert_text(text))]))
            continue

        # detect a definition
        m = re.match(r'^\t([^:]+):\t(.*)$', l)
        if m:
            term = m.group(1)
            definition = m.group(2)
            par_lines.append(Definition(
                convert_text(term), convert_text(definition)))
            continue

        # detect monospace font
        m = re.match(r'^(\s+)([^ ].*)$', l)
        if m:
            indent = m.group(1)
            text = m.group(2)
            par_lines.append(MonospaceLine(indent, convert_text(text)))
            continue

        par_lines.append(Line(convert_text(l)))

    return par_lines

# combine lines into higher level structures


def group_by(xs, f):
    groups = []

    for x in xs:
        if len(groups) == 0 or f(x) != groups[-1][0]:
            groups.append((f(x), []))

        groups[-1][1].append(x)

    return groups


def convert_group(cls, items):

    if cls == ParagraphBreak:
        return []

    elif cls == HorizontalRule:
        return items

    elif cls == Line:
        return [Paragraph(items)]

    elif cls == MonospaceLine:
        return [MonospaceBlock(items)]

    elif cls == Definition:
        return items

    elif cls == 'ListItem':
        return convert_lists(items)

    raise ValueError(cls)


def total_indent(li):
    if isinstance(li, OrderedListItem):
        return li.indent
    elif isinstance(li, UnorderedListItem):
        return li.indent + li.stars-1


def convert_lists(items):
    parts = []

    for item in items:
        if len(parts) == 0:
            parts.append((item, []))
        elif total_indent(item) == total_indent(parts[0][0]):
            parts.append((item, []))
        else:
            parts[-1][1].append(item)


    new_items = []
    for root, subitems in parts:
        # print('------------------')
        # print(f'ROOT: {root}')
        # print(subitems)
        root.parts += convert_lists(subitems)
        new_items.append(root)
    # exit()
    grouped_items = group_by(new_items, lambda x: x.__class__)

    lists = []
    for cls, lis in grouped_items:
        if cls == UnorderedListItem:
            lists.append(UnorderedList(lis))
        elif cls == OrderedListItem:
            lists.append(OrderedList(lis))

    return lists


def convert_items(items):
    def f(x):
        if isinstance(x, OrderedListItem) or isinstance(x, UnorderedListItem):
            return 'ListItem'
        else:
            return x.__class__
            print(f'groups {groups}')
    groups = group_by(items, f)
    return [
        item
        for cls, items2 in groups
        for item in convert_group(cls, items2)
    ]


# def group_

###
### Sub-line level constructs
###


@dataclass
class Text(WikiText):
    text: str

    def to_html(self):
        return self.text


@dataclass
class WikiWord(WikiText):
    wikiword: str

    def to_html(self):
        if self.wikiword in KNOWN_TITLES:
            return f'<a href="{self.wikiword}.html">{self.wikiword}</a>'
        else:
            return self.wikiword

@dataclass
class URL(WikiText):
    url: str

    def to_html(self):
        if re.search(r'(jpe?g|png|gif|webp)', self.url, flags=re.IGNORECASE):
            return f'<img src="{self.url}" />'
        else:
            return f'<a href="{self.url}">{self.url}</a>'


@dataclass
class Italic(WikiText):
    parts: list

    def to_html(self):
        return f'<em>{"".join([ part.to_html() for part in self.parts ])}</em>'


@dataclass
class Bold(WikiText):
    parts: list

    def to_html(self):
        return f'<strong>{"".join([ part.to_html() for part in self.parts ])}</strong>'


def read_leaf_text(text):
    m = re.match("[^']+('[^']+)*|('[^']+)+", text)
    if not m:
        return None
    end = len(m.group(0))
    return (Text(text[:end]), text[end:])


def read_leaf_italic(text):
    m = re.match("''", text)
    if not m:
        return None

    res = read_leaf_text(text[2:])
    if not res:
        return None

    leaf_text, rest = res

    m2 = re.match("''", rest)
    if not m2:
        return None

    return Italic([leaf_text]), rest[2:]


def read_leaf_italic_no_close(text):
    m = re.match("''", text)
    if not m:
        return None

    res = read_leaf_text(text[2:])
    if not res:
        return None

    leaf_text, rest = res
    if res != '':
        return None

    return Italic([leaf_text]), ''


def read_leaf_bold(text):
    m = re.match("'''", text)
    if not m:
        return None

    res = read_leaf_text(text[2:])
    if not res:
        return None

    leaf_text, rest = res

    m2 = re.match("'''", rest)
    if not m2:
        return None

    return Bold([leaf_text]), rest[2:]


def read_leaf_bold_no_close(text):
    m = re.match("'''", text)
    if not m:
        return None

    res = read_leaf_text(text[2:])
    if not res:
        return None

    leaf_text, rest = res
    if res != '':
        return None

    return Bold([leaf_text]), ''


def read_italic(text):
    m = re.match("''", text)
    if not m:
        return None

    text = text[2:]
    parts = []

    while True:
        m2 = re.match("''", text)
        if m2:
            text = text[2:]
            break

        res = read_leaf_text(text) or read_leaf_bold(text)
        if res:
            part, rest = res
            parts.append(part)
            text = rest
            continue

        return None

    return Italic(parts), text


def read_italic_no_close(text):
    m = re.match("''", text)
    if not m:
        return None

    text = text[2:]
    parts = []

    while True:
        if text == '':
            break

        res = read_leaf_text(text) or read_leaf_bold(text)
        if res:
            part, rest = res
            parts.append(part)
            text = rest
            continue

        res = read_leaf_bold_no_close(text)
        if res:
            part, _ = res
            parts.append(part)
            break

        return None

    return Italic(parts), ''


def read_bold(text):
    m = re.match("'''", text)
    if not m:
        return None

    text = text[3:]
    parts = []

    while True:
        m2 = re.match("'''", text)
        if m2:
            text = text[3:]
            break

        res = read_leaf_text(text) or read_leaf_italic(text)
        if res:
            part, rest = res
            parts.append(part)
            text = rest
            continue

        return None

    return Bold(parts), text


def read_bold_no_close(text):
    m = re.match("'''", text)
    if not m:
        return None

    text = text[3:]
    parts = []

    while True:
        if text == '':
            break

        res = read_leaf_text(text) or read_leaf_italic(text)
        if res:
            part, rest = res
            parts.append(part)
            text = rest
            continue

        res = read_leaf_italic_no_close(text)
        if res:
            part, _ = res
            parts.append(part)
            break

        return None

    return Bold(parts), ''


def read_six_single_quotes(text):
    m = re.match("''''''", text)
    if not m:
        return None

    return text[6:]


def convert_text(text):
    parts = []
    urls = []
    start_part = 0
    for m in re.finditer(r"\b(https?|ftps?|gopher|mailto|news):[A-Za-z0-9\-\._~:/\?#\[\]@!\$&'\(\)\*\+\,\;\%\=]+", text):
        url_start = m.start()
        url_end = m.end()
        parts.append(convert_text_no_urls(text[start_part:url_start]))
        urls.append(text[url_start:url_end])
        start_part = url_end
    parts.append(convert_text_no_urls(text[start_part:]))

    converted = []
    for i in range(len(urls)):
        converted += parts[i]
        converted.append(URL(urls[i]))
    converted += parts[-1]
    return converted

def convert_text_no_urls(text):
    parts = []
    wikiwords = []
    start_part = 0
    for m in re.finditer(r'\b([A-Z][a-z]+([A-Z][a-z]*)+)\b', text):
        ww_start = m.start()
        ww_end = m.end()
        parts.append(convert_text_no_urls_no_wikiwords(text[start_part:ww_start]))
        wikiwords.append(text[ww_start:ww_end])
        start_part = ww_end
    parts.append(convert_text_no_urls_no_wikiwords(text[start_part:]))

    converted = []
    for i in range(len(wikiwords)):
        converted += parts[i]
        converted.append(WikiWord(wikiwords[i]))
    converted += parts[-1]
    return converted

def convert_text_no_urls_no_wikiwords(text):
    text = text.replace("''''''", '')
    parts = []

    under_single_quotes = False
    while text:
        res = read_six_single_quotes(text)
        if res:
            text = res
            continue

        res = read_leaf_text(text) or\
            read_bold(text) or\
            read_bold_no_close(text) or\
            read_italic(text) or\
            read_italic_no_close(text) or\
            None
        if res:
            part, text = res
            parts.append(part)
            # print(part, text)
            continue

        first = text[0]
        res = read_leaf_text(text[1:])
        if not res:
            text = text[1:]
            parts.append(Text(first))
        else:
            part, text = res
            parts.append(Text(first + part.text))

    # print(parts)

    return parts


def title(s):
    return ' '.join([
        m.group(0)
        for m in re.finditer(r'[A-Z][a-z]+', s)
    ])


def process_article(in_article_path, out_dir_path):
    m = re.search(r'.*/([A-Za-z]+)\.txt$', in_article_path)
    if not m:
        return None

    t = m.group(1)

    with open(in_article_path, 'r') as f:
        lines = f.read().split('\n')

    # print('\n'.join(lines))
    lines = separate_paragraphs(lines)
    article = Article(title(t), convert_items(lines))

    with open(os.path.join(out_dir_path, t + '.html'), 'w') as f:
        f.write(article.to_html())

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('please provide an input directory path, output directory path, and a base url')
        exit()

    in_dir_path = sys.argv[1]
    out_dir_path = sys.argv[2]
    BASE_URL = sys.argv[3]

    if not os.path.isdir(in_dir_path):
        print('input directory path is not a directory')
        exit()

    if not os.path.isdir(out_dir_path):
        print('output directory path is not a directory')
        exit()

    shutil.copy('wiki.gif', out_dir_path)
    shutil.copy('style.css', out_dir_path)

    for root, _, files in os.walk(in_dir_path):
        KNOWN_TITLES = [ name[:-4] for name in files ]
        for i, file in enumerate(sorted(files)):
            print(f'Processing {i/len(files): >4.1%}: {os.path.join(in_dir_path, file)}...')
            process_article(os.path.join(in_dir_path, file), out_dir_path)

    # with open(in_path, 'r') as f:
    #     lines = f.read().split('\n')
    #
    # # print('\n'.join(lines))
    # lines = separate_paragraphs(lines)
    # article = Article(title('ThisIsTheTitle'), convert_items(lines))
    #
    # for line in article.to_html_lines():
    #     print(line)
