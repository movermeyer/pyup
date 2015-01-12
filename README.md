[![Latest Version](https://pypip.in/v/pyup/badge.png)](https://pypi.python.org/pypi/pyup/)
[![Downloads](https://pypip.in/d/pyup/badge.png?period=month)](https://pypi.python.org/pypi/pyup/)
[![License](https://pypip.in/license/pyup/badge.png)](https://pypi.python.org/pypi/pyup/)

# pyup
Markup generation tool

This utility was originally written for storing text-based invoices in a database for generating PDFs on demand. It doesn't implement all Markdown or ReST directives, only the essentials. If you want to contribute, please feel welcome.

## Installation

    $ pip install pyup

## Example

### Document definition:

    import pyup


    class InvoiceGenerator(pyup.Generator):

        def get_document(self):
            data = self.data
            return (
                pyup.Title('Invoice #' + data['invoice_no']),
                pyup.Text('Date issued: ' + data['date_issued']),
                pyup.HorizontalLine(),
                pyup.Section('Items', level=3),
                pyup.Table(self.invoice_items()),
                pyup.Section('Notes', level=3),
                pyup.UnorderedList([
                    'Account no. XXX-XXX-XX-XX-XX',
                    'Non-EU sale',
                ]),
                pyup.HorizontalLine(),
            )

        def invoice_items(self):
            data = self.data
            return (
                ('Price', 'Quantity', 'Total'),
                ('10', '2', '20'),
                ('20', '1', '20'),
            )

### Generating Markdown:

    data = {
        'invoice_no': '1',
        'date_issued': '20/12/2015',
    }
    output = InvoiceGenerator(data, pyup.MARKDOWN).to_string()
    print(output)

### Output:

# Invoice #1

Date issued: 20/12/2015

----------------

### Items

| Net price | Quantity  | Total     |
| --------- | --------- | --------- |
| 10        | 2         | 20        |
| 20        | 1         | 20        |

### Notes

* Account no. XXX-XXX-XX-XX-XX
* Non-EU sale

----------------


### Source:

    # Invoice #1

    Date issued: 20/12/2015

    ----------------

    #### Items

    | Net price | Quantity  | Total     |
    | --------- | --------- | --------- |
    | 10        | 2         | 20        |
    | 20        | 1         | 20        |

    #### Notes

    * Account no. XXX-XXX-XX-XX-XX
    * Non-EU sale

    ----------------

### Generating PDF from ReStructuredText:

    output = InvoiceGenerator(data, pyup.RESTRUCTUREDTEXT).to_string()

    from rst2pdf import createpdf

    with open('test.pdf', 'w') as pdf_file:
        createpdf.RstToPdf(breaklevel=0, breakside='any').createPdf(
            text=output,
            output=pdf_file
        )
