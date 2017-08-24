import csv
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import datetime

def main():
    #paths = ["부산_금정구_장전2동", "부산_해운대구_중1동", "부산_영도구_동삼2동", "부산_사상구_감전동", "부산_동래구_복산동"]
    paths = ["장전2동", "중1동", "동삼2동", "감전동", "복산동"]
    locations = ['939', '937', '910', '904', '940']
    AWSCSVPath = './20170816141620.csv'
    AWSCSVFile = open(AWSCSVPath, 'r')
    AWSCSVReader = csv.reader(AWSCSVFile)
    AWSList = []
    for AWSRow in AWSCSVReader:
        AWSList.append(AWSRow)

    labels = AWSList.pop(0)



    for i in range(len(paths)):
        writePath = './' + paths[i] + '_AWS.csv'
        f = open(writePath, 'w', newline='')
        wr = csv.writer(f)
        wr.writerow(labels)
        for AWSRow in AWSList:
            if(AWSRow[0] == locations[i]):
                wr.writerow(AWSRow)
        f.close()



if __name__ == '__main__':
    main()
