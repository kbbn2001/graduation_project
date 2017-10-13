from PyQt5 import QtWidgets,QtGui,QtCore
from MainWindow_v2 import Ui_MainWindow
from Web import KMA
from rpy2_RNN import RNN_learn
from rpy2_RNN_loadModels import load_model
from make_train_and_test_file_v2 import data_refine
from make_train_and_test_file_v3 import data_refine as dr
from AWS_years_data_integration import integrate
import sys
import threading
import glob
import datetime as dt
import time

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(800,600)
        self.UiConnection()
        self.refresh_years()

    def UiConnection(self):
        self.ui.Btn_SelectChromedriverFile.clicked.connect(self.on_click_select_chromedriver)
        self.ui.Btn_SelectTrainData.clicked.connect(self.on_click_select_train_data)
        self.ui.Btn_SelectTestData.clicked.connect(self.on_click_select_test_data)
        self.ui.Btn_DownloadAwsData.clicked.connect(self.on_click_download_aws)
        self.ui.Btn_Learning.clicked.connect(self.on_click_learning)
        self.ui.Btn_clear_1.clicked.connect(self.on_click_clear)
        self.ui.Btn_clear_2.clicked.connect(self.on_click_clear)
        self.ui.Btn_clear_3.clicked.connect(self.on_click_clear)
        self.ui.Btn_Inference.clicked.connect(self.on_click_iload_model)
        #self.ui.pushButton_integrate.clicked.connect(self.on_click_integrate)
        self.ui.pushButton_make_train.clicked.connect(self.on_click_make_train)
        self.ui.pushButton_tex.clicked.connect(self.on_click_test)
        self.ui.comboBox_startYear.currentIndexChanged['int'].connect(self.refresh_endyears)
        self.ui.spinBox_startMonth.valueChanged['int'].connect(self.refresh_emonth)
        self.ui.spinBox_endMonth.valueChanged['int'].connect(self.refresh_smonth)
        self.ui.label_kma_link.linkActivated.connect(self.link)
        self.ui.label_cd_link.linkActivated.connect(self.link)
        self.ui.buttonGroup.buttonClicked.connect(self.radio)


    def radio(self):
        for a in self.ui.buttonGroup.buttons():
            for b in self.ui.buttonGroup_3.buttons():
                if a.text()==b.text():
                    if a.isChecked():
                        b.setDisabled(True)
                        b.setChecked(False)
                    else:
                        b.setDisabled(False)

    def refresh_smonth(self):
        self.ui.spinBox_startMonth.setMaximum(self.ui.spinBox_endMonth.value())

    def refresh_emonth(self):
        self.ui.spinBox_endMonth.setMinimum(self.ui.spinBox_startMonth.value())


    def refresh_years(self):

        self.ui.comboBox_startYear.clear()

        fpath = "./data/raw_data/AWS????Data.csv"
        flist = glob.glob(fpath)
        for i in range(len(flist)):
            f=flist[i].find("AWS")
            b=flist[i].rfind("Data")
            year = flist[i][f + 3:b]
            self.ui.comboBox_startYear.addItem(year)
        self.refresh_endyears()

    def refresh_endyears(self):

        self.ui.comboBox_endYear.clear()
        year_list = []
        for a in range(self.ui.comboBox_startYear.count()):
            year_list.append(self.ui.comboBox_startYear.itemText(a))
        ind=self.ui.comboBox_startYear.currentIndex()

        for y in year_list[ind:]:
            self.ui.comboBox_endYear.addItem(y)

    def refresh_endyears2(self):
        year_list = []
        for a in range(self.ui.comboBox_startYear.count()):
            year_list.append(self.ui.comboBox_startYear.itemText(a))
        ind = self.ui.comboBox_startYear.currentIndex()
        if self.ui.comboBox_endYear.currentText() not in year_list[ind:]:
            print("1")

            self.ui.comboBox_endYear.clear()
            for y in year_list[ind:]:
                self.ui.comboBox_endYear.addItem(y)
        elif int(self.ui.comboBox_endYear.itemText(0)) < int(self.ui.comboBox_endYear.currentText()):
            print("2")
            for i in range(self.ui.comboBox_endYear.currentIndex()):
                self.ui.comboBox_endYear.removeItem(i)
        elif int(self.ui.comboBox_endYear.itemText(0)) > int(self.ui.comboBox_startYear.currentText()):
            print("3")
            for i in range(self.ui.comboBox_endYear.currentIndex() - ind):
                self.ui.comboBox_endYear.insertItem(0, self.ui.comboBox_startYear.itemText(i))
        else:
            print("0")


    def thread_to_KMA(self, id, pw, year,chrome_driver_location):
        result=KMA(id,pw,year,chrome_driver_location)
        if result==-1:
            self.ui.statusbar.showMessage("Login failed. Write correct ID and Password.")
        self.ui.Btn_DownloadAwsData.setDisabled(False)
        temp=self.ui.statusbar.currentMessage()
        self.ui.statusbar.showMessage("AWS 데이터 다운로드 완료됨.")
        time.sleep(5)
        self.ui.statusbar.showMessage(temp)



    def on_click_select_chromedriver(self):
        self.ui.statusbar.showMessage("크롬드라이버 파일 선택중")
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.ui.centralwidget, "크롬드라이버 파일 선택창", "./",
                                                            "chromedriver file (chromedriver.exe)", options=options)
        if fileName:
            self.ui.textViewer_SelectedChromedriverDir.setText(fileName)
            self.ui.Btn_SelectChromedriverFile.setDisabled(True)
            self.ui.Btn_DownloadAwsData.setDisabled(False)
            self.ui.lineEdit_ID.setDisabled(False)
            self.ui.lineEdit_PW.setDisabled(False)
            self.ui.spinBox_Year.setDisabled(False)

        self.ui.statusbar.showMessage("대기중")

    def on_click_download_aws(self):
        if self.ui.lineEdit_ID.text()=="":
            self.ui.statusbar.showMessage("Type your KMA e-mail address before click download button.")
            return
        elif self.ui.lineEdit_PW.text()=="":
            self.ui.statusbar.showMessage("Type your Password before click download button.")
            return

        self.ui.Btn_DownloadAwsData.setDisabled(True)
        t=threading.Thread(target=self.thread_to_KMA,args=(self.ui.lineEdit_ID.text(),self.ui.lineEdit_PW.text(),self.ui.spinBox_Year.text(),self.ui.textViewer_SelectedChromedriverDir.toPlainText(),))
        t.daemon=True
        t.start()
        self.ui.statusbar.showMessage("쓰레드를 사용하여 AWS 데이터 다운로드 시작")
        ##KMA(self.lineEdit_ID.text(), self.lineEdit_PW.text(), self.spinBox_Year.text())

    def openFileNameDialog(self, QWidget,*args):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        if args is not None:
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.ui.centralwidget, args[0]+" 데이터 선택창",
                                                                "./data/refined_data/", "Csv Files (*.csv)", options=options)
        else:
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.ui.centralwidget, "QFileDialog.getOpenFileName()",
                                                                "./data/refined_data/", "Csv Files (*.csv)", options=options)
        if fileName:
            QWidget.setText(fileName)

    def on_click_select_train_data(self):
        self.ui.statusbar.showMessage("train 데이터 선택중")
        self.openFileNameDialog(self.ui.textViewer_TrainDataDir,'train')
        self.check_data_filled()
        self.ui.statusbar.showMessage("대기중")

    def on_click_select_test_data(self):
        self.ui.statusbar.showMessage("test 데이터 선택중")
        self.openFileNameDialog(self.ui.textViewer_TestDataDir,'test')
        self.check_data_filled()
        self.ui.statusbar.showMessage("대기중")

    def check_data_filled(self):
        if self.ui.textViewer_TestDataDir.toPlainText()!="":
            self.ui.Btn_Inference.setDisabled(False)
            if self.ui.textViewer_TrainDataDir.toPlainText()!="" :
                self.ui.Btn_Learning.setDisabled(False)
        else:
            self.ui.Btn_Learning.setDisabled(True)
            self.ui.Btn_Inference.setDisabled(True)

    def on_click_learning(self):
        if self.ui.lineEdit_epochs.text().isdecimal()==False:
            self.ui.statusbar.showMessage("Input decimal number in 'epochs' input box.")
            return

        if self.ui.lineEdit_hidden_dim.text().isdecimal()==False:
            self.ui.statusbar.showMessage("Input decimal number in 'hidden_dim' input box.")
            return
        start_time = dt.datetime.now()
        self.ui.statusbar.showMessage("학습중...")
        self.ui.matwidget.clr()
        self.ui.matwidget_2.clr()

        a,b=RNN_learn(self.ui.textViewer_TrainDataDir.toPlainText(),self.ui.textViewer_TestDataDir.toPlainText(),self.ui.lineEdit_epochs.text(),self.ui.lineEdit_hidden_dim.text())
        self.ui.statusbar.showMessage("그래프 작성중")
        self.ui.matwidget.plotting(a,color='red',label='Forecast TMX')
        self.ui.matwidget.plotting(b,color='blue',label='AWS TMX')
        self.ui.matwidget.labeling('시간','일 최고 온도')
        self.ui.matwidget.show()
        self.ui.matwidget.savefig('./graph/result_RNN_raw.png')

        gap = []
        for j in range(len(a)):
            gap.append(abs(float(b[j]) - float(a[j])))
        self.ui.matwidget_2.plotting(gap)
        self.ui.matwidget_2.labeling('시간','실제 최고 온도와 예상 최고 온도 차이')
        self.ui.matwidget_2.show()
        self.ui.matwidget_2.savefig('./graph/result_RNN_dif.png')
        end_time = dt.datetime.now()
        self.ui.statusbar.showMessage("학습 완료 후 대기중. (완료 시간: "+end_time.strftime('%Y-%m-%d %H:%M')+" | 소요시간: "+str(end_time-start_time)+")")


    def on_click_iload_model(self):
        start_time = dt.datetime.now()
        self.ui.statusbar.showMessage("추론중...")
        self.ui.matwidget.clr()
        self.ui.matwidget_2.clr()
        a,b=load_model(self.ui.textViewer_TestDataDir.toPlainText())
        self.ui.statusbar.showMessage("그래프 작성중")
        self.ui.matwidget.plotting(a,color='red',label='Forecast TMX')
        self.ui.matwidget.plotting(b,color='blue',label='AWS TMX')
        self.ui.matwidget.labeling('시간','일 최고 온도')
        self.ui.matwidget.show()
        self.ui.matwidget.savefig('./graph/result_RNN_raw_LD.png')

        gap = []
        for j in range(len(a)):
            gap.append(abs(float(b[j]) - float(a[j])))
        self.ui.matwidget_2.plotting(gap)
        self.ui.matwidget_2.labeling('시간','실제 최고 온도와 예상 최고 온도 차이')
        self.ui.matwidget_2.show()
        self.ui.matwidget_2.savefig('./graph/result_RNN_dif_LD.png')
        end_time = dt.datetime.now()
        self.ui.statusbar.showMessage("추론 완료 후 대기중. (완료 시간: "+end_time.strftime('%Y-%m-%d %H:%M')+" | 소요시간: "+str(end_time-start_time)+")")


    def on_click_clear(self):
        index=self.ui.tabWidget.currentIndex()
        self.ui.setupUi(self)
        self.ui.tabWidget.setCurrentIndex(index)
        self.setFixedSize(800,600)
        self.UiConnection()
        self.refresh_years()
        self.ui.statusbar.showMessage("어플리케이션 초기화 됨.")

    def chk_loc_selected(self):
        dic={}
        dic[0]=self.ui.checkBox_loc_0.isChecked()
        dic[1]=self.ui.checkBox_loc_1.isChecked()
        dic[2]=self.ui.checkBox_loc_2.isChecked()
        dic[3]=self.ui.checkBox_loc_3.isChecked()
        dic[4]=self.ui.checkBox_loc_4.isChecked()
        dic[5]=self.ui.checkBox_loc_5.isChecked()
        dic[6]=self.ui.checkBox_loc_6.isChecked()
        dic[7]=self.ui.checkBox_loc_7.isChecked()
        dic[8]=self.ui.checkBox_loc_8.isChecked()
        dic[9]=self.ui.checkBox_loc_9.isChecked()
        dic[10]=self.ui.checkBox_loc_10.isChecked()
        dic[11]=self.ui.checkBox_loc_11.isChecked()
        dic[12]=self.ui.checkBox_loc_12.isChecked()
        flag=False
        for i in dic:
            flag=flag|i
            if flag==True:
                return dic
        return -1
    def chk_tloc_selected(self):
        dic={}
        dic[0]=self.ui.radioButton_loc_0.isChecked()
        dic[1]=self.ui.radioButton_loc_1.isChecked()
        dic[2]=self.ui.radioButton_loc_2.isChecked()
        dic[3]=self.ui.radioButton_loc_3.isChecked()
        dic[4]=self.ui.radioButton_loc_4.isChecked()
        dic[5]=self.ui.radioButton_loc_5.isChecked()
        dic[6]=self.ui.radioButton_loc_6.isChecked()
        dic[7]=self.ui.radioButton_loc_7.isChecked()
        dic[8]=self.ui.radioButton_loc_8.isChecked()
        dic[9]=self.ui.radioButton_loc_9.isChecked()
        dic[10]=self.ui.radioButton_loc_10.isChecked()
        dic[11]=self.ui.radioButton_loc_11.isChecked()
        dic[12]=self.ui.radioButton_loc_12.isChecked()
        flag=False
        for i in dic:
            flag=flag|i
            if flag==True:
                return dic
        return -1
    def chk_elem_selected(self):
        dic={}
        dic[0]=self.ui.checkBox_elem_0.isChecked()
        dic[1]=self.ui.checkBox_elem_1.isChecked()
        dic[2]=self.ui.checkBox_elem_2.isChecked()
        dic[3]=self.ui.checkBox_elem_3.isChecked()
        flag=False
        for i in dic:
            flag=flag|i
            if flag==True:
                return dic
        return -1

    def chk_unit_selected(self):
        if self.ui.radioButton_unit_0.isChecked()==True:
            return 1
        elif self.ui.radioButton_unit_1.isChecked()==True:
            return 2
        elif self.ui.radioButton_unit_2.isChecked()==True:
            return 7
        elif self.ui.radioButton_unit_3.isChecked()==True:
            return 15
        elif self.ui.radioButton_unit_4.isChecked()==True:
            return 30
        else:
            return -1

    def chk_year_selected(self):
        sy = self.ui.comboBox_startYear.currentText()
        ey=self.ui.comboBox_endYear.currentText()
        if sy=="":
            return -1
        years=[]
        for y in range(self.ui.comboBox_startYear.count()):
            if int(sy)<=int(self.ui.comboBox_startYear.itemText(y)) and int(ey)>=int(self.ui.comboBox_startYear.itemText(y)):
                years.append(self.ui.comboBox_startYear.itemText(y))

        return years

    def chk_month_selected(self):
        sm = self.ui.spinBox_startMonth.value()
        em=self.ui.spinBox_endMonth.value()
        rl = []
        for n in range(sm, em + 1):
            if n < 10:
                rl.append('0' + str(n))
            else:
                rl.append(str(n))
        return rl

    def on_click_test(self):
        self.ui.statusbar.showMessage("this is spartest!")
        years=self.chk_year_selected()
        months=self.chk_month_selected()
        dic_tloc=self.chk_tloc_selected()
        dic_loc=self.chk_loc_selected()
        dic_elem=self.chk_elem_selected()
        unit=self.chk_unit_selected()
        print(years)
        print(months)
        print(dic_tloc)
        print(dic_loc)
        print(dic_elem)
        print(unit)
        dr(months,unit,dic_tloc)


    def on_click_integrate(self):
        start_time = dt.datetime.now()
        years=self.chk_year_selected()
        dic_tloc=self.chk_tloc_selected()
        dic_loc=self.chk_loc_selected()
        if years==-1:
            self.ui.statusbar.showMessage("하나 이상의 AWS 데이터가 수집되어야 합니다. 수집되어 있다면 Clear를 눌러 갱신해주세요.")
            return
        if dic_tloc==-1:
            self.ui.statusbar.showMessage("하나의 학습 타겟 지역을 선택해야 합니다.")
            return
        if dic_loc==-1:
            self.ui.statusbar.showMessage("하나 이상의 학습 데이터 지역을 선택해야 합니다.")
            return

        self.ui.statusbar.showMessage("데이터 통합중")
        integrate(years,dic_loc,dic_tloc)
        end_time = dt.datetime.now()
        self.ui.statusbar.showMessage("데이터 통합 완료 후 대기중. (완료 시간: "+end_time.strftime('%Y-%m-%d %H:%M')+" | 소요시간: "+str(end_time-start_time)+")")

    def on_click_make_train(self):
        start_time = dt.datetime.now()
        months=self.chk_month_selected()
        dic_elem=self.chk_elem_selected()
        unit=self.chk_unit_selected()
        dic_tloc=self.chk_tloc_selected()
        if dic_tloc==-1:
            self.ui.statusbar.showMessage("하나의 학습 타겟 지역을 선택해야 합니다.")
            return
        if dic_elem==-1:
            self.ui.statusbar.showMessage("하나 이상의 학습 데이터 요소를 선택해야 합니다.")
            return
        if unit==-1:
            self.ui.statusbar.showMessage("하나의 학습 데이터 단위를 선택해야합니다.")
            return
        self.ui.statusbar.showMessage("train, test 파일 작성중")
        data_refine(months,dic_elem,unit,dic_tloc)
        end_time = dt.datetime.now()
        self.ui.statusbar.showMessage("train, test 파일 작성 완료 후 대기중. (완료 시간: "+end_time.strftime('%Y-%m-%d %H:%M')+" | 소요시간: "+str(end_time-start_time)+")")


    def link(self,linkstr):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(linkstr))


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
