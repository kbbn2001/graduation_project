import os
import glob
from matplotlib import font_manager, rc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import shutil
from apscheduler.schedulers.blocking import BlockingScheduler


#================= personal information ===========================
my_id="wkddns1@naver.com"
my_pw="tkia1klu@tao"
chrome_driver_location="./chromedriver_win32/chromedriver"
project_directory="."
download_directory="C:/Users/CSE_USER/Downloads"
#================= personal information end =======================

spots=['160','904','910','923','937','938','939','940','941','942','950','968','969']
spot_l=["부산(레)","사상","영도","기장","해운대","부산진","금정구","동래","북구","대연","사하","남항","북항"]



def KMA():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(executable_path=chrome_driver_location, chrome_options=chrome_options)

    KMAlogin(driver)
    AwsHourDownload(driver)
    move("Hour")
    AwsDayDownload(driver)
    move("Day")

    driver.close()
    return

def KMAlogin(driver):
    driver.get("https://data.kma.go.kr/cmmn/main.do")

    item = driver.find_element_by_xpath("//li[@id='login']")
    p = item.find_element_by_tag_name('a')
    p.click()

    print("login sequence...")
    time.sleep(2)

    elem = driver.find_element_by_id("loginId")
    elem.send_keys(my_id)

    elem = driver.find_element_by_id("passwordNo")
    elem.send_keys(my_pw)

    driver.find_element_by_id("loginbtn").click()

    print("login sequence end...")
    time.sleep(2)
    return

def AwsHourDownload(driver):
    driver.get("https://data.kma.go.kr/data/grnd/selectAwsRltmList.do?pgmNo=56")

    print("selecting date sequence...")
    time.sleep(2)

    elem = driver.find_element_by_id("startDt")
    elem.send_keys("20170801")

    elem = driver.find_element_by_class_name("ui-datepicker-year")
    ilist = elem.find_elements_by_tag_name("option")
    for option in ilist:
        if ("2017" in option.text):
            option.click()
            break

    elem = driver.find_element_by_class_name("ui-datepicker-month")
    ilist = elem.find_elements_by_tag_name("option")
    for option in ilist:
        if ("8월" in option.text):
            option.click()
            break

    elist = driver.find_elements_by_xpath("//table[@class='ui-datepicker-calendar']/tbody/tr/td")
    for e in elist:
        if ("1" in e.text):
            p = e.find_element_by_tag_name('a')
            p.click()
            break

    print("selecting date sequence end...")
    time.sleep(1)

    elem = driver.find_element_by_id("btnStn1")
    elem.click()

    print("selecting locations sequence...")
    time.sleep(2)

    elem = driver.find_element_by_id("ztree_32_check")
    elem.click()

    elem = driver.find_element_by_id("ztree_33_check")
    elem.click()

    elem = driver.find_element_by_xpath(
        "//div[@id='sidetreecontrol']/ul[@class='fr']/li[@class='btn-sitetree-complete']")
    p = elem.find_element_by_tag_name('a')
    p.click()

    print("selecting locations sequence end...")
    time.sleep(1)

    elem = driver.find_element_by_id("gubun")
    elem.click()

    print("selecting elements sequence...")
    time.sleep(1)

    elem = driver.find_element_by_id("ztree_1_check")
    elem.click()

    elem = driver.find_element_by_xpath(
        "//div[@id='sidetreecontrol']/ul[@class='fr']/li[@class='btn-sitetree-complete']")
    p = elem.find_element_by_tag_name('a')
    p.click()

    print("selecting elements sequence end...")
    time.sleep(1)

    elem = driver.find_element_by_xpath("//div[@id='dsForm']/div[@class='btn-area text-center']")
    alist = elem.find_elements_by_tag_name('a')
    for p in alist:
        if ("다운로드" in p.text):
            p.click()
            break

    print("download sequence...")
    time.sleep(1)

    elem = driver.find_element_by_id("reqstPurposeCd7")
    elem.click()

    elem = driver.find_element_by_xpath("//div[@id='btnArea']/input[@class='btn btn-primary']")
    elem.click()

    print("waiting downloading...")
    time.sleep(6)
    return

def AwsDayDownload(driver):
    driver.get("https://data.kma.go.kr/data/grnd/selectAwsRltmList.do?pgmNo=56")

    print("selecting data form sequence...")
    time.sleep(2)

    elem = driver.find_element_by_id("dataFormCd")

    ilist = elem.find_elements_by_tag_name("option")
    for option in ilist:
        if ("일 자료" in option.text):
            option.click()
            break

    print("selecting data form sequence end...")


    print("selecting date sequence...")
    time.sleep(2)

    elem = driver.find_element_by_id("startDt")
    elem.send_keys("20170801")

    elem = driver.find_element_by_class_name("ui-datepicker-year")
    ilist = elem.find_elements_by_tag_name("option")
    for option in ilist:
        if ("2017" in option.text):
            option.click()
            break

    elem = driver.find_element_by_class_name("ui-datepicker-month")
    ilist = elem.find_elements_by_tag_name("option")
    for option in ilist:
        if ("8월" in option.text):
            option.click()
            break

    elist = driver.find_elements_by_xpath("//table[@class='ui-datepicker-calendar']/tbody/tr/td")
    for e in elist:
        if ("1" in e.text):
            p = e.find_element_by_tag_name('a')
            p.click()
            break

    print("selecting date sequence end...")
    time.sleep(1)

    elem = driver.find_element_by_id("btnStn1")
    elem.click()

    print("selecting locations sequence...")
    time.sleep(2)

    elem = driver.find_element_by_id("ztree_32_check")
    elem.click()

    elem = driver.find_element_by_id("ztree_33_check")
    elem.click()

    elem = driver.find_element_by_xpath(
        "//div[@id='sidetreecontrol']/ul[@class='fr']/li[@class='btn-sitetree-complete']")
    p = elem.find_element_by_tag_name('a')
    p.click()

    print("selecting locations sequence end...")
    time.sleep(1)

    elem = driver.find_element_by_id("gubun")
    elem.click()

    print("selecting elements sequence...")
    time.sleep(1)

    elem = driver.find_element_by_id("ztree_1_check")
    elem.click()

    elem = driver.find_element_by_xpath(
        "//div[@id='sidetreecontrol']/ul[@class='fr']/li[@class='btn-sitetree-complete']")
    p = elem.find_element_by_tag_name('a')
    p.click()

    print("selecting elements sequence end...")
    time.sleep(1)

    elem = driver.find_element_by_xpath("//div[@id='dsForm']/div[@class='btn-area text-center']")
    alist = elem.find_elements_by_tag_name('a')
    for p in alist:
        if ("다운로드" in p.text):
            p.click()
            break

    print("download sequence...")
    time.sleep(1)

    elem = driver.find_element_by_id("reqstPurposeCd7")
    elem.click()

    elem = driver.find_element_by_xpath("//div[@id='btnArea']/input[@class='btn btn-primary']")
    elem.click()

    print("waiting downloading...")
    time.sleep(6)
    return

def move(form):
    mytime=time.localtime()

    if(mytime.tm_mon<10):
        mymon="0"+str(mytime.tm_mon)
    else:
        mymon=str(mytime.tm_mon)
    if(mytime.tm_mday<10):
        myday="0"+str(mytime.tm_mday)
    else:
        myday=str(mytime.tm_mday)

    fpath = download_directory + "/"+str(mytime.tm_year)+mymon+myday+'??????.csv'

    flist = glob.glob(fpath)
    flist.reverse()
    print("\""+flist[0]+"\" moves to \""+project_directory+"/Aws"+form+"Data.csv\"")

    try:
        os.stat("Aws"+form+"Data.csv")
    except:
        shutil.move(flist[0],project_directory+"/Aws"+form+"Data.csv")
        return

    os.unlink("Aws"+form+"DData.csv")
    shutil.move(flist[0],project_directory+"/Aws"+form+"Data.csv")
    return

def DailyWork():
    KMA()
    #TODO
    #api에서 받아오기
    #TODO END
    return

def BlckSch():
    sched = BlockingScheduler()

    sched.add_job(DailyWork, 'cron', hour='23', minute='30')
    sched.start()
    return

def main():
    font_name=font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
    rc('font',family=font_name)

    DailyWork()
    return



if __name__ == '__main__':
    main()