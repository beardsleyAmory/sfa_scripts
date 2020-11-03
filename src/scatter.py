import random as rand

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
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.scale_lay)
        self.main_lay.addLayout(self.rotation_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)
        self._create_connections()

    def _create_random_scale_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_check_btn = QtWidgets.QCheckBox()
        self.scale_lbl = QtWidgets.QLabel("Randomize Scale:")
        self.options_lay = self._min_max_scale_options_ui()
        #self.scale_le.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.scale_lbl, 0, 0)
        layout.addWidget(self.scale_check_btn, 0, 1)
        layout.addLayout(self.options_lay, 1, 2)
        return layout

    def _min_max_scale_options_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_min_lbl = QtWidgets.QLabel("min")
        self.scale_min_lbl.hide()
        self.scale_min_le = QtWidgets.QLineEdit("0.0")
        self.scale_min_le.setFixedWidth(40)
        self.scale_min_le.hide()
        self.scale_max_lbl = QtWidgets.QLabel("max")
        self.scale_max_lbl.hide()
        self.scale_max_le = QtWidgets.QLineEdit("1.0")
        self.scale_max_le.setFixedWidth(40)
        self.scale_max_le.hide()
        layout.addWidget(self.scale_min_lbl, 1, 2)
        layout.addWidget(self.scale_min_le, 1, 3)
        layout.addWidget(self.scale_max_lbl, 1, 4)
        layout.addWidget(self.scale_max_le, 1, 5)
        return layout

    def _create_random_rotation_ui(self):
        layout = QtWidgets.QGridLayout()
        self.rotate_lbl = QtWidgets.QLabel("Randomize Rotation:")
        self.rotate_check_btn = QtWidgets.QCheckBox()
        self.x_min_le = QtWidgets.QLineEdit("0.0")
        self.x_min_le.setFixedWidth(40)
        self.x_min_le.hide()
        self.x_max_le = QtWidgets.QLineEdit("360.0")
        self.x_max_le.setFixedWidth(40)
        self.x_max_le.hide()
        self.y_min_le = QtWidgets.QLineEdit("0.0")
        self.y_min_le.setFixedWidth(40)
        self.y_min_le.hide()
        self.y_max_le = QtWidgets.QLineEdit("360.0")
        self.y_max_le.setFixedWidth(40)
        self.y_max_le.hide()
        self.z_min_le = QtWidgets.QLineEdit("0.0")
        self.z_min_le.setFixedWidth(40)
        self.z_min_le.hide()
        self.z_max_le = QtWidgets.QLineEdit("360.0")
        self.z_max_le.setFixedWidth(40)
        self.z_max_le.hide()
        layout.addWidget(self.rotate_lbl, 2, 0)
        layout.addWidget(self.rotate_check_btn, 2, 1)
        layout.addWidget(self.x_min_le, 3, 2)
        layout.addWidget(self.x_max_le, 3, 3)
        layout.addWidget(self.y_min_le, 3, 5)
        layout.addWidget(self.y_max_le, 3, 6)
        layout.addWidget(self.z_min_le, 3, 8)
        layout.addWidget(self.z_max_le, 3, 9)
        return layout

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Apply")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    def _create_connections(self):
        self.scale_check_btn.stateChanged.connect(self._show_scale_options)
        self.rotate_check_btn.stateChanged.connect(self._show_rotate_options)
        self.scatter_btn.clicked.connect(self._create_scatter_effect)

    @QtCore.Slot()
    def _show_rotate_options(self):
        if self.rotate_check_btn.isChecked():
            self.x_min_le.show()
            self.x_max_le.show()
            self.y_min_le.show()
            self.y_max_le.show()
            self.z_min_le.show()
            self.z_max_le.show()
        else:
            self.x_min_le.hide()
            self.x_max_le.hide()
            self.y_min_le.hide()
            self.y_max_le.hide()
            self.z_min_le.hide()
            self.z_max_le.hide()

    @QtCore.Slot()
    def _show_scale_options(self):
        if self.scale_check_btn.isChecked():
            self.scale_min_lbl.show()
            self.scale_min_le.show()
            self.scale_max_lbl.show()
            self.scale_max_le.show()
        else:
            self.scale_min_lbl.hide()
            self.scale_min_le.hide()
            self.scale_max_lbl.hide()
            self.scale_max_le.hide()

    def _create_scatter_effect(self):
        selection = cmds.ls(sl=True, fl=True)
        vertices = cmds.filterExpand(selection, selectionMask=31,
                                        expand=True)

        object_to_instance = selection[0]

        """if not vertices:
            object_to_convert = selection[1]
            vertices = cmds.ls(object_to_convert.vtx[*], flatten=True)
            print(vertices)"""

        if cmds.objectType(object_to_instance) == 'transform':

            for vertex in vertices:
                new_instance = cmds.instance(object_to_instance)[0]
                position = cmds.pointPosition(vertex, w=1)
                cmds.move(position[0], position[1], position[2], new_instance, a=1, ws=1)
                if self.scale_check_btn.isChecked():
                    inst_scale = rand.uniform(float(self.scale_min_le.text()), float(self.scale_max_le.text()))
                    cmds.scale(inst_scale, inst_scale, inst_scale, new_instance, a=1, ws=1)

                if self.rotate_check_btn.isChecked():
                    inst_rotation = [
                        rand.uniform(float(self.x_min_le.text()), float(self.x_max_le.text())),
                        rand.uniform(float(self.y_min_le.text()), float(self.y_max_le.text())),
                        rand.uniform(float(self.z_min_le.text()), float(self.z_max_le.text()))]
                    cmds.rotate(inst_rotation[0], inst_rotation[1],
                                inst_rotation[2], new_instance, a=1, ws=1)
