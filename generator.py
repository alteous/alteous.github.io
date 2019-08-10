#!/usr/bin/env python3

import os, re, sys

capture_monospace = re.compile(r'`(.*?)`')
capture_italics = re.compile(r'\_(.*?)\_')
capture_bold = re.compile(r'\*(.*?)\*')
capture_links = re.compile(r'\[(.*?)\]\((.*?)\)')
capture_images = re.compile(r'\!\[(.*?)\]\((.*?)\)')

class Formatter:
    def __init__(self, output_stream):
        self.output_stream = output_stream
        self.indent = 0
        self.indent_size = 4

    def write(self, string, delta_indent):
        if delta_indent == -1:
            self.indent -= 1
        for i in range(0, self.indent):
            print(' ' * self.indent_size, file=self.output_stream, end='')
        if delta_indent == +1:
            self.indent += 1
        print(string, file=self.output_stream)

def expand_content(content):
    content = content.replace(r'\_', '&#95;')
    content = capture_monospace.sub(r'<code>\1</code>', content)
    content = capture_italics.sub(r'<i>\1</i>', content)
    content = capture_bold.sub(r'<b>\1</b>', content)
    content = capture_links.sub(r'<a href="\2">\1</a>', content)
    return content

def generate(input_stream, output_stream, title):
    formatter = Formatter(output_stream)
    output = lambda string, delta_indent = 0 : formatter.write(string, delta_indent)

    output('<!DOCTYPE html>')
    output('<html>', +1)
    output('<head>', +1)
    output('<meta charset="UTF-8"/>')
    if title:
        output('<title>' + title + '</title>')
    output('<style>', +1)
    with open('style.css', 'r') as stylesheet:
        output("".join(stylesheet.readlines()))
    output('</style>', -1)
    output('</head>', -1)
    output('<body>', +1)
    inside_list = False
    paragraph_text = ""
    for next_whole_line in input_stream:
        line = next_whole_line.lstrip()
        is_list_item = line.startswith('*')
        if is_list_item:
            if not inside_list:
                inside_list = True
                output('<ul>', +1)
            content = expand_content(line.split('*')[1].strip())
            output('<li>' + content + '</li>')
        elif not is_list_item and inside_list:
            output('</ul>', -1)
            inside_list = False
        elif line.startswith('###'):
            content = expand_content(line.split('###')[1].strip())
            output('<h3>' + content + '</h3>')
        elif line.startswith('##'):
            content = expand_content(line.split('##')[1].strip())
            output('<h2>' + content + '</h2>')
        elif line.startswith('#'):
            content = expand_content(line.split('#')[1].strip())
            output('<h1>' + content + '</h1>')
        elif line.startswith('!['):
            content = capture_images.sub(r'<img id="\1" alt="\1" src="\2"/>', line).strip()
            output(content)
        else:
            line_is_empty = not line.strip()
            if line_is_empty and paragraph_text:
                output('<p>' + expand_content(paragraph_text).strip() + '</p>')
                paragraph_text = ""
            else:
                paragraph_text += line
    output('</body>', -1)
    output('</html>', -1)

if __name__ == '__main__':
    title = os.getenv('TITLE', 'Untitled')
    generate(sys.stdin, sys.stdout, title)
