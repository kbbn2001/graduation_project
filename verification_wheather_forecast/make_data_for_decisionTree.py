
import csv
paths = ["부산_금정구_청룡동", "부산_금정구_장전2동", "부산_해운대구_중1동", "부산_영도구_동삼2동", "부산_사상구_감전동", "부산_동래구_복산동"]

AWSCSVPath = './부산_금정구_청룡동_test.csv'
AWSCSVFile = open(AWSCSVPath, 'r')
AWSCSVReader = csv.reader(AWSCSVFile)
AWSList = []

writePath = './test.csv'
f = open(writePath, 'w', newline='')
wr = csv.writer(f)

for AWSRow in AWSCSVReader:
    AWSList.append(AWSRow)
labels = AWSList.pop(0)
wr.writerow(labels)
for AWSRow in AWSList:
    if(AWSRow[4] == ''):
        AWSRow[4] = '-1'
    if (AWSRow[5] == ''):
        AWSRow[5] = '-1'
    if (AWSRow[6] == ''):
        AWSRow[6] = '-1'
    AWSRow[2] = AWSRow[2][11:13]
    print(AWSRow)
    if(AWSRow[2][1] == ':'):
        AWSRow[2] = '0' + AWSRow[2][0]
    AWSRow[2] = int(int(AWSRow[2]) / 6)


for AWSRow in AWSList:
    wr.writerow(AWSRow)
f.close()