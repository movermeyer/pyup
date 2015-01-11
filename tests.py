# -*- coding: utf-8 -*-
"""PyUp - Markup generation tool.

:copyright: Copyright (c) 2015 by Robert Pogorzelski.
:license:   MIT, see LICENSE for more details.

"""
import unittest

import pyup


class DocumentGenerator(pyup.Generator):

    def get_document(self):
        data = self.data
        document = [
            pyup.Title(data['title']),
            pyup.Section(data['title']),
            pyup.Section(data['title'], level=2),
            pyup.Section(data['title'], level=3),
            pyup.Text(data['text1']),
            pyup.Section(data['title'], level=3),
            pyup.Bold(data['bold1']),
            pyup.Section(data['title'], level=2),
            pyup.Section(data['title'], level=3),
            pyup.Emphasis(data['text2']),
            pyup.HorizontalLine(),
            pyup.Section(data['title'], level=4),
            pyup.UnorderedList(['A', 'B', 'C']),
            pyup.Section(data['title'], level=4),
            pyup.OrderedList(['A', 'B', 'C']),
            pyup.HorizontalLine(),
        ]
        if data['with_table']:
            document.append(pyup.Table(self.table_items()))
        return document

    def table_items(self):
        data = self.data
        return (
            ('Column1', 'Column2', 'Column3'),
            ('Cell1', data['cell1'], 'Cell3'),
            ('Cell4', 'Cell5', data['cell2']),
        )


class TestGenerator(unittest.TestCase):

    def setUp(self):
        data = {
            'bold1': 'data1',
            'cell1': 'data2',
            'cell2': 'data3',
            'text1': 'data4',
            'text2': 'data5',
            'title': 'data6',
            'with_table': True,
        }
        self.rst_generator = DocumentGenerator(data, pyup.RESTRUCTUREDTEXT)
        self.md_generator = DocumentGenerator(data, pyup.MARKDOWN)

    def test_to_rst(self):
        self.assertEqual(
            self.rst_generator.to_string(),
            (
                '=====\ndata6\n=====\n\ndata6\n=====\n\ndata6\n-----\n\ndata6'
                '\n*****\n\ndata4\n\ndata6\n*****\n\n**data1**\n\ndata6\n-----'
                '\n\ndata6\n*****\n\n*data5*\n\n----------------\n\ndata6\n~~~'
                '~~\n\n* A\n* B\n* C\n\ndata6\n~~~~~\n\n1. A\n#. B\n#. C\n\n--'
                '--------------\n\n======= ======= ======= \nColumn1 Column2 C'
                'olumn3 \n======= ======= ======= \nCell1   data2   Cell3   \n'
                'Cell4   Cell5   data3   \n======= ======= ======= \n'
            )
        )

    def test_to_md(self):
        self.assertEqual(
            self.md_generator.to_string(),
            (
                '# data6\n\n## data6\n\n### data6\n\n#### data6\n\ndata4\n\n##'
                '## data6\n\n**data1**\n\n### data6\n\n#### data6\n\n_data5_\n'
                '\n----------------\n\n##### data6\n\n* A\n* B\n* C\n\n##### d'
                'ata6\n\n1. A\n1. B\n1. C\n\n----------------\n\n| Column1 | C'
                'olumn2 | Column3 |\n| ------- | ------- | ------- |\n| Cell1 '
                '  | data2   | Cell3   |\n| Cell4   | Cell5   | data3   |\n'
            )
        )


class TestRestructuredTextElements(unittest.TestCase):

    def setUp(self):
        self.mode = pyup.RESTRUCTUREDTEXT

    def test_Title(self):
        elem = pyup.Title('test_string')
        self.assertEqual(
            elem.process(self.mode),
            '===========\ntest_string\n==========='
        )

    def test_Section(self):
        elem = pyup.Section('test_string')
        self.assertEqual(elem.process(self.mode), 'test_string\n===========')

        elem = pyup.Section('test_string', level=1)
        self.assertEqual(elem.process(self.mode), 'test_string\n===========')

        elem = pyup.Section('test_string', level=2)
        self.assertEqual(elem.process(self.mode), 'test_string\n-----------')

        elem = pyup.Section('test_string', level=3)
        self.assertEqual(elem.process(self.mode), 'test_string\n***********')

        elem = pyup.Section('test_string', level=4)
        self.assertEqual(elem.process(self.mode), 'test_string\n~~~~~~~~~~~')

        elem = pyup.Section('test_string', level=5)
        self.assertEqual(elem.process(self.mode), 'test_string\n^^^^^^^^^^^')

    def test_Text(self):
        elem = pyup.Text('§¶•ĽľŁÓ-test_string-Ń™ŹĆŻ€ßį')
        self.assertEqual(elem.process(self.mode), '§¶•ĽľŁÓ-test_string-Ń™ŹĆŻ€ßį')

    def test_Emphasis(self):
        elem = pyup.Emphasis('test string')
        self.assertEqual(elem.process(self.mode), '*test string*')

    def test_Bold(self):
        elem = pyup.Bold('test string')
        self.assertEqual(elem.process(self.mode), '**test string**')

    def test_HorizontalLine(self):
        elem = pyup.HorizontalLine()
        self.assertEqual(elem.process(self.mode), '----------------')

        elem = pyup.HorizontalLine('test string')
        self.assertEqual(elem.process(self.mode), '----------------')

    def test_UnorderedList(self):
        elem = pyup.UnorderedList(['A', 'B', 'C', 'D'])
        self.assertEqual(elem.process(self.mode), '* A\n* B\n* C\n* D')

    def test_OrderedList(self):
        elem = pyup.OrderedList(['A', 'B', 'C', 'D'])
        self.assertEqual(elem.process(self.mode), '1. A\n#. B\n#. C\n#. D')

    def test_Image(self):
        elem = pyup.Image('path_to_file')
        self.assertEqual(elem.process(self.mode), '.. image:: path_to_file')

        elem = pyup.Image('path_to_file', alt='Alt Text', title='Title', scale='50', align='right')
        self.assertEqual(
            elem.process(self.mode),
            (
                '.. image:: path_to_file\n' +
                pyup.Image.INDENT + ':alt: Alt Text\n' +
                pyup.Image.INDENT + ':scale: 50 %\n' +
                pyup.Image.INDENT + ':align: right'
            )
        )

    def test_Link(self):
        elem = pyup.Link('http://example.com')
        self.assertEqual(elem.process(self.mode), '.. _http://example.com: http://example.com')

        elem = pyup.Link('http://example.com', title='Example.com')
        self.assertEqual(elem.process(self.mode), '.. _Example.com: http://example.com')

    def test_Table(self):
        elem = pyup.Table([
            ['Col1', 'Col2'],
            ['Cell1', 'Cell2'],
            ['Cell3', 'Cell4'],
        ])
        self.assertEqual(
            elem.process(self.mode),
            '===== ===== \nCol1  Col2  \n===== ===== \nCell1 Cell2 \nCell3 Cell4 \n===== ===== '
        )


class TestMarkdownElements(unittest.TestCase):

    def setUp(self):
        self.mode = pyup.MARKDOWN

    def test_Title(self):
        elem = pyup.Title('test_string_Ń™€ßį§¶•Ľľ')
        self.assertEqual(elem.process(self.mode), '# test_string_Ń™€ßį§¶•Ľľ')

    def test_Section(self):
        elem = pyup.Section('test_string')
        self.assertEqual(elem.process(self.mode), '## test_string')

        elem = pyup.Section('test_string', level=1)
        self.assertEqual(elem.process(self.mode), '## test_string')

        elem = pyup.Section('test_string', level=2)
        self.assertEqual(elem.process(self.mode), '### test_string')

        elem = pyup.Section('test_string', level=3)
        self.assertEqual(elem.process(self.mode), '#### test_string')

        elem = pyup.Section('test_string', level=4)
        self.assertEqual(elem.process(self.mode), '##### test_string')

        elem = pyup.Section('test_string', level=5)
        self.assertEqual(elem.process(self.mode), '###### test_string')

    def test_Text(self):
        elem = pyup.Text('§¶•ĽľŁÓ-test_string-Ń™ŹĆŻ€ßį')
        self.assertEqual(elem.process(self.mode), '§¶•ĽľŁÓ-test_string-Ń™ŹĆŻ€ßį')

    def test_Emphasis(self):
        elem = pyup.Emphasis('test string')
        self.assertEqual(elem.process(self.mode), '_test string_')

    def test_Bold(self):
        elem = pyup.Bold('test string')
        self.assertEqual(elem.process(self.mode), '**test string**')

    def test_HorizontalLine(self):
        elem = pyup.HorizontalLine()
        self.assertEqual(elem.process(self.mode), '----------------')

        elem = pyup.HorizontalLine('test string')
        self.assertEqual(elem.process(self.mode), '----------------')

    def test_UnorderedList(self):
        elem = pyup.UnorderedList(['A', 'B', 'C', 'D'])
        self.assertEqual(elem.process(self.mode), '* A\n* B\n* C\n* D')

    def test_OrderedList(self):
        elem = pyup.OrderedList(['A', 'B', 'C', 'D'])
        self.assertEqual(elem.process(self.mode), '1. A\n1. B\n1. C\n1. D')

    def test_Image(self):
        elem = pyup.Image('path_to_file')
        self.assertEqual(elem.process(self.mode), '![](path_to_file)')

        elem = pyup.Image('path_to_file', alt='Alt Text', title='Title')
        self.assertEqual(elem.process(self.mode), '![Alt Text](path_to_file "Title")')

    def test_Link(self):
        elem = pyup.Link('http://example.com')
        self.assertEqual(elem.process(self.mode), '[http://example.com](http://example.com)')

        elem = pyup.Link('http://example.com', title='Example.com')
        self.assertEqual(elem.process(self.mode), '[Example.com](http://example.com)')

    def test_Table(self):
        elem = pyup.Table([
            ['Col1', 'Col2'],
            ['Cell1', 'Cell2'],
            ['Cell3', 'Cell4'],
        ])
        self.assertEqual(
            elem.process(self.mode),
            '| Col1  | Col2  |\n| ----- | ----- |\n| Cell1 | Cell2 |\n| Cell3 | Cell4 |'
        )


if __name__ == '__main__':
    unittest.main()
