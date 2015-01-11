"""PyUp - Markup generation tool.

:copyright: Copyright (c) 2015 by Robert Pogorzelski.
:license:   MIT, see LICENSE for more details.

"""
RESTRUCTUREDTEXT = 'rst'
MARKDOWN = 'md'


class Element(object):

    def __init__(self, content=None, **options):
        self.content = content
        self.options = options

    def to_rst(self):
        return self.content

    def to_md(self):
        return self.content

    def process(self, mode):
        return getattr(self, 'to_' + mode)()


class Generator(object):

    def __init__(self, data, mode):
        self.data = data
        self.mode = mode

    def get_document(self):
        raise NotImplementedError

    def to_string(self):
        document = self.get_document()
        output = []
        for elem in document:
            result = elem.process(self.mode)
            if result is not None:
                output.append(result)
                output.append('')
        return '\n'.join(output)
