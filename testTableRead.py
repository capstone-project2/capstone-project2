
import camelot

# PDF file to extract tables from (from command-line)
file = "src/sample.pdf"

# extract all the tables in the PDF file
tables = camelot.read_pdf(file)

# number of tables extracted
print("Total tables extracted:", tables.n)

# print the first table as Pandas DataFrame
rlaprint(tables[0].df)
