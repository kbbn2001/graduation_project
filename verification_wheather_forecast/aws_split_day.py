import csv
import os
import math
import copy

AWSCSVFile = open('./부산_금정구_장전2동/aws/201708.csv', 'r')
AWSCSVReader = csv.reader(AWSCSVFile)
AWSList = []
for AWSRow in AWSCSVReader:
    AWSList.append(AWSRow)

firstRow = AWSList.pop(0)


#print(item_sameTime)

while(len(AWSList)):
    item_sameTime = []
    item_sameTime.append(AWSList.pop(0))
    remove_list = []
    for i in range(len(AWSList)):
        Date = item_sameTime[0][1][0:4] + item_sameTime[0][1][5:7] + item_sameTime[0][1][8:10]
        AWSDate = AWSList[i][1][0:4] + AWSList[i][1][5:7] + AWSList[i][1][8:10]
        if(AWSDate == Date):
            item_sameTime.append(AWSList[i])
            remove_list.append(i)
    remove_list.reverse()
    for i in remove_list:
        AWSList.pop(i)

    writePath = './부산_금정구_장전2동/aws/' + Date + '.csv'
    f = open(writePath, 'w', newline='')
    wr = csv.writer(f)
    wr.writerow(firstRow)
    for item in item_sameTime:
        wr.writerow(item)
    f.close()



