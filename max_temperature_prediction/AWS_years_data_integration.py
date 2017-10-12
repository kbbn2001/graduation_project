import csv
import os
import glob
from bgfunc import dirCheck
def integrate(years,dic_loc,dic_tloc):
    dirCheck("./data/integrated_data/")
    fpath = "./data/integrated_data/*_AWS.csv"
    flist = glob.glob(fpath)
    for file in flist:
        os.remove(file)
    locations = ['160', '904', '910', '923', '937', '938', '939', '940', '941', '942', '950', '968', '969']
    paths = ["부산(레)", "사상", "영도", "기장", "해운대", "부산진", "금정구", "동래", "북구", "대연", "사하", "남항", "북항"]
    AWSList = []
    labels = ''
    for year in years:
        AWSCSVPath = './data/raw_data/AWS' + str(year) + 'Data.csv'
        index = 0

        with open(AWSCSVPath, newline='', encoding='EUC-KR') as f:
            reader = csv.reader(f)
            for AWSRow in reader:
                if ( index == 0):
                    index += 1
                    labels = AWSRow
                    continue
                AWSList.append(AWSRow)

    dirCheck("./data/integrated_data/")

    for i in range(len(paths)):
        if dic_loc[i]==True or dic_tloc[i]==True:
            writePath = './data/integrated_data/' + paths[i] + '_AWS.csv'
            f = open(writePath, 'w', newline='')
            wr = csv.writer(f)
            wr.writerow(labels) 
            for AWSRow in AWSList:
                if(AWSRow[0] == locations[i]):
                    wr.writerow(AWSRow)
            f.close()
