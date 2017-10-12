import os
import glob
from matplotlib import font_manager, rc
from selenium import webdriver
import time
import shutil
import sys
from bgfunc import dirCheck

#================= personal information ===========================
project_directory=os.path.abspath(os.getcwd())
#================= personal information end =======================

spots=['160','904','910','923','937','938','939','940','941','942','950','968','969']
spot_l=["부산(레)","사상","영도","기장","해운대","부산진","금정구","동래","북구","대연","사하","남항","북항"]


def KMA(id,pw,year,chrome_driver_location):
    font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
    rc('font', family=font_name)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_download_directory=chrome_driver_location[:chrome_driver_location.rfind("/")+1]+"chrome_download"
    dirCheck(chrome_download_directory)
    dirCheck("./data/raw_data/")
    prefs={"download.default_directory":chrome_download_directory}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=chrome_driver_location, chrome_options=chrome_options)

    i=KMAlogin(driver,id,pw)
    if i!=1:
        driver.close()
        return -1
    AwsDownload(driver,year)
    move(year,chrome_download_directory)
    driver.close()
    return 1

def KMAlogin(driver,id,pw):
    driver.get("https://data.kma.go.kr/cmmn/main.do")

    item = driver.find_element_by_xpath("//li[@id='login']")
    p = item.find_element_by_tag_name('a')
    p.click()

    print("login sequence.", end="")
    elem = driver.find_element_by_id("wrap-datapop")
    while ("display: none" in elem.get_attribute("style")):
        print(".", end="")
        time.sleep(.5)
    print(".")

    elem = driver.find_element_by_id("loginId")
    elem.send_keys(id)

    elem = driver.find_element_by_id("passwordNo")
    elem.send_keys(pw)

    driver.find_element_by_id("loginbtn").click()

    print("login check")
    elem=driver.find_elements_by_class_name("msgcontainer")
    if elem!=[]:
        print("failed")
        return -1

    print("login waiting.", end="")
    elem = driver.find_element_by_id("logout")
    while ("display: none" in elem.get_attribute("style")):
        print(".", end="")
        time.sleep(.5)
        ielem = driver.find_elements_by_class_name("msgcontainer")
        if ielem != []:
            print("failed")
            return -1
    print(".")

    print("login sequence end.", end="")
    return 1

def AwsDownload(driver,year):
    driver.get("https://data.kma.go.kr/data/grnd/selectAwsRltmList.do?pgmNo=56")

    print("screen loading.", end="")
    elem = driver.find_element_by_class_name("content-head")
    titleText=elem.find_element_by_tag_name("h2").text
    while ("자료조회-방재기상관측" not in titleText):
        print(".", end="")
        time.sleep(.5)
    print(".")

    print("selecting start date sequence...")##여기부터이다.


    elem = driver.find_element_by_id("startDt")
    elem.send_keys(str(year)+"0101")

    print("waiting calendar appear.", end="")
    elem = driver.find_element_by_id("ui-datepicker-div")
    while ("display: block" not in elem.get_attribute("style")):
        print(".", end="")
        time.sleep(.5)
    print(".")

    elem = driver.find_element_by_class_name("ui-datepicker-year")
    ilist = elem.find_elements_by_tag_name("option")
    ilist.reverse()
    for option in ilist:
        if (str(year) in option.text):
            option.click()
            break

    elem = driver.find_element_by_class_name("ui-datepicker-month")
    ilist = elem.find_elements_by_tag_name("option")
    for option in ilist:
        if ("1월" in option.text):
            option.click()
            break

    elist = driver.find_elements_by_xpath("//table[@class='ui-datepicker-calendar']/tbody/tr/td")
    for e in elist:
        if ("1" in e.text):
            p = e.find_element_by_tag_name('a')
            p.click()
            break

    elem=driver.find_element_by_id("startHh")
    ilist=elem.find_elements_by_tag_name("option")
    for option in ilist:
        if ("00" in option.text):
            option.click()
            break


    print("selecting start date sequence end...")

    print("selecting end date sequence...")
    time.sleep(1)

    elem = driver.find_element_by_id("endDt")
    elem.send_keys(str(year) + "1231")

    print("waiting calendar appear.", end="")
    elem = driver.find_element_by_id("ui-datepicker-div")
    while ("display: block" not in elem.get_attribute("style")):
        print(".", end="")
        time.sleep(.5)
    print(".")

    elem = driver.find_element_by_class_name("ui-datepicker-year")
    ilist = elem.find_elements_by_tag_name("option")
    ilist.reverse()
    for option in ilist:
        if (str(year) in option.text):
            option.click()
            break

    elem = driver.find_element_by_class_name("ui-datepicker-month")
    ilist = elem.find_elements_by_tag_name("option")
    for option in ilist:
        if ("12월" in option.text):
            option.click()
            break

    elist = driver.find_elements_by_xpath("//table[@class='ui-datepicker-calendar']/tbody/tr/td")
    for e in elist:
        if ("31" in e.text):
            p = e.find_element_by_tag_name('a')
            p.click()
            break

    elem = driver.find_element_by_id("endHh")
    ilist = elem.find_elements_by_tag_name("option")
    for option in ilist:
        if ("23" in option.text):
            option.click()
            break

    print("selecting end date sequence end...")

    elem = driver.find_element_by_id("btnStn1")
    elem.click()

    print("waiting popup appear.", end="")
    elem = driver.find_elements_by_id("ztree_32_check")
    while (len(elem)==0):
        print(".", end="")
        time.sleep(.5)
        elem = driver.find_elements_by_id("ztree_32_check")
    print(".")

    print("selecting locations sequence...")
    time.sleep(.5)
    elem = driver.find_element_by_id("ztree_32_check")
    elem.click()

    elem = driver.find_element_by_xpath(
        "//div[@id='sidetreecontrol']/ul[@class='fr']/li[@class='btn-sitetree-complete']")
    p = elem.find_element_by_tag_name('a')
    p.click()

    print("waiting popup disappear.", end="")
    elem = driver.find_elements_by_id("divPopupTemp")
    while (len(elem)!=0):
        print(".", end="")
        time.sleep(.5)
        elem = driver.find_elements_by_id("divPopupTemp")
    print(".")

    print("selecting locations sequence end...")

    elem = driver.find_element_by_id("gubun")
    elem.click()

    print("waiting popup appear.", end="")
    elem = driver.find_elements_by_id("ztree_1_check")
    while (len(elem)==0):
        print(".", end="")
        time.sleep(.5)
        elem = driver.find_elements_by_id("ztree_1_check")
    print(".")

    print("selecting elements sequence...")
    time.sleep(.5)

    elem = driver.find_element_by_id("ztree_1_check")
    elem.click()

    elem = driver.find_element_by_xpath(
        "//div[@id='sidetreecontrol']/ul[@class='fr']/li[@class='btn-sitetree-complete']")
    p = elem.find_element_by_tag_name('a')
    p.click()

    print("waiting popup disappear.", end="")
    elem = driver.find_elements_by_id("divPopupTemp")
    while (len(elem)!=0):
        print(".", end="")
        time.sleep(.5)
        elem = driver.find_elements_by_id("divPopupTemp")
    print(".")

    print("selecting elements sequence end...")

    elem = driver.find_element_by_xpath("//div[@id='dsForm']/div[@class='btn-area text-center']")
    alist = elem.find_elements_by_tag_name('a')
    for p in alist:
        if ("다운로드" in p.text):
            p.click()
            break

    print("waiting popup appear.", end="")
    elem = driver.find_elements_by_id("divPopupTemp")
    while (len(elem)==0):
        print(".", end="")
        time.sleep(.5)
        elem = driver.find_elements_by_id("divPopupTemp")
    print(".")


    print("download sequence...")

    time.sleep(1)
    elem = driver.find_element_by_id("reqstPurposeCd7")
    elem.click()

    elem = driver.find_element_by_xpath("//div[@id='btnArea']/input[@class='btn btn-primary']")
    elem.click()

    print("waiting downloading.",end="")
    sys.stdout.flush()
    time.sleep(1)
    elem=driver.find_element_by_id("loading-mask")
    while("display: block" in elem.get_attribute("style")):
        print(".",end="")
        sys.stdout.flush()
        time.sleep(1)
    print(".")
    time.sleep(6)
    return

def move(form,chrome_download_directory):
    mytime=time.localtime()

    if(mytime.tm_mon<10):
        mymon="0"+str(mytime.tm_mon)
    else:
        mymon=str(mytime.tm_mon)
    if(mytime.tm_mday<10):
        myday="0"+str(mytime.tm_mday)
    else:
        myday=str(mytime.tm_mday)

    fpath = chrome_download_directory + "/"+str(mytime.tm_year)+mymon+myday+'??????.csv'

    flist = glob.glob(fpath)
    flist.reverse()
    print("\""+flist[0]+"\" moves to \""+project_directory+"/data/raw_data/AWS"+form+"Data.csv\"")

    try:
        os.stat("Aws"+form+"Data.csv")
    except:
        shutil.move(flist[0],project_directory+"/data/raw_data/AWS"+form+"Data.csv")
        return

    os.unlink("Aws"+form+"Data.csv")
    shutil.move(flist[0],project_directory+"/data/raw_data/AWS"+form+"Data.csv")
    return
