
# !/usr/bin/env python
# coding: utf-8

import time
import datetime
import os
import math

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from compile import *

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.run_button=None
		self.code_area=None
		self.result=None
		self.current_file=None
		self.setMinimumSize(QSize(200,100))
		self.draw_widgets()
	def file_new(self):
		self.current_file=None
		# self.code_area.setPlainText("# Anand Ramasamy")
		self.code_area.setPlainText("")
	def file_open(self):
		options=QFileDialog.Options()
		options |=QFileDialog.DontUseNativeDialog
		fileName,_=QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
		if fileName:
			self.current_file=fileName
			CODE=open(fileName,"r").read()
			self.code_area.setPlainText(CODE)
	def file_save(self):
		if self.current_file==None:
			options=QFileDialog.Options()
			options |=QFileDialog.DontUseNativeDialog
			fileName,_=QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*)", options=options)
			if fileName:
				self.current_file=fileName
		if self.current_file!=None:
			CODE=self.code_area.toPlainText()
			fobj=open(self.current_file,"w")
			fobj.write(CODE)
			fobj.close()
	def compile_code(self):
		CODE=self.code_area.toPlainText()
		# run
		compiler=Compiler(CODE)
		compiler.run()
		result_string=compiler.result_text_for_label
		self.result.setPlainText(result_string)
		# self.result.setDisabled(True)
	def draw_widgets(self):
		#
		self.statusBar()
		#
		newAction=QAction(QIcon('exit.png'),'&New',self)
		newAction.setShortcut('Ctrl+N')
		newAction.setStatusTip('New File')
		newAction.triggered.connect(self.file_new)
		#
		openAction=QAction(QIcon('exit.png'),'&Open',self)
		openAction.setShortcut('Ctrl+O')
		openAction.setStatusTip('Open File')
		openAction.triggered.connect(self.file_open)
		#
		SaveAction=QAction(QIcon('exit.png'),'&Save',self)
		SaveAction.setShortcut('Ctrl+S')
		SaveAction.setStatusTip('Save File')
		SaveAction.triggered.connect(self.file_save)
		#
		exitAct=QAction(QIcon('exit.png'),'&Exit',self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(qApp.quit)
		#
		file_bar=self.menuBar()
		fileMenu=file_bar.addMenu('&File')
		fileMenu.addAction(newAction)
		fileMenu.addAction(openAction)
		fileMenu.addAction(SaveAction)
		fileMenu.addAction(exitAct)
		#
		runAct=QAction(QIcon('exit.png'),'&Run',self)
		runAct.setShortcut('Alt+Return')
		runAct.setStatusTip('Run Code')
		runAct.triggered.connect(self.compile_code)
		#
		run_bar=self.menuBar()
		fileMenu=run_bar.addMenu('&Run')
		fileMenu.addAction(runAct)
		#
		self.code_area=QPlainTextEdit(self)
		# text="# Anand Ramasamy"
		text=""
		self.code_area.insertPlainText(text)
		self.code_area.move(5,50)
		self.code_area.resize(595,500)
		#
		self.result=QPlainTextEdit(self)
		self.result.setToolTip('Output Terminal')
		self.result.insertPlainText("")
		self.result.move(600,50)
		self.result.resize(340,500)
		# self.result.setDisabled(True)
		#
		self.setGeometry(100,100,950,550)
		self.setWindowTitle('Glitch IDE')
		self.show()


def main():
	app=QApplication(sys.argv)
	ex=App()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()


#---------
