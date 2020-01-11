#!/usr/bin/python3

#tooltips
# Please read this tutorial on how to prepare your images for use with DeepCreamPy.
# The greater the number of variations, the longer decensoring process will be.

import sys, time, json
from PySide2.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QDesktopWidget, QApplication
from PySide2.QtWidgets import qApp, QApplication, QRadioButton, QPushButton, QTextEdit, QLabel
from PySide2.QtWidgets import QSizePolicy,QMainWindow, QStatusBar, QProgressBar, QComboBox
from PySide2.QtCore import Qt, QObject
from PySide2.QtGui import QFont, QTextCursor
from signals import Signals
from decensor import Decensor
from language.language import Language

class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.signals = Signals()
		self.lang = Language()
		self.initUI()
		self.setSignals()
		self.decensor = Decensor(self)
		self.decensor.lang = self.lang
		self.load_model()

	def initUI(self):

		grid_layout = QGridLayout()
		grid_layout.setSpacing(11)
		self.setLayout(grid_layout)

		#Tutorial
		self.tutorialLabel = QLabel()
		self.tutorialLabel.setText(self.lang.msg_tutorial)
		self.tutorialLabel.setAlignment(Qt.AlignCenter)
		self.tutorialLabel.setFont(QFont('Sans Serif', 13))

		#Censor type group
		# self.censorTypeGroupBox = QGroupBox('Censor Type')
		self.censorTypeGroupBox = QGroupBox(self.lang.censor_type)

		self.barButton = QRadioButton(self.lang.bar_censor)
		self.mosaicButton = QRadioButton(self.lang.mosaic_censor)
		self.barButton.setChecked(True)

		censorLayout = QVBoxLayout()
		censorLayout.addWidget(self.barButton)
		censorLayout.addWidget(self.mosaicButton)
		# censorLayout.addStretch(1)
		self.censorTypeGroupBox.setLayout(censorLayout)

		#Variation count group
		self.variationsGroupBox = QGroupBox(self.lang.number_of_decensor_variations)

		var1Button = QRadioButton('1')
		var2Button = QRadioButton('2')
		var3Button = QRadioButton('4')
		var1Button.setChecked(True)

		varLayout = QVBoxLayout()
		varLayout.addWidget(var1Button)
		varLayout.addWidget(var2Button)
		varLayout.addWidget(var3Button)
		# varLayout.addStretch(1)
		self.variationsGroupBox.setLayout(varLayout)

		#Decensor button
		self.decensorButton = QPushButton(self.lang.button_decensor_your_images)
		self.decensorButton.clicked.connect(self.decensorClicked)
		self.decensorButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

		#Progress message
		# self.progressGroupBox = QGroupBox('Progress')

		self.progressMessage = QTextEdit()
		self.progressCursor = QTextCursor(self.progressMessage.document())
		self.progressMessage.setTextCursor(self.progressCursor)
		self.progressMessage.setReadOnly(True)
		self.progressCursor.insertText(self.lang.msg_first_guide)

		# Progress Bar
		self.statusBar  = QStatusBar(self)
		self.progressBar = QProgressBar()
		self.progressBar.setMinimum(0)
		self.progressBar.setMaximum(100)
		self.progressBar.setValue(0)
		self.statusLabel = QLabel(self.lang.showing_progress)

		self.statusBar.addWidget(self.statusLabel, 1)
		self.statusBar.addWidget(self.progressBar, 2)

		# comboBox for UI langauge Select
		self.statusBar2  = QStatusBar(self)
		self.comboBox_Langauge = QComboBox(self)
		self.comboBox_Langauge.activated.connect(self.set_language)
		for item in self.lang.names:
			self.comboBox_Langauge.addItem(item)
		self.statusLabel2 = QLabel("Language  ", alignment=Qt.AlignRight)
		self.statusBar2.addWidget(self.statusLabel2, 6)
		self.statusBar2.addWidget(self.comboBox_Langauge, 2)

		#put all groups into grid
		# addWidget(row, column, rowSpan, columnSpan)
		grid_layout.addWidget(self.statusBar2, 0,0,1,2)
		grid_layout.addWidget(self.tutorialLabel, 0+1, 0, 1, 2)
		grid_layout.addWidget(self.censorTypeGroupBox, 1+1, 0, 1, 1)
		grid_layout.addWidget(self.variationsGroupBox, 1+1, 1, 1, 1)
		grid_layout.addWidget(self.decensorButton, 2+1, 0, 1, 2)
		grid_layout.addWidget(self.progressMessage, 3+1, 0, 1, 2)
		grid_layout.addWidget(self.statusBar, 4+1, 0, 1, 2)

		#window size settings
		self.resize(900, 600)
		self.center()
		self.setWindowTitle('DeepCreamPy v2.2.0-beta')
		self.show()

	def load_model(self):
		# load model to make able to decensor several times
		self.decensorButton.setEnabled(False)
		self.decensorButton.setText(self.lang.button_while_loading_model)
		self.decensor.start()
		self.decensor.signals = self.signals
		self.progressCursor.insertText(self.lang.msg_while_loading_model)

	def setSignals(self):
		self.signals.update_decensorButton_Text.connect(self.decensorButton.setText)
		self.signals.update_decensorButton_Enabled.connect(self.decensorButton.setEnabled)
		self.signals.update_statusLabel_Text.connect(self.statusLabel.setText)
		self.signals.update_ProgressBar_SET_VALUE.connect(self.progressBar.setValue)
		self.signals.update_ProgressBar_MAX_VALUE.connect(self.progressBar.setMaximum)
		self.signals.update_ProgressBar_MIN_VALUE.connect(self.progressBar.setMinimum)
		# self.signals.insertText_progressCursor.connect(self.progressCursor.insertText)
		self.signals.insertText_progressCursor.connect(self.progressMessage.append)
		self.signals.clear_progressMessage.connect(self.progressMessage.clear)
		self.signals.appendText_progressMessage.connect(self.progressMessage.append)

	def set_language(self):
		# updates all strings in UI to langeuage selected
		name = self.comboBox_Langauge.currentText()
		if self.lang.language_name == name:
			return
		self.lang.language_name = name

		self.tutorialLabel.setText(self.lang.msg_tutorial)
		self.censorTypeGroupBox.setTitle(self.lang.censor_type)
		self.barButton.setText(self.lang.bar_censor)
		self.mosaicButton.setText(self.lang.mosaic_censor)
		self.variationsGroupBox.setTitle(self.lang.number_of_decensor_variations)
		self.statusLabel.setText(self.lang.showing_progress)
		# self.decensorButton.setText(self.lang.button_while_loading_model)

	def decensorClicked(self):
		self.decensorButton.setEnabled(False)
		self.progressMessage.clear()
		self.progressCursor.insertText(self.lang.msg_decensoring_start)

		#https://stackoverflow.com/questions/42349470/pyqt-find-checked-radiobutton-in-a-group
		#set decensor to right settings
		#censor type
		if self.mosaicButton.isChecked:
			self.decensor.is_mosaic = False
		else:
			self.decensor.is_mosaic = True

		#variations count
		variationsElements = self.variationsGroupBox.children()
		variationsButtons = [elem for elem in variationsElements if isinstance(elem, QRadioButton)]
		for vb in variationsButtons:
			if vb.isChecked():
				variations = int(vb.text())
		self.decensor.variations = variations

		self.decensorButton.setEnabled(False)
		self.decensor.start()

	# centers the main window
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

if __name__ == '__main__':
	import os
	# if OS is "Windows"
	if os.name == 'nt':
		import PySide2
		pyqt = os.path.dirname(PySide2.__file__)
		QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())
