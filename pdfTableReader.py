'''
import camelot
tables = camelot.read_pdf('src/test3.pdf')
tables.export('result/tResult.html',f='html',compress=True)

'''
import tabula
import os

tables = tabula.read_pdf("src/sample.pdf", pages="2")

folder_name = "result"
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)
# iterate over extracted tables and export as excel individually
print("<n>",type(tables))
for i, table in enumerate(tables, start=1):
    print("<p>",table)
    table.to_html(os.path.join(folder_name, f"table_{i}.html"), index=False)
    


