__author__ = 'Varun S S'
from PyQt4.QtCore import pyqtSignal,QObject,pyqtSlot,QString
from PyQt4 import QtGui, uic, QtCore

import data
import math
import req
import config
import mission
import analysis
import pyqtgraph

from gui import Window3

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        self.create_objects()

        # self.requirements()
        # self.mission()

        self.mw = Window3.Ui_MainWindow()
        super(MyWindow, self).__init__()
        self.mw.setupUi(self)
        self.update_gui()

        self.update_objects()


        #self.connect(self.mw.pass_slider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.change_gross_wt)

        self.show()

    def update_gui(self):
        self.requirements()
        self.mission()
    def create_objects(self):
        self.req1 = req.AircraftRequirements()
        self.aircraft1 = config.Aircraft()

        self.mission1 = mission.MissionDef()

        # for i in range(self.mission1.num_segments):
        #     self.mission1.segments[i].ref=i
        #     if self.mission1.segments[i].type==3:
        #        self.mission1.segments[i].range=self.req1.design_range
        #     elif self.mission1.segments[i].type==4:
        #         self.mission1.segments[i].time=self.req1.loiter_time

    def update_objects(self):
        self.req1.update_req(self.aircraft1)
        self.aircraft1.update_config()
        self.mission1.update_mission()

    def requirements(self):
        self.req_set_defaults()
        self.req_unit_conversions()
        self.req_data_input()

    def mission(self):
        self.miss_set_defaults()
        self.miss_segments()
        self.miss_unit_conversions()
        self.miss_data_inputs()
        self.mission_profile()
        self.connect(self.mw.add_seg_push, QtCore.SIGNAL(_fromUtf8("clicked()")), self.add_seg_push)
        self.connect(self.mw.rem_seg_push, QtCore.SIGNAL(_fromUtf8("clicked()")), self.rem_seg_push)
    def req_set_defaults(self):

        # Requirements Tab
        self.mw.des_rang_inp.setText(QString.number(self.req1.design_range))
        self.mw.des_rang_payload_inp.setText(QString.number(self.req1.des_rang_payload))
        self.mw.serv_ceil_inp.setText(QString.number(self.req1.service_ceil))
        self.mw.roc_inp.setText(QString.number(self.req1.roc))
        self.mw.cruise_m_inp.setText(QString.number(self.req1.cruise_mach))
        self.mw.tod_land_inp.setText(QString.number(self.req1.to_distance_land))
        self.mw.tod_water_inp.setText(QString.number(self.req1.to_distance_water))
        self.mw.lan_land_inp.setText(QString.number(self.req1.la_distance_land))
        self.mw.lan_water_inp.setText(QString.number(self.req1.la_distance_water))
        self.mw.max_run_alt_inp.setText(QString.number(self.req1.max_run_alt))
        self.mw.inst_inp.setText(QString.number(self.req1.inst_turn))
        self.mw.sus_inp.setText(QString.number(self.req1.sus_turn))
        self.mw.bank_ang_inp.setText(QString.number(self.req1.bank_ang))
        self.mw.fuel_res_inp.setText(QString.number(self.req1.fuel_res_rang))
        self.mw.pass_inp.setText(QString.number(self.req1.pass_num))
        self.mw.cargo_inp.setText(QString.number(self.req1.cargo_wt))
        self.mw.pay_wt_inplab.setText(QString.number(analysis.calc_payload(self.req1)))
        self.mw.atm_alt_lab.setText("Atmospheric Compliance at "+QString.number(self.req1.max_run_alt)+" m")

        # Mission Definition Tab

        self.mw.miss_nam_inp.setText(self.mission1.name)
        self.mw.alt_beg_inp.setText(QString.number(self.mission1.segments[0].y_pos_start))
        self.mw.rang_seg_inp.setText(QString.number(self.mission1.segments[0].range))
        self.mw.ht_seg_inp.setText(QString.number(self.mission1.segments[0].height))
        self.mw.time_seg_inp.setText(QString.number(self.mission1.segments[0].time))

    def req_unit_conversions(self):
        self.connect(self.mw.des_rang_km_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.des_rang_km_comb)
        self.connect(self.mw.des_rang_payload_kg_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.des_rang_payload_kg_comb)
        self.connect(self.mw.ser_ceil_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.ser_ceil_m_comb)
        self.connect(self.mw.roc_mpers_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.roc_mpers_comb)

        self.connect(self.mw.tod_lan_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.tod_lan_m_comb)
        self.connect(self.mw.tod_water_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.tod_water_m_comb)
        self.connect(self.mw.lan_land_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.lan_land_m_comb)
        self.connect(self.mw.lan_water_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.lan_water_m_comb)
        self.connect(self.mw.max_run_alt_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.max_run_alt_m_comb)

        self.connect(self.mw.inst_degpers_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.inst_degpers_comb)
        self.connect(self.mw.sus_degpers_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.sus_degpers_comb)
        self.connect(self.mw.bank_ang_deg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.bank_ang_comb)

        self.connect(self.mw.fuel_res_km_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.fuel_res_km_comb)
        self.connect(self.mw.cargo_kg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.cargo_kg_comb)

    def req_data_input(self):
        self.connect(self.mw.des_rang_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.des_rang_inp)
        self.connect(self.mw.des_rang_payload_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.des_rang_payload_inp)
        self.connect(self.mw.serv_ceil_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.serv_ceil_inp)
        self.connect(self.mw.roc_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.roc_inp)
        self.connect(self.mw.cruise_m_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.cruise_m_inp)

        self.connect(self.mw.tod_land_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.tod_land_inp)
        self.connect(self.mw.tod_water_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.tod_water_inp)
        self.connect(self.mw.lan_land_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.lan_land_inp)
        self.connect(self.mw.lan_water_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.lan_water_inp)
        self.connect(self.mw.max_run_alt_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.max_run_alt_inp)

        self.connect(self.mw.inst_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.inst_inp)
        self.connect(self.mw.sus_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.sus_inp)
        self.connect(self.mw.bank_ang_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.bank_ang_inp)

        self.connect(self.mw.fuel_res_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.fuel_res_inp)
        self.connect(self.mw.pass_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.pass_inp)
        self.connect(self.mw.cargo_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.cargo_inp)

        # Spin boxes
        self.connect(self.mw.roc_isa_t_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.roc_isa_t_sb)
        self.connect(self.mw.run_msl_isa_t_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.run_msl_isa_t_sb)
        self.connect(self.mw.run_alt_isa_t_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.run_alt_isa_t_sb)

        # Combo Boxes
        self.connect(self.mw.set_req_push,QtCore.SIGNAL(_fromUtf8("clicked()")),self.set_req_push)
        #self.connect(self.mw.reg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.reg_comb)

    def miss_set_defaults(self):
        self.counter = 0
        self.mw.miss_nam_inp.setText(self.mission1.name)
        self.mw.alt_beg_inp.setText(QString.number(self.mission1.segments[self.counter].y_pos_start))

    def miss_segments(self):
        i = self.counter % 6
        self.mw.typ_seg_comb.setCurrentIndex(i)
        self.mw.rang_seg_inp.setText(QString.number(self.mission1.segments[self.counter].range))
        self.mw.ht_seg_inp.setText(QString.number(self.mission1.segments[self.counter].height))
        self.mw.time_seg_inp.setText(QString.number(self.mission1.segments[self.counter].time))

    def miss_data_inputs(self):
        self.connect(self.mw.miss_nam_inp,QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),self.miss_nam_inp)
        self.connect(self.mw.alt_beg_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.alt_beg_inp)

        self.connect(self.mw.typ_seg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.typ_seg_comb)
        self.connect(self.mw.rang_seg_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.rang_seg_inp)
        self.connect(self.mw.ht_seg_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.ht_seg_inp)
        self.connect(self.mw.time_seg_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.time_seg_inp)

        self.connect(self.mw.ana_miss_push, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ana_miss_push)



    def miss_unit_conversions(self):
        self.connect(self.mw.alt_beg_seg_m_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.alt_beg_seg_m_comb)
        self.connect(self.mw.rang_seg_m_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.rang_seg_m_comb)
        self.connect(self.mw.ht_seg_m_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.ht_seg_m_comb)
        self.connect(self.mw.time_seg_hr_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.time_seg_hr_comb)

    def mission_profile(self):
        self.mw.time_seg_inp.setDisabled(True)
        self.profile = self.mw.mission_graphics
        w = self.profile.width()
        h = self.profile.height()
        self.x1=0
        self.y1=0
        self.x2=0
        self.y2=0
        self.horiz_pos = w/2
        self.vert_pos = h*2
        self.current_horiz = -w/2
        self.current_vert = (h/2 - self.vert_pos)
        self.scene = QtGui.QGraphicsScene()
        self.lines = []
    # Push Buttons
    @pyqtSlot()
    def add_seg_push(self):
        self.mission1.segments[self.counter].type = self.mw.typ_seg_comb.currentText()
        self.draw_segment()
        self.counter += 1
        if self.counter >= self.mission1.segments_num:
            self.mission1.segments.append(mission.MissionPhase())
            self.mission1.segments_num += 1
        self.miss_segments()

    @pyqtSlot()
    def rem_seg_push(self):
        if self.counter == 0:
            pass
        else:
            self.counter -= 1
            self.mission1.segments_num -= 1
            self.delete_segment()
            self.miss_segments()

    @pyqtSlot()
    def ana_miss_push(self):
        self.update_objects()
        analysis.class1_estimation(self.req1,self.aircraft1,self.mission1)

        print "After Analysis", self.aircraft1.gross_weight

    # Graphics View
    def delete_segment(self):
        self.lines[self.counter].setLine(0,0,0,0)
        phase = self.mission1.segments[self.counter].type
        if phase == "Takeoff":
            self.current_horiz = self.current_horiz - self.horiz_pos/2
        elif phase == "Climb":
            self.current_horiz = self.current_horiz - self.horiz_pos/2
            self.current_vert = self.current_vert + self.vert_pos
        elif phase == "Cruise":
            self.current_horiz = self.current_horiz - self.horiz_pos
        elif phase == "Loiter":
            self.current_horiz = self.current_horiz - self.horiz_pos/4
            self.current_vert = self.current_vert - self.vert_pos/2
        elif phase == "Descent":
            self.current_horiz = self.current_horiz - self.horiz_pos/4
            self.current_vert = self.current_vert - self.vert_pos/2
        elif phase == "Landing":
            self.current_horiz = self.current_horiz - self.horiz_pos/2
        self.scene.removeItem(self.lines[self.counter])

    def draw_segment(self):
        self.lines.append(QtGui.QGraphicsLineItem())
        phase = self.mission1.segments[self.counter].type

        if phase == "Takeoff":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/2
            self.y1 = self.current_vert
            self.y2 = self.current_vert
            # print self.x1
            # print
        elif phase == "Climb":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/2
            self.y1 = self.current_vert
            self.y2 = self.current_vert - self.vert_pos
        elif phase == "Cruise":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos
            self.y1 = self.current_vert
            self.y2 = self.current_vert
        elif phase == "Loiter":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/4
            self.y1 = self.current_vert
            self.y2 = self.current_vert + self.vert_pos/2
        elif phase == "Descent":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/4
            self.y1 = self.current_vert
            self.y2 = self.current_vert + self.vert_pos/2
        elif phase == "Landing":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/2
            self.y1 = self.current_vert
            self.y2 = self.current_vert
        self.lines[self.counter].setLine(self.x1,self.y1,self.x2,self.y2)
        self.current_horiz = self.x2
        self.current_vert = self.y2

        self.scene.addItem(self.lines[self.counter])
        self.profile.setScene(self.scene)

    # Data Input Slots

    # Requirements Tab
    @pyqtSlot()
    def des_rang_inp(self, text):
        if self.isfloat(text):
            if self.mw.des_rang_km_comb.currentText() == "km":
                self.req1.design_range = float(text)
            elif self.mw.des_rang_km_comb.currentText() == "mi":
                self.req1.design_range = float(text)/data.Conversion.KM_2_MI
            else:
                self.req1.design_range = float(text)/data.Conversion.KM_2_NM
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.des_rang_lab.text())
            self.mw.des_rang_inp.setText("0")
            self.req1.design_range = 0
            input_warn.exec_()

    @pyqtSlot()
    def des_rang_payload_inp(self, text):
        if self.isfloat(text):
            if self.mw.des_rang_payload_kg_comb.currentText() == "kg":
                self.req1.des_rang_payload = float(text)
            else:
                self.req1.des_rang_payload = data.Conversion.LB_2_KG*float(text)
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.des_rang_payload_lab.text())
            self.mw.des_rang_payload_inp.setText("0")
            self.req1.des_rang_payload = 0
            input_warn.exec_()

    @pyqtSlot()
    def serv_ceil_inp(self, text):
        if self.isfloat(text):
            if self.mw.ser_ceil_m_comb.currentText() == "m":
                self.req1.service_ceil = float(text)
            else:
                self.req1.service_ceil = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.serv_ceil_lab.text())
            self.mw.serv_ceil_inp.setText("0")
            self.req1.service_ceil = 0
            input_warn.exec_()

    @pyqtSlot()
    def roc_inp(self, text):
        if self.isfloat(text):
            if self.mw.roc_mpers_comb.currentText() == "m/s":
                self.req1.roc = float(text)
            else:
                self.req1.roc = float(text)/data.Conversion.MPERS_2_FTPERMIN
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.roc_lab.text())
            self.mw.roc_inp.setText("0")
            self.req1.roc = 0
            input_warn.exec_()

    @pyqtSlot()
    def cruise_m_inp(self, text):
        if self.isfloat(text):
            self.req1.cruise_mach = float(text)
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.cruise_m_lab.text())
            self.mw.cruise_m_inp.setText("0")
            self.req1.cruise_mach = 0
            input_warn.exec_()

    @pyqtSlot()
    def roc_isa_t_sb(self, temp):
        self.req1.roc_isa_t = temp

    @pyqtSlot()
    def tod_land_inp(self, text):
        if self.isfloat(text):
            if self.mw.tod_lan_m_comb.currentText() == "m":
                self.req1.to_distance_land = float(text)
            else:
                self.req1.to_distance_land = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.tod_land_lab.text())
            self.mw.tod_land_inp.setText("0")
            self.req1.to_distance_land = 0
            input_warn.exec_()

    @pyqtSlot()
    def tod_water_inp(self, text):
        if self.isfloat(text):
            if self.mw.tod_water_m_comb.currentText() == "m":
                self.req1.to_distance_water = float(text)
            else:
                self.req1.to_distance_water = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.tod_water_lab.text())
            self.mw.tod_water_inp.setText("0")
            self.req1.to_distance_water = 0
            input_warn.exec_()

    @pyqtSlot()
    def lan_land_inp(self, text):
        if self.isfloat(text):
            if self.mw.lan_land_m_comb.currentText() == "m":
                self.req1.la_distance_land = float(text)
            else:
                self.req1.la_distance_land = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.lan_land_lab.text())
            self.mw.lan_land_inp.setText("0")
            self.req1.la_distance_land = 0
            input_warn.exec_()

    @pyqtSlot()
    def lan_water_inp(self, text):
        if self.isfloat(text):
            if self.mw.lan_water_m_comb.currentText() == "m":
                self.req1.la_distance_water = float(text)
            else:
                self.req1.la_distance_water = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.lan_water_lab.text())
            self.mw.lan_water_inp.setText("0")
            self.req1.la_distance_water = 0
            input_warn.exec_()

    @pyqtSlot()
    def max_run_alt_inp(self, text):
        if self.isfloat(text):
            if self.mw.max_run_alt_m_comb.currentText() == "m":
                self.req1.max_run_alt = float(text)
                self.mw.atm_alt_lab.setText("Atmospheric compliance at "+text+" m")
            else:
                f = float(text)/data.Conversion.M_2_FT
                self.req1.max_run_alt = f
                self.mw.atm_alt_lab.setText("Atmospheric compliance at "+QString.number(f)+" m")
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.max_run_alt_lab.text())
            self.mw.max_run_alt_inp.setText("0")
            self.req1.max_run_alt = 0
            input_warn.exec_()

    @pyqtSlot()
    def run_msl_isa_t_sb(self, temp):
        self.req1.run_msl_isa_t = temp

    @pyqtSlot()
    def run_alt_isa_t_sb(self, temp):
        self.req1.run_alt_isa_t = temp

    @pyqtSlot()
    def inst_inp(self, text):
        if self.isfloat(text):
            if self.mw.inst_degpers_comb.currentText() == "deg/s":
                self.req1.inst_turn = float(text)
            else:
                self.req1.inst_turn = float(text)/data.Conversion.DEG_2_RAD
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.inst_lab.text())
            self.mw.inst_inp.setText("0")
            self.req1.inst_turn = 0
            input_warn.exec_()

    @pyqtSlot()
    def sus_inp(self, text):
        if self.isfloat(text):
            if self.mw.sus_degpers_comb.currentText() == "deg/s":
                self.req1.sus_turn = float(text)
            else:
                self.req1.sus_turn = float(text)/data.Conversion.DEG_2_RAD
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.sus_lab.text())
            self.mw.sus_inp.setText("0")
            self.req1.sus_turn = 0
            input_warn.exec_()

    @pyqtSlot()
    def bank_ang_inp(self, text):
        if self.isfloat(text):
            if self.mw.bank_ang_deg_comb.currentText() == "deg":
                self.req1.bank_ang = float(text)
            else:
                self.req1.bank_ang = float(text)/data.Conversion.DEG_2_RAD
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.bank_ang_lab.text())
            self.mw.bank_ang_inp.setText("0")
            self.req1.bank_ang = 0
            input_warn.exec_()

    @pyqtSlot()
    def fuel_res_inp(self, text):
        if self.isfloat(text):
            if self.mw.fuel_res_km_comb.currentText() == "km":
                self.req1.fuel_res_rang = float(text)
            elif self.mw.fuel_res_km_comb.currentText() == "mi":
                self.req1.fuel_res_rang = float(text)/data.Conversion.KM_2_MI
            else:
                self.req1.fuel_res_rang = float(text)/data.Conversion.KM_2_NM
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.fuel_res_lab.text())
            self.mw.fuel_res_inp.setText("0")
            self.req1.fuel_res_rang = 0
            input_warn.exec_()

    @pyqtSlot()
    def pass_inp(self, num):
        print num
        if self.isdigit(num):
            print "isdigit"
            self.req1.pass_num = int(num)
            se = analysis.calc_payload(self.req1)
            self.mw.pay_wt_inplab.setText(QString.number(se))
        elif num == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.pass_lab.text())
            self.mw.pass_inp.setText("0")
            self.req1.pass_num = 0
            input_warn.exec_()

    @pyqtSlot()
    def cargo_inp(self, wt):
         if self.isfloat(wt):
            if self.mw.cargo_kg_comb.currentText() == "kg":
                self.req1.cargo_wt = float(wt)
            else:
                self.req1.cargo_wt = data.Conversion.LB_2_KG*float(wt)
            se = analysis.calc_payload(self.req1)
            self.mw.pay_wt_inplab.setText(QString.number(se))
         elif wt == "":
            pass
         else:
             input_warn = QtGui.QMessageBox()
             input_warn.setText("Please enter a number"+" in "+self.mw.cargo_lab.text())
             self.mw.cargo_inp.setText("0")
             self.req1.cargo_wt = 0
             input_warn.exec_()

    # Mission Tab
    @pyqtSlot()
    def miss_nam_inp(self, text):
        self.mission1.name = text

    @pyqtSlot()
    def alt_beg_inp(self, alt):
        if self.isfloat(alt):
            if self.mw.alt_beg_seg_m_comb.currentText() == "m":
                self.mission1.segments[self.counter].y_pos_start = float(alt)
            else:
                self.mission1.segments[self.counter].y_pos_start = float(alt)/data.Conversion.M_2_FT
        elif alt == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.alt_beg_lab.text())
            self.mw.alt_beg_inp.setText("0")
            self.mission1.segments[self.counter].y_pos_start = 0
            input_warn.exec_()

    @pyqtSlot()
    def rang_seg_inp(self, dist):
        if self.isfloat(dist):
            if self.mw.rang_seg_m_comb.currentText() == "m":
                self.mission1.segments[self.counter].range = float(dist)
            else:
                self.mission1.segments[self.counter].range = float(dist)/data.Conversion.M_2_FT
        elif dist == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.rang_seg_lab.text())
            self.mw.rang_seg_inp.setText("0")
            self.mission1.segments[self.counter].range = 0
            input_warn.exec_()

    @pyqtSlot()
    def ht_seg_inp(self, ht):
        if self.isfloat(ht):
            if self.mw.ht_seg_m_comb.currentText() == "m":
                self.mission1.segments[self.counter].height = float(ht)
            else:
                self.mission1.segments[self.counter].height = float(ht)/data.Conversion.M_2_FT
        elif ht == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.ht_seg_lab.text())
            self.mw.ht_seg_inp.setText("0")
            self.mission1.segments[self.counter].height = 0
            input_warn.exec_()

    @pyqtSlot()
    def time_seg_inp(self, t):
        if self.isfloat(t):
            if self.mw.time_seg_hr_comb.currentText() == "hr":
                self.mission1.segments[self.counter].time = float(t)
            else:
                self.mission1.segments[self.counter].time = float(t)/data.Conversion.HR_2_MIN
        elif t == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.time_seg_lab.text())
            self.mw.time_seg_inp.setText("0")
            self.mission1.segments[self.counter].time = 0
            input_warn.exec_()

    @pyqtSlot()
    def typ_seg_comb(self, segment):
        if segment == "Takeoff":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
        elif segment == "Climb":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
        elif segment == "Cruise":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
        elif segment == "Loiter":
            self.mw.rang_seg_inp.setDisabled(True)
            self.mw.ht_seg_inp.setDisabled(True)
            self.mw.time_seg_inp.setDisabled(False)
        elif segment == "Descent":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
        elif segment == "Landing":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
    # Unit conversion Slots
    # ========****=========

    # Requirements Tab
    @pyqtSlot()
    def set_req_push(self):
        self.req1.regulation = self.mw.reg_comb.currentText()

    @pyqtSlot()
    def des_rang_km_comb(self, dist):
        if dist == "mi":
            g = data.Conversion.KM_2_MI*self.req1.design_range
            self.mw.des_rang_inp.setText(QString.number(g))
        elif dist == "nm":
            g = data.Conversion.KM_2_NM*self.req1.design_range
            self.mw.des_rang_inp.setText(QString.number(g))
        else:
            self.mw.des_rang_inp.setText(QString.number(self.req1.design_range))

    @pyqtSlot()
    def des_rang_payload_kg_comb(self, wt):
        if wt == "lb":
            g = self.req1.des_rang_payload/data.Conversion.LB_2_KG
            self.mw.des_rang_payload_inp.setText(QString.number(g))
        else:
            self.mw.des_rang_payload_inp.setText(QString.number(self.req1.payload_wt))

    @pyqtSlot()
    def ser_ceil_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.service_ceil*data.Conversion.M_2_FT
            self.mw.serv_ceil_inp.setText(QString.number(g))
        else:
            self.mw.serv_ceil_inp.setText(QString.number(self.req1.service_ceil))

    @pyqtSlot()
    def roc_mpers_comb(self, speed):
        if speed == "ft/min":
            g = self.req1.roc*data.Conversion.MPERS_2_FTPERMIN
            self.mw.roc_inp.setText(QString.number(g))
        else:
            self.mw.roc_inp.setText(QString.number(self.req1.roc))

    @pyqtSlot()
    def tod_lan_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.to_distance_land*data.Conversion.M_2_FT
            self.mw.tod_land_inp.setText(QString.number(g))
        else:
            self.mw.tod_land_inp.setText(QString.number(self.req1.to_distance_land))

    @pyqtSlot()
    def tod_water_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.to_distance_water*data.Conversion.M_2_FT
            self.mw.tod_water_inp.setText(QString.number(g))
        else:
            self.mw.tod_water_inp.setText(QString.number(self.req1.to_distance_water))

    @pyqtSlot()
    def lan_land_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.la_distance_land*data.Conversion.M_2_FT
            self.mw.lan_land_inp.setText(QString.number(g))
        else:
            self.mw.lan_land_inp.setText(QString.number(self.req1.la_distance_land))

    @pyqtSlot()
    def lan_water_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.la_distance_water*data.Conversion.M_2_FT
            self.mw.lan_water_inp.setText(QString.number(g))
        else:
            self.mw.lan_water_inp.setText(QString.number(self.req1.la_distance_water))

    @pyqtSlot()
    def max_run_alt_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.max_run_alt*data.Conversion.M_2_FT
            self.mw.max_run_alt_inp.setText(QString.number(g))
        else:
            self.mw.max_run_alt_inp.setText(QString.number(self.req1.max_run_alt))

    @pyqtSlot()
    def inst_degpers_comb(self, rate):
        if rate == "rad/s":
            g = self.req1.inst_turn*data.Conversion.DEG_2_RAD
            self.mw.inst_inp.setText(QString.number(g))
        else:
            self.mw.inst_inp.setText(QString.number(self.req1.inst_turn))

    @pyqtSlot()
    def sus_degpers_comb(self, rate):
        if rate == "rad/s":
            g = self.req1.sus_turn*data.Conversion.DEG_2_RAD
            self.mw.sus_inp.setText(QString.number(g))
        else:
            self.mw.sus_inp.setText(QString.number(self.req1.sus_turn))

    @pyqtSlot()
    def bank_ang_comb(self, ang):
        if ang == "rad":
            g = self.req1.bank_ang*data.Conversion.DEG_2_RAD
            self.mw.bank_ang_inp.setText(QString.number(g))
        else:
            self.mw.bank_ang_inp.setText(QString.number(self.req1.bank_ang))

    @pyqtSlot()
    def fuel_res_km_comb(self, dist):
        if dist == "mi":
            g = self.req1.fuel_res_rang*data.Conversion.KM_2_MI
            self.mw.fuel_res_inp.setText(QString.number(g))
        elif dist == "km":
            self.mw.fuel_res_inp.setText(QString.number(self.req1.fuel_res_rang))
        else:
            g = self.req1.fuel_res_rang*data.Conversion.KM_2_NM
            self.mw.fuel_res_inp.setText(QString.number(g))

    @pyqtSlot()
    def cargo_kg_comb(self, wt):
         if wt == "lb":
            g = self.req1.cargo_wt/data.Conversion.LB_2_KG
            self.mw.cargo_inp.setText(QString.number(g))
         else:
            self.mw.cargo_inp.setText(QString.number(self.req1.cargo_wt))
    # Mission Tab

    @pyqtSlot()
    def alt_beg_seg_m_comb(self, dist):
        if dist == "ft":
            g = self.mission1.segments[self.counter].y_pos_start*data.Conversion.M_2_FT
            self.mw.alt_beg_inp.setText(QString.number(g))
        else:
            self.mw.alt_beg_inp.setText(QString.number(self.mission1.segments[self.counter].y_pos_start))

    @pyqtSlot()
    def rang_seg_m_comb(self, dist):
        if dist == "ft":
            g = self.mission1.segments[self.counter].range*data.Conversion.M_2_FT
            self.mw.rang_seg_inp.setText(QString.number(g))
        else:
            self.mw.rang_seg_inp.setText(QString.number(self.mission1.segments[self.counter].range))

    @pyqtSlot()
    def ht_seg_m_comb(self, ht):
        if ht == "ft":
            g = self.mission1.segments[self.counter].height*data.Conversion.M_2_FT
            self.mw.ht_seg_inp.setText(QString.number(g))
        else:
            self.mw.ht_seg_inp.setText(QString.number(self.mission1.segments[self.counter].height))

    @pyqtSlot()
    def time_seg_hr_comb(self, t):
        if t == "hr":
            self.mw.time_seg_inp.setText(QString.number(self.mission1.segments[self.counter].time))
        else:
            g = self.mission1.segments[self.counter].time*data.Conversion.HR_2_MIN
            self.mw.time_seg_inp.setText(QString.number(g))

    # Assisting Functions

    def isfloat(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def isdigit(self,value):
        try:
            int(value)
            return True
        except ValueError:
            return False


