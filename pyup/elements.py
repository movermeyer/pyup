"""PyUp - Markup generation tool.

:copyright: Copyright (c) 2015 by Robert Pogorzelski.
:license:   MIT, see LICENSE for more details.

"""
from pyup.base import Element


__all__ = [
    'Bold',
    'Emphasis',
    'HorizontalLine',
    'OrderedList',
    'Section',
    'Image',
    'Link',
    'Table',
    'Text',
    'Title',
    'UnorderedList',
]


class Title(Element):

    def to_rst(self):
        line = '=' * len(self.content)
        return line + '\n' + self.content + '\n' + line

    def to_md(self):
        return '# ' + self.content


class Section(Element):

    RST_MAPPING = {
        1: '=',
        2: '-',
        3: '*',
        4: '~',
        5: '^',
    }

    def to_rst(self):
        level = self.options['level'] if 'level' in self.options else 1
        return self.content + '\n' + Section.RST_MAPPING[level] * len(self.content)

    def to_md(self):
        level = self.options['level'] if 'level' in self.options else 1
        return '#' + '#' * level + ' ' + self.content


class Text(Element):

    pass


class Emphasis(Text):

    def to_rst(self):
        return '*' + self.content + '*'

    def to_md(self):
        return '_' + self.content + '_'


class Bold(Text):

    def to_rst(self):
        return '**' + self.content + '**'

    def to_md(self):
        return self.to_rst()


class HorizontalLine(Element):

    def to_rst(self):
        return '----------------'

    def to_md(self):
        return self.to_rst()


class UnorderedList(Element):

    def to_rst(self):
        return '\n'.join(['* ' + item for item in self.content])

    def to_md(self):
        return self.to_rst()


class OrderedList(Element):

    def to_rst(self):
        output = ['#. ' + item for item in self.content]
        output[0] = '1' + output[0][1:]
        return '\n'.join(output)

    def to_md(self):
        return '\n'.join(['1. ' + item for item in self.content])


class Image(Element):

    INDENT = '    '

    def to_rst(self):
        output = ['.. image:: ' + self.content]
        if 'alt' in self.options:
            output.append(
                Image.INDENT + ':alt: ' + self.options['alt'],
            )
        if 'scale' in self.options:
            output.append(
                Image.INDENT + ':scale: ' + self.options['scale'] + ' %',
            )
        if 'align' in self.options:
            output.append(
                Image.INDENT + ':align: ' + self.options['align'],
            )
        return '\n'.join(output)

    def to_md(self):
        output = '![](' + self.content + ')'
        if 'alt' in self.options:
            output = output[:2] + self.options['alt'] + output[2:]
        if 'title' in self.options:
            output = output[:-1] + ' "' + self.options['title'] + '"' + output[-1:]
        return output


class Link(Element):

    def to_rst(self):
        title = self.options['title'] if 'title' in self.options else self.content
        return '.. _' + title + ': ' + self.content

    def to_md(self):
        title = self.options['title'] if 'title' in self.options else self.content
        return '[' + title + '](' + self.content + ')'


class Table(Element):

    def __init__(self, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.cols = len(self.content[0])
        self.rows = len(self.content)
        self.max_len = max([len(ele2) for ele in self.content for ele2 in ele])

    def to_rst(self):
        divider = ''.join(['=' * self.max_len + ' ' for _ in range(self.cols)])
        output = [divider]
        row_render = lambda i: ''.join(
            [c + ' ' * (self.max_len - len(c)) + ' ' for c in self.content[i]]
        )
        output.append(row_render(0))
        output.append(divider)
        for row in range(1, self.rows):
            output.append(row_render(row))
        output.append(divider)
        return '\n'.join(output)

    def to_md(self):
        divider = ''.join(['| ' + '-' * self.max_len + ' ' for _ in range(self.cols)])
        output = []
        row_render = lambda i: ''.join(
            ['| ' + c + ' ' * (self.max_len - len(c)) + ' ' for c in self.content[i]]
        )
        output.append(row_render(0) + '|')
        output.append(divider + '|')
        for row in range(1, self.rows):
            output.append(row_render(row) + '|')
        return '\n'.join(output)
