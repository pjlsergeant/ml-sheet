import xlsxwriter

from llmsheet.formatter import Formatter

workbook = xlsxwriter.Workbook()
f = Formatter.lazy(workbook)

f1 = f({'bold': True, 'font_color': 'red'})
f2 = f({'bold': False, 'font_color': 'green'})
f3 = f({'font_color': 'red', 'bold': True})

assert( f1 != f2 )
assert( f1 == f3 )