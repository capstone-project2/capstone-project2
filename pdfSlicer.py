from PyPDF2 import PdfFileReader, PdfFileWriter

원본 = PdfFileReader(open("origin_paper.pdf", 'rb'))

# writer라는 이름의 pdf작성기를 준비
writer = PdfFileWriter()

# 원본 pdf파일에서 원하는 페이지를 추출해서 writer에 추가
#writer.addPage(원본.getPage(0))

#시작부터 끝까지
for i in range(87-1, 90):
    writer.addPage(원본.getPage(i))

# writer가 새 pdf파일로 저장
writer.write(open("result/sample2.pdf", 'wb'))
