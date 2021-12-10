from tika import parser
import re
import json
from collections import OrderedDict

contemp = []
meta = []
metaTemp = []
metaResult = {}
section = []
secResult = {}
body = []
botemp = []
contResult = {}
stateM = 0
stateB = 0
totalResult = {}
data = parser.from_file("src/samplePast.pdf")
content = data["content"].strip()

#print(content)
tmp = {}
tmp["test"] = content

for i in range(8):
    content = content.replace(str(i+1)+". ","@_@"+str(i+1)+".")
content = content.split("@_@") 

for i in range(len(content)):
    if not((content[i] == "")):
        contemp.append(content[i])

for i in range(len(contemp)):
    contemp[i] = contemp[i].split("\n\n")

for i in range(len(contemp)):
    for j in range(len(contemp[i])):
        if(contemp[i][j].count(".") == 1 and len(contemp[i][j]) > 2 and ("0" <= contemp[i][j][0] and contemp[i][j][0] <= "9")):
            #목차 삽입
            section.append(contemp[i][j])
            if("0" <= contemp[i][j][2] and contemp[i][j][2] <= "9"):
                #큰 목차는 10#@
                contemp[i][j] = contemp[i][j].replace(contemp[i][j], contemp[i][j][0]+contemp[i][j][2]+"#@")
            else:
                #작은 목차는 11$@
                contemp[i][j] = contemp[i][j].replace(contemp[i][j], contemp[i][j][0]+"0$@")
        
        if("†" in contemp[i][j] and not(len(meta))):
            j = j - 1
            for k in range(10):
                if("요   약" in contemp[i][j]):
                    #요약 삽입 방지
                    stateM = 1
                if(stateM == 0):
                    #주제 및 소속 및 저자 삽입
                    meta.append(contemp[i][j])
                if("주제어:" in contemp[i][j]):
                    #주제어 삽입
                    meta.append(contemp[i][j])
                    break
                j = j + 1
        
        #if("[" in contemp[i][j][0:7] and "]" in contemp[i][j][0:7]\
        #   and ("표" in contemp[i][j][0:7] or "그림" in contemp[i][j][0:7])):
            #contemp[i][j] = contemp[i][j].replace(contemp[i][j][-1],contemp[i][j][-1]+"@@")
            #contemp[i][j] = contemp[i][j].replace("\n","@@")
           # print("<><>",contemp[i][j])
        
            
        if("참고문헌" in contemp[i][j]):
            for p in range(50):
                if(contemp[i][j].count("-") > 1):
                    break
                #참고문헌 삽입
                meta.append(contemp[i][j])
                j = j + 1
            break
        if(contemp[i][j].count("-") < 2 or botemp[i] != "" or botemp[i] != " "):
            if("[" in contemp[i][j][0:7] and "]" in contemp[i][j][0:7]\
           and ("표" in contemp[i][j][0:7] or "그림" in contemp[i][j][0:7])):
                tmp = contemp[i][j].split("\n")
                for k in range(len(tmp)):
                    botemp.append(tmp[k])
                    #print(tmp[k])
            else:
                botemp.append(contemp[i][j])
            
#body내용 처리
for i in range(len(meta)):
    try:
        botemp.remove(meta[i])
    except:
        continue

for i in range(len(botemp)-1 , 0 , -1):
    botemp[i] = botemp[i].replace("\n","")
    if(botemp[i].count("-") > 1 or botemp[i] == ""):
        del(botemp[i])
    if("한국컴퓨터교육학회" in botemp[i]):
        del(botemp[i])
    if(stateB == 0 and "주제어:" in botemp[i]):
        del(botemp[i])
        stateB = 1
    if(stateB == 1):
        if(botemp[i][0] == "요" and botemp[i][4] == "약"):
            del(botemp[i])
            stateB = 0
        else:
            del(botemp[i])

for i in range(len(meta)):
    meta[i] = meta[i].split("\n")

for i in range(len(meta)):
    for j in range(len(meta[i])):
        metaTemp.append(meta[i][j])

metaTitle = []
metaAuthor = []
metaSum = []
metaRefer = []

stateM = 0
for i in range(len(metaTemp)):
    if(stateM == 0 and "†" in metaTemp[i]):
        stateM = 1
        startIdx = i
        for k in range(k-3, 0, -1):
            metaTitle.append(metaTemp[startIdx - k])
    elif(stateM == 1 and ("주제어:" in metaTemp[i])):
        endIdx = i
        metaSum.append(metaTemp[endIdx])
        for j in range(startIdx, endIdx):
            metaAuthor.append(metaTemp[j])
        stateM = 0
    elif("참고문헌" in metaTemp[i]):
        p = i
        for q in range(p, len(metaTemp)):
            metaRefer.append(metaTemp[q])
        break
    else:
        pass

lastTitle = "".join(metaTitle)
lastAuthor = "".join(metaAuthor)
lastSum = metaSum[0].replace("주제어:","").split(",")
lastRefer = "".join(metaRefer).replace("참고문헌","").replace("[","@[")

#주제 한글과 영문 분리
for i in range(len(lastTitle)):
    if('a' <= lastTitle[i] and lastTitle[i] <= 'z'\
       or 'A' <= lastTitle[i] and lastTitle[i] <= 'Z'):
        tempC = lastTitle[i]
        metaTitle = lastTitle.split(tempC)
        metaTitle[1] = tempC + metaTitle[1]
        break

metaRefer = lastRefer.split("@")
for i in range(len(metaRefer)-1, -1, -1):
    if(metaRefer[i] == ""):
        metaRefer.pop(i)

stateC = 0
#저자 한글과 영문 분리
for i in range(len(lastAuthor)):
    if('a' <= lastAuthor[i] and lastAuthor[i] <= 'z'\
       or 'A' <= lastAuthor[i] and lastAuthor[i] <= 'Z'):
        if(stateC == 1):
            tempC = lastAuthor[i]
            metaAuthor = lastAuthor.split(tempC)
            metaAuthor[1] = tempC + metaAuthor[1]
            break
        stateC = stateC + 1

#section정리
for i in range(len(section)):
    section[i] = section[i].replace("\n","")


#body내용 자연스럽게 잇기 처리
lastbody = []
for i in range(len(botemp)-1):
    if(botemp[i][-1] != "." and botemp[i][-2] != "."\
       and botemp[i][3] != "@" and botemp[i+1][3] != "@"\
       and botemp[i+1][0] != "["):
        lastbody.append(botemp[i]+(botemp[i+1]))
        #print("<마크>",botemp[i][-1])
        #print(botemp[i])
        #print("<병합>")
        #print(botemp[i+1])
        #print("<Next>================================================")
    #else:
        #lastbody.append(botemp[i+1])

for i in range(len(botemp)-1, -1, -1):
    if(botemp[i-1][-1] != "." and botemp[i-1][-2] != "."\
       and botemp[i-1][3] != "@" and botemp[i][3] != "@"\
       and botemp[i][0] != "["):
        botemp[i] = botemp[i-1]+botemp[i]
        del botemp[i-1]
#for i in range(len(botemp)):
#    print(botemp[i])
#    print("<Next>")

#meta와 section을 딕셔너리로 정리
metaResult["Title"] = metaTitle
metaResult["Author"] = metaAuthor
metaResult["Keyword"] = lastSum
metaResult["Reference"] = metaRefer
secResult["Section"] = section
contResult["Content"] = botemp

#json저장 전 모든 정리 데이터 병합
totalResult.update(metaResult)
totalResult.update(secResult)
totalResult.update(contResult)

#for i in range(len(botemp)):
#    print(botemp[i])
#    print("<Next>")

#json으로 저장
#with open('result/extracted.json', 'w', encoding="utf-8") as make_file:
#    json.dump(totalResult, make_file, ensure_ascii=False, indent="\t")

#print(metaResult["Title"])
#print(secResult["Section"][0])


#본문 내용과 캡션 분리하는 것 성공함.
#앞서서 본문 내용 중 메타데이터 뽑아낼때 일부 탈락되는
#내용이 있는 것으로 확인되고, 이거 해결하고 난 뒤
#각 나눠진 문단들 중 끊긴 부분 자연스럽게 이어주기
#그리고 원본 영역과 요약(빈칸) 구분해서 json파일 만들기

#문장의 마지막 문자 마침표인지 체크하고 아니면 이어버리기
#그림이나 도표 캡션 수정하기
#정리한 데이터 딕셔너리로 만들고 json파일로 저장
