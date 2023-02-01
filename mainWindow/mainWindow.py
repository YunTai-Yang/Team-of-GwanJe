from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect ,QPushButton,QLineEdit, QLabel, QMessageBox, QInputDialog, QCheckBox, QMdiSubWindow
from PyQt5.QtCore import QThread, QUrl, QTimer, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont

import sys, os
from pyqtgraph import PlotWidget, GridItem
from numpy import empty, zeros
from .import widgetSize as ws

class GraphViewer_Thread(QThread):
    def __init__(self, mainwindow,datahub):
        super().__init__()
        self.mainwindow = mainwindow
        self.datahub = datahub

        self.view = QWebEngineView(self.mainwindow)
        self.view.load(QUrl())
        self.view.setGeometry(*ws.webEngine_geometry)
        
        self.pw_angle = PlotWidget(self.mainwindow)
        self.angle_title = QLabel(self.mainwindow)
        self.angle_title.setText("<b>&#8226; Angle</b>")

        self.pw_angleSpeed = PlotWidget(self.mainwindow)
        self.angleSpeed_title = QLabel(self.mainwindow)
        self.angleSpeed_title.setText("<b>&#8226; Angle Speed</b>")

        self.pw_accel = PlotWidget(self.mainwindow)
        self.accel_title = QLabel(self.mainwindow)
        self.accel_title.setText("<b>&#8226; Angle Speed</b>")

        self.pw_angle.setGeometry(*ws.pw_angle_geometry)

        self.pw_angleSpeed.setGeometry(*ws.pw_angleSpeed_geometry)
        self.pw_accel.setGeometry(*ws.pw_accel_geometry)

        self.angle_title.setGeometry(*ws.angle_title_geometry)
        self.angleSpeed_title.setGeometry(*ws.angleSpeed_title_geometry)
        self.accel_title.setGeometry(*ws.accel_title_geometry)

        self.angle_title.setFont(ws.font_angle_title)
        self.angleSpeed_title.setFont(ws.font_angleSpeed_title)
        self.accel_title.setFont(ws.font_accel_title)

        self.pw_angle.addItem(GridItem())
        self.pw_angleSpeed.addItem(GridItem())
        self.pw_accel.addItem(GridItem())

        #set label in each axis
        self.pw_angle.getPlotItem().getAxis('bottom').setLabel('Time(second)')
        self.pw_angle.getPlotItem().getAxis('left').setLabel('Degree')
        self.pw_angleSpeed.getPlotItem().getAxis('bottom').setLabel('Time(second)')
        self.pw_angleSpeed.getPlotItem().getAxis('left').setLabel('Degree/second')
        self.pw_accel.getPlotItem().getAxis('bottom').setLabel('Time(second)')
        self.pw_accel.getPlotItem().getAxis('left').setLabel('g(gravity accel)')

        #set range in each axis
        self.pw_angle.setYRange(-180,180)
        self.pw_angleSpeed.setYRange(-1000,1000)
        self.pw_accel.setYRange(-6,6)

        #legend
        self.pw_angle.getPlotItem().addLegend()
        self.pw_angleSpeed.getPlotItem().addLegend()
        self.pw_accel.getPlotItem().addLegend()
        

        self.curve_roll = self.pw_angle.plot(pen='r', name = "roll")
        self.curve_pitch = self.pw_angle.plot(pen='g',name = "pitch")
        self.curve_yaw = self.pw_angle.plot(pen='b', name = "yaw")

        self.curve_rollSpeed = self.pw_angleSpeed.plot(pen='r', name = "roll speed")
        self.curve_pitchSpeed = self.pw_angleSpeed.plot(pen='g', name = "pitch speed")
        self.curve_yawSpeed = self.pw_angleSpeed.plot(pen='b', name = "yaw speed")

        self.curve_xaccel = self.pw_accel.plot(pen='r', name = "x acc")
        self.curve_yaccel = self.pw_accel.plot(pen='g',name = "y acc")
        self.curve_zaccel = self.pw_accel.plot(pen='b',name ="z acc")

        self.loadnum = 0

        self.starttime = 0.0
        self.starttime_count = 0
        self.init_sec = 0
        self.time = zeros(150)
        self.roll = zeros(150)
        self.pitch = zeros(150)
        self.yaw = zeros(150)
        self.rollSpeed = zeros(150)
        self.pitchSpeed = zeros(150)
        self.yawSpeed = zeros(150)
        self.xaccel = zeros(150)
        self.yaccel = zeros(150)
        self.zaccel = zeros(150)

    def update_data(self):
        if len(self.datahub.altitude) == 0:
            pass

        else:
            if len(self.datahub.altitude) <= 150 :
                n = len(self.datahub.altitude) 
                self.roll[-n:] = self.datahub.rolls
                self.pitch[-n:] = self.datahub.pitchs
                self.yaw[-n:] = self.datahub.yaws
                self.rollSpeed[-n:] = self.datahub.rollSpeeds
                self.pitchSpeed[-n:] = self.datahub.pitchSpeeds
                self.yawSpeed[-n:] = self.datahub.yawSpeeds
                self.xaccel[-n:] = self.datahub.Xaccels
                self.yaccel[-n:] = self.datahub.Yaccels
                self.zaccel[-n:] = self.datahub.Zaccels
                hours = self.datahub.hours * 3600
                minutes = self.datahub.mins * 60
                miliseconds = self.datahub.tenmilis * 0.01
                seconds = self.datahub.secs
                totaltime = hours + minutes + miliseconds + seconds
                self.starttime = self.datahub.hours[0]*3600 + self.datahub.mins[0]*60 + self.datahub.tenmilis[0]*0.01+ self.datahub.secs[0]
                self.time[-n:] = totaltime - self.starttime
            
            else : 
                self.roll[:] = self.datahub.rolls[-150:]
                self.pitch[:] = self.datahub.pitchs[-150:]
                self.yaw[:] = self.datahub.yaws[-150:]
                self.rollSpeed[:] = self.datahub.rollSpeeds[-150:]
                self.pitchSpeed[:] = self.datahub.pitchSpeeds[-150:]
                self.yawSpeed[:] = self.datahub.yawSpeeds[-150:]
                self.xaccel[:] = self.datahub.Xaccels[-150:]
                self.yaccel[:] = self.datahub.Yaccels[-150:]
                self.zaccel[:] = self.datahub.Zaccels[-150:]
                hours = self.datahub.hours[-150:] * 3600
                minutes = self.datahub.mins[-150:] * 60
                miliseconds = self.datahub.tenmilis[-150:] * 0.01
                seconds = self.datahub.secs[-150:]
                totaltime = hours + minutes + miliseconds + seconds
                self.time[:] = totaltime - self.starttime

            self.curve_roll.setData(x=self.time, y=self.roll)
            self.curve_pitch.setData(x=self.time, y=self.pitch)
            self.curve_yaw.setData(x=self.time, y=self.yaw)

            self.curve_rollSpeed.setData(x=self.time, y=self.rollSpeed)
            self.curve_pitchSpeed.setData(x=self.time, y=self.pitchSpeed)
            self.curve_yawSpeed.setData(x=self.time, y=self.yawSpeed)

            self.curve_xaccel.setData(x=self.time, y=self.xaccel)
            self.curve_yaccel.setData(x=self.time, y=self.yaccel)
            self.curve_zaccel.setData(x=self.time, y=self.zaccel)

    def on_load_finished(self):
        # to move the timer to the same thread as the QObject
        self.mytimer = QTimer(self)
        self.mytimer.timeout.connect(self.update_data)
        self.mytimer.start(100)

    def run(self):
        self.view.loadFinished.connect(self.on_load_finished)


class MapViewer_Thread(QThread):
    def __init__(self, mainwindow,datahub):
        super().__init__()
        self.mainwindow = mainwindow
        self.datahub= datahub
        # self.setWindowTitle("Real-time Dynamic Map")

        # Create the QWebEngineView widget
        self.view = QWebEngineView(self.mainwindow)
        self.view.setGeometry(*ws.map_geometry)
        
        # Load the HTML file that contains the leaflet map
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        file_path = os.path.join(dir_path, 'map.html')
        self.view.load(QUrl.fromLocalFile(file_path))
        self.view.show()


    def on_load_finished(self):
        # Get the QWebEnginePage object
    
        page = self.view.page()
        # Inject a JavaScript function to update the marker's location
        self.script = f"""
        var lat = 36.666;
        var lng = 126.666;
        var map = L.map("map").setView([lat,lng], 15);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
            maxZoom: 18,
        }}).addTo(map);
        var marker = L.marker([lat,lng]).addTo(map);
        /*
        trigger is a variable which update a map view according to their location
        */
        var trigger_javascript = 0;
        function updateMarker(latnew, lngnew, trigger_python) {{
           
            marker.setLatLng([latnew, lngnew]);
        
            if(trigger_python >= 1 && trigger_javascript == 0) {{
            map.setView([latnew,lngnew], 15);
            trigger_javascript = 1;
            }}
        }}
        """
        #{print(self.datahub.latitudes)}
        page.runJavaScript(self.script)
        # Create a QTimer to call the updateMarker function every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_marker)
        self.timer.start(1000)

    def update_marker(self):
        #wait for receiving datas.....
        if len(self.datahub.latitudes) == 0:
            pass
        # Call the JavaScript function to update the marker's location
        else: 
            self.view.page().runJavaScript(f"updateMarker({self.datahub.latitudes[-1]},{self.datahub.longitudes[-1]},{len(self.datahub.latitudes)})")

    # Connect the QWebEngineView's loadFinished signal to the on_load_finished slot
    def run(self):
        self.view.loadFinished.connect(self.on_load_finished)


class MainWindow(QMainWindow):
    def __init__(self, datahub):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.datahub = datahub
        self.resize(*ws.full_size)
        self.setStyleSheet("QMainWindow { background-color: rgb(250, 250, 250);}")
        
        """Set Buttons"""
        self.start_button = QPushButton("Press Start",self)
        self.stop_button = QPushButton("Stop",self)
        self.rf_port_edit = QLineEdit("COM8",self)
        self.port_text = QLabel("Port",self)
        self.baudrate_edit = QLineEdit("115200",self)
        self.baudrate_text = QLabel("Baudrate",self)
        self.guide_text = QLabel(ws.guide,self)

        self.start_button.setFont(ws.font_start_text)
        self.stop_button.setFont(ws.font_stop_text)
        self.start_button.setStyleSheet("background-color: rgb(30,30,100); color: rgb(250, 250, 250);font-weight: bold;")
        self.stop_button.setStyleSheet("background-color: rgb(150,30,30); color: rgb(250, 250, 250);font-weight: bold;")

        shadow_start_button = QGraphicsDropShadowEffect()
        shadow_stop_button = QGraphicsDropShadowEffect()
        shadow_start_button.setOffset(8)
        shadow_stop_button.setOffset(8)
        self.start_button.setGraphicsEffect(shadow_start_button)
        self.stop_button.setGraphicsEffect(shadow_stop_button)

        self.baudrate_text.setFont(ws.font_baudrate)
        self.port_text.setFont(ws.font_portText)
        self.guide_text.setFont(ws.font_guideText)

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.rf_port_edit.setEnabled(True)
        self.baudrate_edit.setEnabled(True)
        
        """Set Buttons Connection"""
        self.start_button.clicked.connect(self.start_button_clicked)
        self.stop_button.clicked.connect(self.stop_button_clicked)
        
        self.roll_hide_checkbox = QCheckBox("roll",self)
        self.pitch_hide_checkbox = QCheckBox("pitch",self)
        self.yaw_hide_checkbox = QCheckBox("yaw",self)

        self.rollspeed_hide_checkbox = QCheckBox("w_x",self)
        self.pitchspeed_hide_checkbox = QCheckBox("w_y",self)
        self.yawspeed_hide_checkbox = QCheckBox("w_z",self)

        self.xacc_hide_checkbox = QCheckBox("Xaccel",self)
        self.yacc_hide_checkbox = QCheckBox("Yaccel",self)
        self.zacc_hide_checkbox = QCheckBox("Zaccel",self)

        self.roll_hide_checkbox.setGeometry(*ws.roll_checker_geomoetry)
        self.pitch_hide_checkbox.setGeometry(*ws.pitch_checker_geomoetry)
        self.yaw_hide_checkbox.setGeometry(*ws.yaw_checker_geomoetry)

        self.rollspeed_hide_checkbox.setGeometry(*ws.rollS_checker_geomoetry)
        self.pitchspeed_hide_checkbox.setGeometry(*ws.pitchS_checker_geomoetry)
        self.yawspeed_hide_checkbox.setGeometry(*ws.yawS_checker_geomoetry)

        self.xacc_hide_checkbox.setGeometry(*ws.ax_checker_geomoetry)
        self.yacc_hide_checkbox.setGeometry(*ws.ay_checker_geomoetry)
        self.zacc_hide_checkbox.setGeometry(*ws.az_checker_geomoetry)

        self.roll_hide_checkbox.setFont(ws.checker_font)
        self.pitch_hide_checkbox.setFont(ws.checker_font)
        self.yaw_hide_checkbox.setFont(ws.checker_font)

        self.xacc_hide_checkbox.setFont(ws.checker_font)
        self.yacc_hide_checkbox.setFont(ws.checker_font)
        self.zacc_hide_checkbox.setFont(ws.checker_font)

        self.roll_hide_checkbox.stateChanged.connect(self.roll_hide_checkbox_state)
        self.pitch_hide_checkbox.stateChanged.connect(self.pitch_hide_checkbox_state)
        self.yaw_hide_checkbox.stateChanged.connect(self.yaw_hide_checkbox_state)
        self.rollspeed_hide_checkbox.stateChanged.connect(self.rollspeed_hide_checkbox_state)
        self.pitchspeed_hide_checkbox.stateChanged.connect(self.pitchspeed_hide_checkbox_state)
        self.yawspeed_hide_checkbox.stateChanged.connect(self.yawspeed_hide_checkbox_state)
        self.xacc_hide_checkbox.stateChanged.connect(self.xacc_hide_checkbox_state)
        self.yacc_hide_checkbox.stateChanged.connect(self.yacc_hide_checkbox_state)
        self.zacc_hide_checkbox.stateChanged.connect(self.zacc_hide_checkbox_state)

        self.rollspeed_hide_checkbox.setFont(ws.checker_font)
        self.pitchspeed_hide_checkbox.setFont(ws.checker_font)
        self.yawspeed_hide_checkbox.setFont(ws.checker_font)

        """Set Geometry"""
        self.start_button.setGeometry(*ws.start_geometry)
        self.stop_button.setGeometry(*ws.stop_geometry)
        self.port_text.setGeometry(*ws.port_text_geometry)
        self.rf_port_edit.setGeometry(*ws.port_edit_geometry)
        self.baudrate_text.setGeometry(*ws.baudrate_text_geometry)
        self.baudrate_edit.setGeometry(*ws.baudrate_edit_geometry)
        self.guide_text.setGeometry(*ws.cmd_geometry)
        
        """Set Viewer Thread"""
        self.mapviewer = MapViewer_Thread(self,datahub)
        self.graphviewer = GraphViewer_Thread(self,datahub)
        self.mapviewer.start()
        self.graphviewer.start()

    # Run when start button is clicked
    def start_button_clicked(self):
        QMessageBox.information(self,"information","Program Start")
        FileName,ok = QInputDialog.getText(self,'Input Dialog', 'Enter your File Name',QLineEdit.Normal,"Your File Name")
        if ok:
            self.datahub.mySerialPort = self.rf_port_edit.text()
            self.datahub.myBaudrate = self.baudrate_edit.text()
            self.datahub.file_Name = FileName+'.csv'
            self.datahub.communication_start()
            
            self.datahub.serial_port_error=-1
            if self.datahub.check_communication_error():
                QMessageBox.warning(self,"warning","SSUJJUN")
                self.datahub.communication_stop()

            else:
                self.datahub.datasaver_start()
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                self.rf_port_edit.setEnabled(False)
                self.baudrate_edit.setEnabled(False)
        self.datahub.serial_port_error=-1
    # Run when stop button is clicked
    def stop_button_clicked(self):
        QMessageBox.information(self,"information","Program Stop")
        self.datahub.communication_stop()
        self.datahub.datasaver_stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.rf_port_edit.setEnabled(False)
        self.baudrate_edit.setEnabled(False)
        self.result_window()

    #curve hide check box is clicked
    def roll_hide_checkbox_state(self,state):
        self.graphviewer.curve_roll.setVisible(state != Qt.Checked)
    def pitch_hide_checkbox_state(self,state):
        self.graphviewer.curve_pitch.setVisible(state != Qt.Checked)
    def yaw_hide_checkbox_state(self,state):
        self.graphviewer.curve_yaw.setVisible(state != Qt.Checked)
    def rollspeed_hide_checkbox_state(self,state):
        self.graphviewer.curve_rollSpeed.setVisible(state != Qt.Checked)
    def pitchspeed_hide_checkbox_state(self,state):
        self.graphviewer.curve_pitchSpeed.setVisible(state != Qt.Checked)
    def yawspeed_hide_checkbox_state(self,state):
        self.graphviewer.curve_yawSpeed.setVisible(state != Qt.Checked)
    def xacc_hide_checkbox_state(self,state):
        self.graphviewer.curve_xaccel.setVisible(state != Qt.Checked)
    def yacc_hide_checkbox_state(self,state):
        self.graphviewer.curve_yaccel.setVisible(state != Qt.Checked)
    def zacc_hide_checkbox_state(self,state):
        self.graphviewer.curve_zaccel.setVisible(state != Qt.Checked)

    def result_window(self):
        self.resultwindow = QMainWindow()
        self.resultwindow.resize(440,440)
        self.pw_altitude = PlotWidget(self.resultwindow)
        self.pw_altitude_timeline = self.datahub.hours * 3600 + self.datahub.mins * 60 + self.datahub.secs + self.datahub.tenmilis*0.01 
        self.pw_altitude_timeline -= self.pw_altitude_timeline[0]
        self.pw_altitude.plot(self.pw_altitude_timeline,self.datahub.altitude ,pen = "r", name = "Altitude")
        self.pw_altitude.setGeometry(20,20,400,400)
        self.resultwindow.show()



    # Main Window start method
    def start(self):
        self.show()
        
    def setEventLoop(self):
        sys.exit(self.app.exec_())
        
    # Run when mainwindow is closed
    def closeEvent(self, event):
        self.stop_button_clicked()
        event.accept()