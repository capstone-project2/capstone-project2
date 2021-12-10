import tika
tika.initVM()
from tika import parser
import re
import json
from collections import OrderedDict
import fitz
import io
from PIL import Image
#import tabula
import os
import pandas as pd
import dataframe_image as dfi

def Divider(content):
    page = ['- 1 -','- 2 -','- 3 -','- 4 -','- 5 -','- 6 -','- 7 -','- 8 -','- 9 -']
    contemp = []
    sectemp = []
    content = content.split("\n\n")    

    for i in range(len(content)):
        if((content[i] == '') or ('계 학술발표논문집 제' in content[i]) or (content[i] in page)):
            pass
        else:
            if(content[i].count(".") == 1 and len(content[i]) > 2 and ("0" <= content[i][0] and content[i][0] <= "9")):
                sectemp.append(content[i])
                if("0" <= content[i][2] and content[i][2] <= "9"):
                    content[i] = content[i].replace(content[i], content[i][0]+content[i][2]+"#@")
                else:
                    content[i] = content[i].replace(content[i], content[i][0]+"0#@")
            
            contemp.append(content[i])

    return contemp, sectemp

def Meta(contemp):
    stateM = 0
    metatemp = []
    abstract = []
    for i in range(len(contemp)):
        if("†" in contemp[i] and not(len(metatemp))):
                i = i - 2
                for j in range(10):
                    if("요   약" in contemp[i]):
                        #요약 삽입 방지
                        stateM = 1
                        abstract.append(contemp[i])
                        abstract.append(contemp[i+1])
                    if(stateM == 0):
                        #주제 및 소속 및 저자 삽입
                        metatemp.append(contemp[i])
                    if("주제어:" in contemp[i]):
                        #주제어 삽입
                        metatemp.append(contemp[i])
                        break
                    i = i + 1
    
    for i in metatemp:
        if(i in contemp):
            contemp.pop(contemp.index(i))
    for i in abstract:
        if(i in contemp):
            try:
                contemp.pop(contemp.index(i))
            except:
                pass
    
    return contemp, metatemp

def MetaDiv(metatemp):
    stateM = 0
    mTitle = []
    mKey = []
    mAuthor = []
    for i in range(len(metatemp)):
        if(stateM == 0 and "†" in metatemp[i]):
            stateM = 1
            startIdx = i
            for k in range(i, 0, -1):
                mTitle.append(metatemp[startIdx - k])
        elif(stateM == 1 and ("주제어:" in metatemp[i])):
            endIdx = i
            mKey.append(metatemp[endIdx])
            for j in range(startIdx, endIdx):
                mAuthor.append(metatemp[j])
            stateM = 0

    if(len(mTitle) > 1):
        mTitle = (" ".join(mTitle)).split('\n')
    if(len(mAuthor) > 1):
        mAuthor = (" ".join(mAuthor)).replace('\n',"")
    for i in range(len(mAuthor)):
        if('A' <= mAuthor[i] and mAuthor[i] <= 'Z'\
           and 'a' <= mAuthor[i+1] and mAuthor[i+1] <= 'z'):
            mAuthor = mAuthor.replace(mAuthor[i]+mAuthor[i+1],"@" + mAuthor[i]+mAuthor[i+1])
            mAuthor = mAuthor.split("@")
            break
    mKey = mKey[0][4:].split(',')
    
    return mTitle, mAuthor, mKey

def Reference(contemp):
    reftemp = []
    new = ''
    j = 0
    for i in range(len(contemp)):
        if("참고문헌" in contemp[i]):
            for p in range(50):
                #참고문헌 삽입
                j = j + 1
                try:
                    reftemp.append(contemp[i+j])
                except:
                    break
            break
        
    for i in reftemp:
        if(i in contemp):
            contemp.pop(contemp.index(i))
    contemp.pop(contemp.index('참고문헌'))

    for i in range(len(reftemp)):
        if(reftemp[i][0] == '[' and reftemp[i][2] == ']'):
            reftemp[i] = reftemp[i].replace(reftemp[i][0]+reftemp[i][1],'#$'+reftemp[i][0]+reftemp[i][1])
    new = ("".join(reftemp)).split('#$')

    for i in range(len(new)-1, -1, -1):
        new[i] = new[i].replace('\n','')
        if(new[i] == ''):
            del new[i]    
    reftemp = new
    
    return contemp, reftemp

def smooth(temp):
    j = 0
    new = []
    for i in range(len(temp)):
        if(j+1 == len(temp)):
            new.append(temp[j].replace('\n',''))
            break
        if(temp[j][2:4] == '#@' or temp[j][0:3] == '<표 '\
           or temp[j][0:4] == '<그림 ' or temp[j+1][2:4] == '#@'\
           or temp[j+1][0:3] == '<표 ' or temp[j+1][0:4] == '<그림 '):
            new.append(temp[j].replace('\n',''))
            j += 1
            pass
        else:
            if(temp[j][-1] != '.'):
                new.append((temp[j]+temp[j+1]).replace('\n',''))
                j += 1
            else:
                new.append(temp[j].replace('\n',''))
            j += 1
            
    return new

def Body(contemp):
    pure = []
    table = []
    i = 0
    size = len(contemp)
    Tcount = 0
    temp = []
    #텍스트로부터 표 데이터 분리하기
    while(True):
        if(i >= size):
            break
        Tcount = contemp[i].count('<표 ')
        pure.append(contemp[i])
        i += 1
        while(Tcount > 0):
            if(i >= size):
                break
            if(contemp[i][0:3] == '<표 '):
                pure.append(contemp[i])
                #테이블 데이터를 datafrane으로 변환해서 넣어보기
                table.append(pd.DataFrame(temp))
                temp = []
                Tcount -= 1
            else:
                temp.append(contemp[i].replace("\n",""))
            i += 1
            
    #문장 잇고 분리하기
    pure = smooth(pure)
   
    return pure, table

def Summary(contemp):

    
    
    return contemp

def ConvJson(mTitle, mAuthor, mKey, refer\
                       ,section, orignal, summary):
    metaResult = {}
    secResult = {}
    contResult = {}
    contemp = {}
    totalResult = {}

    metaResult["Title"] = mTitle
    metaResult["Author"] = mAuthor
    metaResult["Keyword"] = mKey
    metaResult["Reference"] = refer
    secResult["Section"] = section

    contemp["Orignal"] = orignal
    contemp["Summary"] = summary
    contResult["Content"] = contemp
    
    totalResult.update(metaResult)
    totalResult.update(secResult)
    totalResult.update(contResult)
    
    return totalResult

def imgExtract(pdf_file):
    if not os.path.isdir('result/img'):
        os.mkdir('result/img')
    # PDF페이지 수만큼 반복
    for page_index in range(len(pdf_file)):
        # 페이지 자체 가져오기
        page = pdf_file[page_index]
        image_list = page.getImageList()
        # 해당 페이지에서 찾은 이미지 개수 알림
        if image_list:
            pass
            #print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            #print("[!] No images found on page", page_index)
            pass
        for image_index, img in enumerate(page.getImageList(), start=1):
            # 이미지로부터 데이터정보 뽑기
            xref = img[0]
            # 이미지 바이트 추출
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            size = image.size
            if(size[0] > 1500 or size[1] > 1500 or len(image.getextrema()) < 3):
                pass
            else:
                image.save(open(f"result/img/그림 {image_index}.{image_ext}", "wb"))

def tableExtract(tables):
    #앞서 추출한 테이블 데이터를 이미지로 추출
    if not os.path.isdir('result/img'):
        os.mkdir('result/img')
    #for i, table in enumerate(tables, start=1):
    #    table.to_html(os.path.join('result', f"table_{i}.html"), index=False)
    for i in range(len(tables)):
        dfi.export(table[i], 'result/img/표 '+str(i+1)+'.jpeg', max_cols=-1, max_rows=-1)


#===============<코드 시작>==================
file = "src/sample.pdf"

#텍스트 처리
data = parser.from_file(file)

content = data["content"].strip()

content, section = Divider(content)
content, meta = Meta(content)
content, refer = Reference(content)
mTitle, mAuthor, mKey = MetaDiv(meta)

orignal, table = Body(content)
summary = Summary(content)

totalResult = ConvJson(mTitle, mAuthor, mKey, refer\
                       ,section, orignal, summary) 

with open('result/convResult.json','w',encoding='utf-8') as make_file:
    json.dump(totalResult, make_file, ensure_ascii=False, indent='\t')

#이미지 처리
pdf_file = fitz.open(file)
imgExtract(pdf_file)

#표 처리
#tables = tabula.read_pdf(file, pages="all")
tableExtract(table)



