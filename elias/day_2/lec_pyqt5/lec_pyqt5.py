# pyqt5는 python 12 or 13에서 정상설치 안됨

import inspect
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
import logging
from datetime import datetime
import os
import sys
import time

from main_ui import Ui_Dialog as Main_Ui

DISPLAY_LOG_IN_TERMINAL = True

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s (%(funcName)20s:%(lineno)4d) [%(levelname)s]: %(message)s')

# Print log in terminal
if DISPLAY_LOG_IN_TERMINAL is True:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

# Write log in file
today = datetime.now().strftime('%Y_%m_%d')
filename = f'{today}.log'

# If file exist, remove it
if os.path.isfile(filename):
    os.remove(filename)

file_handler = logging.FileHandler(filename)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class MainDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)

        self.main_ui = Main_Ui()
        self.main_ui.setupUi(self)
        self.setWindowTitle('QT Sample Dialog')

        self.my_thread = None

        # Line Edit
        self.main_ui.btn_get_le.clicked.connect(self.get_le)
        self.main_ui.btn_set_le.clicked.connect(self.set_le)

        # Exit
        self.main_ui.btn_exit.clicked.connect(self.close_dialog)

        # Thread
        self.main_ui.btn_start.clicked.connect(self.start_thread)
        self.main_ui.btn_stop.clicked.connect(self.stop_thread)

        # Spin Box
        self.main_ui.spinBox.setSingleStep(1)
        self.main_ui.btn_get_sp.clicked.connect(self.get_sp)
        self.main_ui.btn_set_sp.clicked.connect(self.set_sp)

        # Radio Button
        self.main_ui.btn_get_rb.clicked.connect(self.get_rb)
        self.main_ui.btn_set_rb.clicked.connect(self.set_rb)

        # List Widget
        self.lw_count = 0
        self.main_ui.btn_add_list.clicked.connect(self.add_lw)
        self.main_ui.btn_remove_list.clicked.connect(self.delete_lw)
        self.main_ui.listWidget.clicked.connect(self.select_row_lw)
        self.main_ui.btn_get_list.clicked.connect(self.get_list_lw)

        # Table Widget
        self.tableWidgetInit()
        self.main_ui.btn_get_tablewidget_item.clicked.connect(self.get_item)

        # MessageBox
        self.main_ui.btn_information.clicked.connect(self.box_info)
        self.main_ui.btn_warning.clicked.connect(self.box_warning)
        self.main_ui.btn_question.clicked.connect(self.box_question)

        # Disable, Enable
        self.main_ui.btn_enable.clicked.connect(self.enable_exit_button)
        self.main_ui.btn_disable.clicked.connect(self.disable_exit_button)

        # Clear Log
        self.main_ui.btn_clear_log.clicked.connect(self.clear_log)

        # Combobox
        self.main_ui.btn_add_element.clicked.connect(self.add_element)
        self.main_ui.btn_delete_element.clicked.connect(self.delete_element)
        self.main_ui.btn_get_element.clicked.connect(self.get_element)
        self.main_ui.btn_get_all_element.clicked.connect(self.get_all_element)

        # FileDialog
        self.main_ui.btn_getopenfilename.clicked.connect(self.get_openfilename)
        self.main_ui.btn_getopenfilenames.clicked.connect(self.get_openfilenames)
        self.main_ui.btn_getsavefilename.clicked.connect(self.get_savefilename)

    def start_thread(self):
        try:
            max_count = 100
            self.main_ui.progressBar.setMinimum(0)
            self.main_ui.progressBar.setMaximum(max_count)
            self.main_ui.progressBar.setValue(0)

            interval = 0.1
            self.my_thread = ProcessThread(None, interval, max_count)
            self.my_thread.logSignal.connect(self.add_log)
            self.my_thread.stopSignal.connect(self.thread_is_stopped)
            self.my_thread.countSignal.connect(self.count)
            self.my_thread.start()

            self.set_enable_buttons(False)
        except Exception as e:
            print('--> Exception is "%s" (Line: %s)' % (e, sys.exc_info()[-1].tb_lineno))

    def stop_thread(self):
        if self.my_thread is not None:
            self.my_thread.stop()

    @pyqtSlot(str)
    def add_log(self, message):
        now = datetime.now()
        now = now.strftime('%H:%M:%S')

        # 호출된 함수와 라인번호 가져오기
        curframe = inspect.currentframe()
        callframe = inspect.getouterframes(curframe, 2)
        func_name = callframe[1].function
        line_no = callframe[1].lineno

        log_message = f'[{now}]: {message} <{func_name}:{line_no}>'
        file_message = f'{message} <{func_name}:{line_no}>'
        self.main_ui.tb_log.append(log_message)
        logger.info(file_message)

    @pyqtSlot(int)
    def count(self, count):
        self.add_log(f'ProgressBar Value: {count}')
        self.main_ui.progressBar.setValue(count)

    @pyqtSlot()
    def thread_is_stopped(self):
        self.set_enable_buttons(True)
        self.main_ui.progressBar.setValue(0)

    def set_enable_buttons(self, enable):
        self.main_ui.btn_start.setEnabled(enable)
        self.main_ui.btn_stop.setEnabled(not enable)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            pass

    def close_dialog(self):
        self.close()
        # self.exit(0)

    def get_le(self):
        value = self.main_ui.lineEdit.text()
        self.add_log(f'LineEdit: {value}')

    def set_le(self):
        self.main_ui.lineEdit.setText('World')

    ############################################################################################
    # FileDailog
    def get_openfilename(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '', 'All File(*);;Excel File(*.xlsx)')
        if filename[0]:
            self.add_log(filename[0])
            self.add_log(filename[1])

    def get_openfilenames(self):
        filename = QFileDialog.getOpenFileNames(self, 'Open File', '', 'All File(*);;Excel File(*.xlsx)')
        if filename[0]:
            for file in filename[0]:
                self.add_log(file)
            self.add_log(filename[1])

    def get_savefilename(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'All File(*);;Excel File(*.xlsx)')
        if filename[0]:
            self.add_log(filename[0])
            self.add_log(filename[1])

    ############################################################################################
    # Combobox
    def add_element(self):
        count = self.main_ui.comboWidget.count() + 1
        self.main_ui.comboWidget.addItem(f'Item {count}')

    def delete_element(self):
        current_index = self.main_ui.comboWidget.currentIndex()
        self.main_ui.comboWidget.removeItem(current_index)

    def get_element(self):
        current_index = self.main_ui.comboWidget.currentIndex()
        self.add_log(self.main_ui.comboWidget.itemText(current_index))

    def get_all_element(self):
        element_list = [self.main_ui.comboWidget.itemText(i) for i in range(self.main_ui.comboWidget.count())]
        self.add_log(element_list)

    ####################################################################
    # Clear Log
    def clear_log(self):
        self.main_ui.tb_log.clear()

    ####################################################################
    # Enable/Disable Button
    def enable_exit_button(self):
        self.main_ui.btn_exit.setEnabled(True)
        self.main_ui.gb_le.setEnabled(True)

    def disable_exit_button(self):
        self.main_ui.btn_exit.setEnabled(False)
        self.main_ui.gb_le.setEnabled(False)

    ######################################################################################
    # MessageBox
    def box_question(self):
        # result = QMessageBox.question(self, 'Question', 'Do you delete?', QMessageBox.Ok, QMessageBox.Cancel)
        result = QMessageBox.question(self, 'Question', 'Do you delete?', QMessageBox.Yes, QMessageBox.No)
        if result == QMessageBox.Yes:
            self.add_log('Yes')
        else:
            self.add_log('No')

    def box_warning(self):
        result = QMessageBox.warning(self, 'Warning', 'Wrong Information', QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.add_log('Yes')
        else:
            self.add_log('No')

    def box_info(self):
        result = QMessageBox.information(self, 'Information', 'Success', QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.add_log('Yes')
        else:
            self.add_log('No')

    ###########################################################################################
    # TableWidget
    def tableWidgetInit(self):
        columns = ['Name', 'Address', 'Age']
        self.main_ui.tableWidget.setColumnCount(len(columns))
        self.main_ui.tableWidget.setHorizontalHeaderLabels(columns)
        self.main_ui.tableWidget.setColumnWidth(0, 89)
        self.main_ui.tableWidget.setColumnWidth(1, 100)
        self.main_ui.tableWidget.setColumnWidth(2, 80)

        table_data = [['Kim', 'Seoul', '20'],
                      ['Park', 'Busan', '20'],
                      ['Lee', 'Daegu', '20']]
        self.main_ui.tableWidget.setRowCount(len(table_data))

        for i, data in enumerate(table_data):
            for j in range(len(data)):
                item = QTableWidgetItem(data[j])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.main_ui.tableWidget.setItem(i, j, item)

    def get_item(self):
        row = int(self.main_ui.le_row.text())
        column = int(self.main_ui.le_column.text())
        self.add_log(f'TableWidget Item[{row},{column}]: {self.main_ui.tableWidget.item(row, column).text()}')

    ###########################################################################################
    # ListWidget
    def add_lw(self):
        self.lw_count += 1
        self.main_ui.listWidget.addItem(f'Hello: {self.lw_count}')

    def delete_lw(self):
        current_row = self.main_ui.listWidget.currentRow()
        self.main_ui.listWidget.takeItem(current_row)

    def select_row_lw(self):
        current_row = self.main_ui.listWidget.currentRow()
        self.add_log(f'CurrentRow: {current_row}')

    def get_list_lw(self):
        items = []
        for i in range(self.main_ui.listWidget.count()):
            items.append(self.main_ui.listWidget.item(i).text())
        self.add_log(f'ListWidget: {items}')

    ###########################################################################################
    # SpinBox
    def get_sp(self):
        value = self.main_ui.spinBox.value()
        self.add_log(f'SpinBox: {value}')

    def set_sp(self):
        self.main_ui.spinBox.setValue(10)

    ###########################################################################################
    # RadioButton
    def get_rb(self):
        value = self.main_ui.radioButton_a.isChecked()
        self.add_log(f'RadioButton A: {value}')
        value = self.main_ui.radioButton_b.isChecked()
        self.add_log(f'RadioButton B: {value}')
        value = self.main_ui.checkBox.isChecked()
        self.add_log(f'CheckBox: {value}')

    def set_rb(self):
        self.main_ui.radioButton_a.setChecked(True)
        self.main_ui.radioButton_b.setChecked(False)
        self.main_ui.checkBox.setChecked(True)

class ProcessThread(QThread):
    logSignal = pyqtSignal(str)
    countSignal = pyqtSignal(int)
    stopSignal = pyqtSignal()

    def __init__(self, param, interval=0.5, max_count=100):
        super(self.__class__, self).__init__()
        # super().__init__()
        self.param = param
        self.isRunning = True
        self.interval = interval
        self.max_count = max_count

    def run(self):
        self.logSignal.emit('Thread is started')
        count = 1

        while self.isRunning:
            time.sleep(self.interval)
            self.countSignal.emit(count)
            count += 1

            if count > self.max_count:
                break

        self.logSignal.emit('Thread is dead')
        self.stopSignal.emit()

    def stop(self):
        self.isRunning = False
        self.logSignal.emit('Thread is stopping...')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MainDialog()
    myWindow.show()
    app.exec()

























