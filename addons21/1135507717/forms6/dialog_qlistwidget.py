# Form implementation generated from reading ui file './dialog_qlistwidget.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(684, 535)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.listWidget = My_List_Widget(Dialog)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.CurrentChanged|QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked|QtWidgets.QAbstractItemView.EditTrigger.EditKeyPressed|QtWidgets.QAbstractItemView.EditTrigger.SelectedClicked)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pb_add_empty = QtWidgets.QPushButton(Dialog)
        self.pb_add_empty.setObjectName("pb_add_empty")
        self.horizontalLayout_2.addWidget(self.pb_add_empty)
        self.pb_edit_tag = QtWidgets.QPushButton(Dialog)
        self.pb_edit_tag.setObjectName("pb_edit_tag")
        self.horizontalLayout_2.addWidget(self.pb_edit_tag)
        self.pb_search = QtWidgets.QPushButton(Dialog)
        self.pb_search.setObjectName("pb_search")
        self.horizontalLayout_2.addWidget(self.pb_search)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Edit tags</span> (<span style=\" font-weight:600;\">Basic Mode </span>that handles many tags with <br/>scrolling - the keys Return&amp;Space keys are not handled,<br/>see the add-on config)</p></body></html>"))
        self.pb_add_empty.setText(_translate("Dialog", "add empty line"))
        self.pb_edit_tag.setText(_translate("Dialog", "edit tag for current line"))
        self.pb_search.setText(_translate("Dialog", "search"))
from ..my_list_widget import My_List_Widget
