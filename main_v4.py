import os, io
import math
import csv
from datetime import datetime

import webbrowser
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import *
import sys
import pymysql
import pandas as pd

from WaitingSpinnerWidget import Overlay
from mainUI4 import Ui_MainWindow


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

conn = pymysql.connect(
        # host="localhost",
        host="localhost",
        user="root",
        password="",
        db="jodalcheng",
        port=3306,
        charset='utf8')

global row_num, current_page_num, total_page_num, check_result, search_trigger, fname
row_num = 0
current_page_num = 1
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM tpn_public_notice")
total_num = cursor.fetchone()[0]
total_page_num = math.ceil(int(total_num) / 40)
check_result = False
search_trigger = False

class test(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initMainTable()

        self.overlay = Overlay(self.centralWidget())
        self.overlay.hide()

        self.pushButton_search.clicked.connect(self.btn_search)
        self.pushButton_clear.clicked.connect(self.initMainTable)
        self.pushButton_previous_page.clicked.connect(self.btn_previous_page)
        self.pushButton_next_page.clicked.connect(self.btn_next_page)

        self.radioButton_bidE.clicked.connect(self.radioB_bidE)

        # self.tableWidget.cellClicked.connect(self.cell_clicked)
        self.tableWidget.cellDoubleClicked.connect(self.cell_DBclicked)

        self.dateEdit_start.setDate(QDate.currentDate())
        self.dateEdit_end.setDate(QDate.currentDate())
        self.pushButton_folder_path.clicked.connect(self.open_folder_path_clicked)
        self.pushButton_download.clicked.connect(self.download_excel)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True) # 행마다 색깔을 변경 하는 코드
        self.gui_palette = QtGui.QPalette() #반복되는 행의 색깔을 지정하는 코드
        self.gui_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(255,255,0,0)) #반복되는 행의 색깔을 지정하는 코드
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # Pyqt종료시 호출
    def closeEvent(self, event):
        conn.close()     # DB연결 종료
        super(test, self).closeEvent(event)

    # Resize 이벤트
    def resizeEvent(self, event):
        super(test, self).resizeEvent(event)
        self.arrangecolumn()
        self.overlay.resize(event.size())

    def showEvent(self, a0):
        self.arrangecolumn()
        return super().showEvent(a0)

    def no_result(self):
        global current_page_num, total_page_num, check_result, search_trigger
        current_page_num = 1
        total_page_num = 1
        table = self.tableWidget
        table.setColumnCount(1)
        table.setRowCount(1)
        table.setHorizontalHeaderLabels(["검색 결과"])
        table.setItem(0, 0, QTableWidgetItem("조회 결과가 없습니다."))
        self.label_3.setText(str(total_page_num)+"페이지 중 " + str(current_page_num) + "페이지")
        self.arrangecolumn()
        check_result = False
        search_trigger = False

    # 메인테이블에 DB 데이터 표시하기
    def refreshMainTable(self):
        global current_page_num, total_page_num, check_result
        if check_result == False:
            self.init_table()
            check_result = True
        current_page_num = 1
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tpn_public_notice WHERE pn_visible = 1")
        total_num = cursor.fetchone()[0]
        total_page_num = math.ceil(int(total_num) / 40)
        cursor.execute("SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts FROM tpn_public_notice WHERE pn_visible = 1 ORDER BY pn_date desc limit 40")
        table = self.tableWidget
        table.setRowCount(0)

        for row, form in enumerate(cursor):
            table.insertRow(row)
            for column, item in enumerate(form):
                if (column<9):
                    table.setItem(row, column, QTableWidgetItem(str(item)))

        self.label_3.setText(str(total_page_num)+"페이지 중 " + str(current_page_num) + "페이지")
        self.arrangecolumn()

    # 메인테이블 초기화
    def initMainTable(self):
        global check_result, search_trigger
        table = self.tableWidget

        table.setColumnCount(9)
        table.setRowCount(0)
        table.setHorizontalHeaderLabels(["번호","공고/계약일","사업명","계약방법","기관명","금액", "입찰 개시 일시", "입찰 마감 일시", "개찰(입찰) 일시"])

        check_result = True
        search_trigger = False
        self.refreshMainTable()

    # no_result 후 컬럼명 초기화
    def init_table(self):
        global check_result
        table = self.tableWidget

        table.setColumnCount(9)
        table.setRowCount(0)
        table.setHorizontalHeaderLabels(["번호","공고/계약일","사업명","계약방법","기관명","금액", "입찰 개시 일시", "입찰 마감 일시", "개찰(입찰) 일시"])
        check_result = True

    # 이전 페이지 이동
    def btn_previous_page(self):
        global row_num, current_page_num, total_page_num, check_result, search_trigger, date_start, date_end
        if check_result == False:
            self.init_table()
            check_result = True

        if row_num < 39:
            row_num = 0
            current_page_num = 1
        else:
            row_num -= 40
            current_page_num -= 1

        if search_trigger == False:
            sql = "SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts FROM tpn_public_notice WHERE pn_visible = 1 order by pn_date desc limit " + str(row_num) + ", 40"
        else:
            sql = "SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts FROM tpn_public_notice WHERE pn_open_ts >= '" + date_start + "%' AND pn_open_ts <= '" + date_end + "%' AND pn_visible = 1 ORDER BY pn_open_ts LIMIT " + str(row_num) + ", 40"

        cursor = conn.cursor()
        cursor.execute(sql)
        table = self.tableWidget
        table.setRowCount(0)
        for row, form in enumerate(cursor):
            table.insertRow(row)
            for column, item in enumerate(form):
                if (column<9):
                    table.setItem(row, column, QTableWidgetItem(str(item)))

        self.label_3.setText(str(total_page_num)+"페이지 중 " + str(current_page_num) + "페이지")
        self.arrangecolumn()

    # 다음페이지 검색
    def btn_next_page(self):
        global row_num, current_page_num, total_page_num, check_result
        if check_result == False:
            self.init_table()
            check_result = True
        cursor = conn.cursor()
        row_num += 40
        current_page_num += 1
        # sql = "SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts FROM tpn_public_notice order by pn_date desc limit " + str(row_num) + ", 40"
        if search_trigger == False:
            sql = "SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts FROM tpn_public_notice WHERE pn_visible = 1 order by pn_date desc limit " + str(row_num) + ", 40"
        else:
            sql = "SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts FROM tpn_public_notice WHERE pn_open_ts >= '" + date_start + "%' AND pn_open_ts <= '" + date_end + "%' AND pn_visible = 1 ORDER BY pn_open_ts LIMIT " + str(row_num) + ", 40"
        cursor.execute(sql)
        table = self.tableWidget
        table.setRowCount(0)
        for row, form in enumerate(cursor):
            table.insertRow(row)
            for column, item in enumerate(form):
                if (column<9):
                    table.setItem(row, column, QTableWidgetItem(str(item)))

        self.label_3.setText(str(total_page_num)+"페이지 중 " + str(current_page_num) + "페이지")
        self.arrangecolumn()

    # 입찰공고를 검색하기
    def btn_search(self):
        global row_num, total_page_num, current_page_num, check_result, date_start, date_end, search_trigger
        if check_result == False:
            self.init_table()
            check_result = True
        row_num = 0
        current_page_num = 1
        date_start = self.dateEdit_start.date().toString("yyyy-MM-dd") + " 00:00:00"
        date_end = self.dateEdit_end.date().toString("yyyy-MM-dd") + " 23:59:59"
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tpn_public_notice WHERE pn_open_ts >= '" + date_start + "%' AND pn_open_ts <= '" + date_end + "%' AND pn_visible = 1")
        total_num = cursor.fetchone()[0]
        total_page_num = math.ceil(int(total_num) / 40)
        # sql = "SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts FROM tpn_public_notice WHERE pn_open_ts LIKE '" + date_start + "%' OR pn_open_ts LIKE '" + date_end + "%' ORDER BY pn_open_ts LIMIT " + str(row_num) + ", 40"
        sql = "SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts FROM tpn_public_notice WHERE pn_open_ts >= '" + date_start + "%' AND pn_open_ts <= '" + date_end + "%' AND pn_visible = 1 ORDER BY pn_open_ts LIMIT " + str(row_num) + ", 40"
        cursor.execute(sql)
        if cursor.fetchone() == None:
            self.no_result()
        else:
            table = self.tableWidget
            table.setRowCount(0)
            for row, form in enumerate(cursor):
                table.insertRow(row)
                for column, item in enumerate(form):
                    if (column<9):
                        table.setItem(row, column, QTableWidgetItem(str(item)))

            self.label_3.setText(str(total_page_num)+"페이지 중 " + str(current_page_num) + "페이지")
            search_trigger = True
            self.arrangecolumn()



    # # 키워드목록에서 클릭이 발생하면 해당 키워드를 에디트창에 반영
    # def cell_clicked(self, row, col):
    #     # 동작영역을 데이터가 있는 범위내로 한정해야 함
    #     sel_key = self.tableWidget.item(row,col)
    #     if (sel_key):
    #         sel_key = sel_key.text()
    #         print(sel_key)


    # 키워드목록에서 더블클릭이 발생하면
    # 해당 항복의 공고문을 웹브라우저로 호출
    def cell_DBclicked(self, row, col):
        sel_key = self.tableWidget.item(row,0)
        sel_key = sel_key.text()
        cursor = conn.cursor()
        cursor.execute("SELECT pn_url FROM tpn_public_notice WHERE pn_num= %s", (sel_key))
        sel_key = cursor.fetchone()

        if (sel_key):
            sel_key = sel_key[0]
            webbrowser.open(sel_key)

    def radioB_bidE(self):
        self.radioButton_bidE.setChecked(True)

    def arrangecolumn(self):
        table = self.tableWidget
        header = table.horizontalHeader()
        twidth = header.width()
        width = []
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
            width.append(header.sectionSize(column))

        wfactor = twidth / sum(width)
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.Interactive)
            header.resizeSection(int(column), int(width[column]*wfactor))

    def open_folder_path_clicked(self):
        global fname, search_trigger, date_start, date_end
        fname = QFileDialog.getExistingDirectory()
        if search_trigger == False:
            file_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            file_name = date_start.replace(" 00:00:00", "") + ' ~ ' + date_end.replace(" 23:59:59", "")
        fname = fname + '/' + file_name + '.xlsx'
        self.folder_path_showing.setText(fname)
        self.folder_path_showing.setEnabled(False)

    def download_excel(self):
        global fname, search_trigger, date_start, date_end
        cursor = conn.cursor()

        if search_trigger == False:
            sql = "SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts, pn_url FROM tpn_public_notice WHERE pn_visible = 1 ORDER BY pn_date desc"
            cursor.execute(sql)
            db_data = cursor.fetchall()

        else:
            sql = "SELECT pn_num, pn_date, pn_title, pn_method, pn_institution_name, pn_price, pn_bid_start_ts, pn_bid_end_ts, pn_open_ts, pn_url FROM tpn_public_notice WHERE pn_open_ts >= '" + date_start + "%' AND pn_open_ts <= '" + date_end + "%' AND pn_visible = 1 ORDER BY pn_open_ts"
            cursor.execute(sql)
            db_data = cursor.fetchall()

        df = pd.DataFrame(db_data, columns = ["번호","공고/계약일","사업명","계약방법","기관명","금액", "입찰 개시 일시", "입찰 마감 일시", "개찰(입찰) 일시", "URL"])
        df.to_excel(fname)

    def keyPressEvent(self, ev):
        if (ev.key() == Qt.Key_C) and (ev.modifiers() & Qt.ControlModifier):
            self.copySelection()

    def copySelection(self):
        selection = self.tableWidget.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream).writerows(table)
            QApplication.clipboard().setText(stream.getvalue())

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dial = test()
    dial.showMaximized()
    sys.exit(app.exec_())