from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Scatter Tool UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Object Tool")
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        self.setMaximumHeight(400)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.title_lbl = QtWidgets.QLabel("Scatter Object Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.scale_lay = self._create_random_scale_ui()
        self.rotation_lay = self._create_random_rotation_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.scale_lay)
        self.main_lay.addLayout(self.rotation_lay)
        self.main_lay.addStretch()
        self.setLayout(self.main_lay)

    def _create_random_scale_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_check_btn = QtWidgets.QCheckBox()
        self.scale_lbl = QtWidgets.QLabel("Randomize Scale:")
        self.min_lbl = QtWidgets.QLabel("min")
        self.min_lbl.setStyleSheet("font: 10px")
        self.min_le = QtWidgets.QLineEdit("0.0")
        self.min_le.setFixedWidth(40)
        self.max_lbl = QtWidgets.QLabel("max")
        self.max_le = QtWidgets.QLineEdit("1.0")
        self.max_le.setFixedWidth(40)
        #self.scale_le.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.scale_lbl, 0, 0)
        layout.addWidget(self.scale_check_btn, 0, 1)
        layout.addWidget(self.min_lbl, 1, 2)
        layout.addWidget(self.min_le, 1, 3)
        layout.addWidget(self.max_lbl, 1, 4)
        layout.addWidget(self.max_le, 1, 5)
        return layout

    def _create_random_rotation_ui(self):
        layout = QtWidgets.QGridLayout()
        self.rotate_lbl = QtWidgets.QLabel("Randomize Rotation:")
        self.rotate_check_btn = QtWidgets.QCheckBox()
        self.x_min_le = QtWidgets.QLineEdit("0.0")
        self.x_min_le.setFixedWidth(40)
        self.x_max_le = QtWidgets.QLineEdit("360.0")
        self.x_max_le.setFixedWidth(40)
        self.y_min_le = QtWidgets.QLineEdit("0.0")
        self.y_min_le.setFixedWidth(40)
        self.y_max_le = QtWidgets.QLineEdit("360.0")
        self.y_max_le.setFixedWidth(40)
        self.z_min_le = QtWidgets.QLineEdit("0.0")
        self.z_min_le.setFixedWidth(40)
        self.z_max_le = QtWidgets.QLineEdit("360.0")
        self.z_max_le.setFixedWidth(40)
        layout.addWidget(self.rotate_lbl, 2, 0)
        layout.addWidget(self.rotate_check_btn, 2, 1)
        layout.addWidget(self.x_min_le, 3, 2)
        layout.addWidget(self.x_max_le, 3, 3)
        layout.addWidget(self.y_min_le, 3, 5)
        layout.addWidget(self.y_max_le, 3, 6)
        layout.addWidget(self.z_min_le, 3, 8)
        layout.addWidget(self.z_max_le, 3, 9)
        return layout