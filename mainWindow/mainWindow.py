from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect , QPushButton,QLineEdit, QLabel, QMessageBox, QInputDialog, QCheckBox, QStackedWidget, QAction
from PyQt5.QtCore import QThread, QUrl, QTimer, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QPixmap
from pyqtgraph import PlotWidget, GridItem, AxisItem

from numpy import zeros, array, cross, reshape, sin, cos, deg2rad
from numpy.random import rand
from numpy.linalg import norm

from matplotlib.pyplot import figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from datetime import timedelta
from os.path import abspath, dirname, join, exists
from sys import exit, argv

from pandas import read_csv

from . import widgetStyle as ws

class PageWindow(QMainWindow):
    gotoSignal = pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


class GraphViewer_Thread(QThread):
    def __init__(self, mainwindow,datahub):
        super().__init__()
        self.mainwindow = mainwindow
        self.datahub = datahub

        self.view = QWebEngineView(self.mainwindow)
        self.view.load(QUrl())
        self.view.setGeometry(*ws.webEngine_geometry)
        
        self.angle_title = QLabel(self.mainwindow)
        self.angle_title.setText("<b>&#8226; Angle</b>")
        self.pw_angle = PlotWidget(self.mainwindow)
        
        self.angleSpeed_title = QLabel(self.mainwindow)
        self.angleSpeed_title.setText("<b>&#8226; Angle Speed</b>")
        self.pw_angleSpeed = PlotWidget(self.mainwindow)
        
        self.accel_title = QLabel(self.mainwindow)
        self.accel_title.setText("<b>&#8226; Acceleration</b>")
        self.pw_accel = PlotWidget(self.mainwindow)
        
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

        self.x_ran = 500
        self.time = zeros(self.x_ran)
        self.roll = zeros(self.x_ran)
        self.pitch = zeros(self.x_ran)
        self.yaw = zeros(self.x_ran)
        self.rollSpeed = zeros(self.x_ran)
        self.pitchSpeed = zeros(self.x_ran)
        self.yawSpeed = zeros(self.x_ran)
        self.xaccel = zeros(self.x_ran)
        self.yaccel = zeros(self.x_ran)
        self.zaccel = zeros(self.x_ran)

        self.starttime = 0.0

    def update_data(self):
        if len(self.datahub.speed) == 0:
            pass

        else:
            if len(self.datahub.speed) <= self.x_ran :
                n = len(self.datahub.speed) 
                self.roll[-n:] = self.datahub.rolls[-n:]
                self.pitch[-n:] = self.datahub.pitchs[-n:]
                self.yaw[-n:] = self.datahub.yaws[-n:]
                self.rollSpeed[-n:] = self.datahub.rollSpeeds[-n:]
                self.pitchSpeed[-n:] = self.datahub.pitchSpeeds[-n:]
                self.yawSpeed[-n:] = self.datahub.yawSpeeds[-n:]
                self.xaccel[-n:] = self.datahub.Xaccels[-n:]
                self.yaccel[-n:] = self.datahub.Yaccels[-n:]
                self.zaccel[-n:] = self.datahub.Zaccels[-n:]
                hours = self.datahub.hours[-n:] * 3600
                minutes = self.datahub.mins[-n:] * 60
                miliseconds = self.datahub.tenmilis[-n:] * 0.01
                seconds = self.datahub.secs[-n:]
                totaltime = hours + minutes + miliseconds + seconds
                self.starttime = self.datahub.hours[0]*3600 + self.datahub.mins[0]*60 + self.datahub.tenmilis[0]*0.01+ self.datahub.secs[0]
                self.time[-n:] = totaltime - self.starttime
            
            else : 
                self.roll[:] = self.datahub.rolls[-self.x_ran:]
                self.pitch[:] = self.datahub.pitchs[-self.x_ran:]
                self.yaw[:] = self.datahub.yaws[-self.x_ran:]
                self.rollSpeed[:] = self.datahub.rollSpeeds[-self.x_ran:]
                self.pitchSpeed[:] = self.datahub.pitchSpeeds[-self.x_ran:]
                self.yawSpeed[:] = self.datahub.yawSpeeds[-self.x_ran:]
                self.xaccel[:] = self.datahub.Xaccels[-self.x_ran:]
                self.yaccel[:] = self.datahub.Yaccels[-self.x_ran:]
                self.zaccel[:] = self.datahub.Zaccels[-self.x_ran:]
                hours = self.datahub.hours[-self.x_ran:] * 3600
                minutes = self.datahub.mins[-self.x_ran:] * 60
                miliseconds = self.datahub.tenmilis[-self.x_ran:] * 0.01
                seconds = self.datahub.secs[-self.x_ran:]
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

    def graph_clear(self):

        self.time = zeros(self.x_ran)
        self.roll = zeros(self.x_ran)
        self.pitch = zeros(self.x_ran)
        self.yaw = zeros(self.x_ran)
        self.rollSpeed = zeros(self.x_ran)
        self.pitchSpeed = zeros(self.x_ran)
        self.yawSpeed = zeros(self.x_ran)
        self.xaccel = zeros(self.x_ran)
        self.yaccel = zeros(self.x_ran)
        self.zaccel = zeros(self.x_ran)

        self.curve_roll.clear()
        self.curve_pitch.clear()
        self.curve_yaw.clear()

        self.curve_rollSpeed.clear()
        self.curve_pitchSpeed.clear()
        self.curve_yawSpeed.clear()

        self.curve_xaccel.clear()
        self.curve_yaccel.clear()
        self.curve_zaccel.clear()


    def on_load_finished(self):
        # to move the timer to the same thread as the QObject
        self.mytimer = QTimer(self)
        self.mytimer.timeout.connect(self.update_data)
        self.mytimer.start(30)

    def run(self):
        self.view.loadFinished.connect(self.on_load_finished)


class MapViewer_Thread(QThread):
    def __init__(self, mainwindow,datahub):
        super().__init__()
        self.mainwindow = mainwindow
        self.datahub= datahub

        # Create the QWebEngineView widget
        self.view = QWebEngineView(self.mainwindow)
        self.view.setGeometry(*ws.map_geometry)
        
        # Load the HTML file that contains the leaflet map
        path = abspath(__file__)
        dir_path = dirname(path)
        file_path = join(dir_path, 'map.html')
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


class RocketViewer_Thread(QThread):
    def __init__(self,mainwindow, datahub):
        super().__init__()
        self.mainwindow = mainwindow
        self.datahub = datahub
        self.pose = array([1.0, 0.0, 0.0])
        self.radius = 0.1
        self.normal = array([0.0, 0.0, 0.0])
        self.x = rand(1)
        self.y = rand(1)
        self.circle_point = zeros((3,5)) 
        self.view = QWebEngineView(self.mainwindow)
        self.view.load(QUrl())
        self.view.setGeometry(*ws.model_geometry)
        

        self.fig = figure(facecolor='#a0a0a0')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mainwindow)
        self.canvas.setGeometry(*ws.model_geometry)

        self.speed_label = QLabel("Speed : ",self.mainwindow)
        self.speed_label.setGeometry(*ws.speed_label_geometry)
        self.speed_label.setFont(ws.font_speed_text)


        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection = '3d', facecolor='#a0a0a0')
        self.ax.set_xlim([-1,1])
        self.ax.set_ylim([-1,1])
        self.ax.set_zlim([-1,1])
        self.ax.axis('off')
        self.ax.quiver(0, 0, 0, self.pose[0],self.pose[1],self.pose[2],length = 1, lw=2, color='black')

    def on_load_finished(self):
        self.mytimer = QTimer(self)
        self.mytimer.timeout.connect(self.update_pose)
        self.mytimer.start(100)
    
    def quaternion_from_euler(self, x, y, z):
        x = deg2rad(x) / 2
        y = deg2rad(y) / 2
        z = deg2rad(z) / 2

        cx = cos(x)
        cy = cos(y)
        cz = cos(z)

        sx = sin(x)
        sy = sin(y)
        sz = sin(z)

        qw = cx * cy * cz + sx * sy * sz
        qx = sx * cy * cz - cx * sy * sz
        qy = cx * sy * cz + sx * cy * sz
        qz = cx * cy * sz - sx * sy * cz

        return array([qw, qx, qy, qz])

    def quaternion_rotate_vector(self, quat, vec):
        qw, qx, qy, qz = quat
        x, y, z = vec

        ix = qw * x + qy * z - qz * y
        iy = qw * y + qz * x - qx * z
        iz = qw * z + qx * y - qy * x
        iw = -qx * x - qy * y - qz * z

        x = ix * qw + iw * -qx + iy * -qz - iz * -qy
        y = iy * qw + iw * -qy + iz * -qx - ix * -qz
        z = iz * qw + iw * -qz + ix * -qy - iy * -qx

        return array([x, y, z])
    
    def circle_points(self,normal):
        z = (-normal[0]*self.x - normal[1]*self.y)/normal[2]
        self.circle_point[:,0] = normal
        u = array([self.x,self.y,z])/norm([self.x,self.y,z])
        u = reshape(u,3)
        n = normal/norm(normal)
        for i in range(1,5):
            self.circle_point[:,i] = self.radius * cos(deg2rad(90*i))*u + self.radius * sin(deg2rad(90*i))*(cross(u,n))
        return self.circle_point

    def update_pose(self):
        if len(self.datahub.speed) == 0:
            pass
        else:
            self.ax.cla()
            self.ax.set_facecolor('#a0a0a0')
            self.ax.axis('off')
            quat = self.quaternion_from_euler(self.datahub.rolls[-1], self.datahub.pitchs[-1],  self.datahub.yaws[-1])
            result = self.quaternion_rotate_vector(quat, self.pose)
            circle_vectors = self.circle_points(result)
            
            for i in range(5):
                rocket_vectors = circle_vectors[:,i] + result
                self.ax.quiver(circle_vectors[0,i],circle_vectors[1,i],circle_vectors[2,i], rocket_vectors[0], rocket_vectors[1], rocket_vectors[2], lw=0.5, color='black')

            self.ax.set_xlim([-1,1])
            self.ax.set_ylim([-1,1])
            self.ax.set_zlim([-1,1])
            self.ax.set_xlabel("pitch")
            self.ax.set_ylabel("yaw")
            self.ax.set_zlabel("roll")  
            self.speed_label.setText('Speed : {:.2f} m/s'.format(self.datahub.speed[-1]))
            self.canvas.draw()

    def run(self):
        self.view.loadFinished.connect(self.on_load_finished)  

class MainWindow(PageWindow):

    def __init__(self, datahub):
        super().__init__()
        self.datahub = datahub

        self.initUI()
        self.initGraph()

        """Start Thread"""
        self.mapviewer = MapViewer_Thread(self,datahub)
        self.graphviewer = GraphViewer_Thread(self,datahub)
        self.rocketviewer = RocketViewer_Thread(self,datahub)

        self.initMenubar()

        self.mapviewer.start()
        self.graphviewer.start()
        self.rocketviewer.start()

        self.resetcheck = 0
        
    def initUI(self):

        """Set Buttons"""
        self.start_button = QPushButton("Press Start",self)
        self.stop_button = QPushButton("Stop",self)
        self.reset_button = QPushButton("Reset",self)
        self.now_status = QLabel(ws.wait_status,self)
        self.rf_port_edit = QLineEdit("COM8",self)
        self.port_text = QLabel("Port:",self)
        self.baudrate_edit = QLineEdit("115200",self)
        self.baudrate_text = QLabel("Baudrate:",self)
        self.guide_text = QLabel(ws.guide,self)

        self.start_button.setFont(ws.font_start_text)
        self.stop_button.setFont(ws.font_stop_text)
        self.reset_button.setFont(ws.font_reset_text)
        self.rf_port_edit.setStyleSheet("background-color: rgb(250,250,250);")
        self.baudrate_edit.setStyleSheet("background-color: rgb(250,250,250);")
        self.start_button.setStyleSheet("background-color: rgb(30,30,100); color: rgb(250, 250, 250);font-weight: bold;")
        self.stop_button.setStyleSheet("background-color: rgb(150,30,30); color: rgb(250, 250, 250);font-weight: bold;")
        self.reset_button.setStyleSheet("background-color: rgb(150,30,30); color: rgb(250, 250, 250);font-weight: bold;")

        self.shadow_start_button = QGraphicsDropShadowEffect()
        self.shadow_stop_button = QGraphicsDropShadowEffect()
        self.shadow_reset_button = QGraphicsDropShadowEffect()
        self.shadow_start_button.setOffset(6)
        self.shadow_stop_button.setOffset(0)
        self.shadow_reset_button.setOffset(0)
        self.start_button.setGraphicsEffect(self.shadow_start_button)
        self.stop_button.setGraphicsEffect(self.shadow_stop_button)
        self.reset_button.setGraphicsEffect(self.shadow_reset_button)

        self.baudrate_text.setFont(ws.font_baudrate)
        self.port_text.setFont(ws.font_portText)
        self.guide_text.setFont(ws.font_guideText)

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.rf_port_edit.setEnabled(True)
        self.baudrate_edit.setEnabled(True)

        """Set Buttons Connection"""
        self.start_button.clicked.connect(self.start_button_clicked)
        self.stop_button.clicked.connect(self.stop_button_clicked)
        self.reset_button.clicked.connect(self.reset_button_clicked)

        """Set Geometry"""
        self.start_button.setGeometry(*ws.start_geometry)
        self.stop_button.setGeometry(*ws.stop_geometry)
        self.reset_button.setGeometry(*ws.reset_geometry)
        self.port_text.setGeometry(*ws.port_text_geometry)
        self.rf_port_edit.setGeometry(*ws.port_edit_geometry)
        self.baudrate_text.setGeometry(*ws.baudrate_text_geometry)
        self.baudrate_edit.setGeometry(*ws.baudrate_edit_geometry)
        self.guide_text.setGeometry(*ws.cmd_geometry)
        self.now_status.setGeometry(*ws.status_geometry)
        self.now_status.setFont(ws.font_status_text)

        self.path = abspath(__file__)
        self.dir_path = dirname(self.path)
        file_path_logo = join(self.dir_path, 'team_logo.png')

        self.irri_logo = QLabel(self)
        self.irri_logo.setPixmap(QPixmap(file_path_logo).scaled(*ws.irri_logo_geometry[2:4], Qt.KeepAspectRatio))
        self.irri_logo.setGeometry(*ws.irri_logo_geometry)  

    def initMenubar(self):
        self.statusBar()

        change_Action = QAction('Analysis', self)
        change_Action.setShortcut('Ctrl+L')
        change_Action.triggered.connect(self.gosub)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('Menu')
        filemenu.addAction(change_Action)
        self.setStyleSheet("QMenuBar {background-color: rgb(130,130,130);color: rgb(255,255,255);border: 1px solid #000;}")

    def initGraph(self):
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

    def gosub(self):
        self.goto("sub")

    # Run when start button is clicked
    def start_button_clicked(self):
        if self.resetcheck == 0:
            self.datahub.clear()
            QMessageBox.information(self,"information","Program Start")
            FileName,ok = QInputDialog.getText(self,'Input Dialog', 'Enter your File Name',QLineEdit.Normal,"Your File Name")
            file_dir = dirname(self.dir_path)
            file_path = join(file_dir,FileName)+".csv"
            if exists(file_path):
                QMessageBox.information(self,"information","Same file already exist")
            else:
                if ok:
                    self.datahub.mySerialPort=self.rf_port_edit.text()
                    self.datahub.myBaudrate = self.baudrate_edit.text()
                    self.datahub.file_Name = FileName+'.csv'
                    self.datahub.communication_start()
                    
                    self.datahub.serial_port_error=-1
                    if self.datahub.check_communication_error():
                        QMessageBox.warning(self,"warning","Check the Port or Baudrate again.")
                        self.datahub.communication_stop()
                    else:
                        self.datahub.datasaver_start()
                        self.now_status.setText(ws.start_status)
                        self.start_button.setEnabled(False)
                        self.stop_button.setEnabled(True)
                        self.rf_port_edit.setEnabled(False)
                        self.baudrate_edit.setEnabled(False)
                        self.shadow_start_button.setOffset(0)
                        self.shadow_stop_button.setOffset(6)
                        self.shadow_reset_button.setOffset(6)
                self.datahub.serial_port_error=-1
        else:
            self.datahub.communication_start()
            self.datahub.serial_port_error=-1
            self.now_status.setText(ws.start_status)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.rf_port_edit.setEnabled(False)
            self.baudrate_edit.setEnabled(False)
            self.shadow_start_button.setOffset(0)
            self.shadow_stop_button.setOffset(6)
            self.shadow_reset_button.setOffset(6)
            self.resetcheck = 0  

    # Run when stop button is clicked
    def stop_button_clicked(self):
        self.datahub.communication_stop()
        self.now_status.setText(ws.stop_status)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(True)
        self.rf_port_edit.setEnabled(False)
        self.shadow_start_button.setOffset(6)
        self.shadow_stop_button.setOffset(0)
        self.shadow_reset_button.setOffset(6)
        self.resetcheck = 1

    def reset_button_clicked(self):
        request = QMessageBox.question(self,'Message', 'Are you sure to reset?')
        if request == QMessageBox.Yes:
            QMessageBox.information(self,"information","Program Reset")
            self.datahub.communication_stop()
            self.datahub.datasaver_stop()
            self.now_status.setText(ws.wait_status)
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.reset_button.setEnabled(False)
            self.rf_port_edit.setEnabled(False)
            self.shadow_start_button.setOffset(6)
            self.shadow_stop_button.setOffset(0)
            self.shadow_reset_button.setOffset(0)
            self.graphviewer.graph_clear()
            self.datahub.clear()
            self.resetcheck = 0
        else:
            QMessageBox.information(self,"information","Cancel")

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


class TimeAxisItem(AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [str(timedelta(milliseconds = millis))[:-4] for millis in values]

#  Analysis1
class SubWindow(PageWindow):
    def __init__(self,datahub):
        super().__init__()
        
        self.datahub = datahub
        self.timespace = None
        self.initUI()
        self.initGraph()
        self.initMenubar()

    def initUI(self):
        self.csv_name_edit = QLineEdit("{}".format(self.datahub.file_Name),self)
        self.analysis_button = QPushButton("Analysis", self)
        self.analysis_angular_button = QPushButton("Angular Data Analysis", self)
        self.analysis_alnsp_button = QPushButton("Altitude & Speed Analysis", self)
        self.set_range_button = QPushButton("Reset range", self)
        self.max_altitude_label = QLabel("Max. altitude",self)
        self.max_speed_label = QLabel("Max. speed",self)
        self.max_accel_label = QLabel("Max. acceleration", self)

        self.max_altitude = QLabel("0 ",self)
        self.max_speed = QLabel("0 ",self)
        self.max_accel = QLabel("0 ", self)

        self.max_altitude_label.setStyleSheet("font-weight: bold;")
        self.max_speed_label.setStyleSheet("font-weight: bold;")
        self.max_accel_label.setStyleSheet("font-weight: bold;")
        self.max_altitude.setStyleSheet("font-weight: bold;")
        self.max_speed.setStyleSheet("font-weight: bold;")
        self.max_accel.setStyleSheet("font-weight: bold;")
        self.analysis_button.setStyleSheet("font-weight: bold;")
        self.analysis_angular_button.setStyleSheet("font-weight: bold;")
        self.analysis_alnsp_button.setStyleSheet("font-weight: bold;")
        self.set_range_button.setStyleSheet("font-weight: bold;")
        self.csv_name_edit.setStyleSheet("background-color: rgb(250,250,250);")

        self.csv_name_edit.setGeometry(*ws.csv_name_geometry)
        self.analysis_button.setGeometry(*ws.analysis_button_geometry)
        self.analysis_angular_button.setGeometry(*ws.analysis_angular_button_geometry)
        self.analysis_alnsp_button.setGeometry(*ws.analysis_alnsp_button_geometry)
        self.set_range_button.setGeometry(*ws.set_range_geometry)
        self.max_altitude_label.setGeometry(*ws.max_altitude_label_geometry)
        self.max_speed_label.setGeometry(*ws.max_speed_label_geometry)
        self.max_accel_label.setGeometry(*ws.max_accel_label_geometry)
        self.max_altitude.setGeometry(*ws.max_altitude_geometry)
        self.max_speed.setGeometry(*ws.max_speed_geometry)
        self.max_accel.setGeometry(*ws.max_accel_geometry)
        

        self.max_altitude_label.setFont(ws.font_max_alti_label_text)
        self.max_speed_label.setFont(ws.font_max_speed_label_text)
        self.max_accel_label.setFont(ws.font_max_accel_label_text)
        self.max_altitude.setFont(ws.font_max_alti_text)
        self.max_speed.setFont(ws.font_max_speed_text)
        self.max_accel.setFont(ws.font_max_accel_text)

        self.analysis_button.clicked.connect(self.start_analysis)
        self.analysis_angular_button.clicked.connect(self.start_angularGraph)
        self.analysis_alnsp_button.clicked.connect(self.start_alnspGraph)
        self.set_range_button.clicked.connect(self.reset_range)

        path = abspath(__file__)
        dir_path = dirname(path)
        file_path_logo = join(dir_path, 'team_logo.png')

        self.irri_logo = QLabel(self)
        self.irri_logo.setPixmap(QPixmap(file_path_logo).scaled(*ws.irri_logo_geometry[2:4], Qt.KeepAspectRatio))
        self.irri_logo.setGeometry(*ws.irri_logo_geometry)  

    def initGraph(self):
        self.gr_angle = PlotWidget(self, axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.gr_angleSpeed = PlotWidget(self, axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.gr_accel = PlotWidget(self, axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.gr_altitude = PlotWidget(self, axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.gr_speed = PlotWidget(self, axisItems={'bottom': TimeAxisItem(orientation='bottom')})

        self.gr_angle.setGeometry(*ws.gr_angle_geometry)
        self.gr_angleSpeed.setGeometry(*ws.gr_angleSpeed_geometry)
        self.gr_accel.setGeometry(*ws.gr_accel_geometry)
        self.gr_altitude.setGeometry(*ws.gr_angle_geometry)
        self.gr_speed.setGeometry(*ws.gr_angleSpeed_geometry)

        self.gr_angle.addItem(GridItem())
        self.gr_angleSpeed.addItem(GridItem())
        self.gr_accel.addItem(GridItem())
        self.gr_altitude.addItem(GridItem())
        self.gr_speed.addItem(GridItem())

        self.gr_angle.getPlotItem().getAxis('left').setLabel('Degree')
        self.gr_angleSpeed.getPlotItem().getAxis('left').setLabel('Degree/second')
        self.gr_accel.getPlotItem().getAxis('left').setLabel('g(gravity accel)')
        self.gr_altitude.getPlotItem().getAxis('left').setLabel('Altitude')
        self.gr_speed.getPlotItem().getAxis('left').setLabel('Speed')

        self.gr_angle.getPlotItem().addLegend()
        self.gr_angleSpeed.getPlotItem().addLegend()
        self.gr_accel.getPlotItem().addLegend()
        self.gr_altitude.getPlotItem().addLegend()
        self.gr_speed.getPlotItem().addLegend()

        self.curve_roll = self.gr_angle.plot(pen='r', name = "roll")
        self.curve_pitch = self.gr_angle.plot(pen='g',name = "pitch")
        self.curve_yaw = self.gr_angle.plot(pen='b', name = "yaw")

        self.curve_rollSpeed = self.gr_angleSpeed.plot(pen='r', name = "roll speed")
        self.curve_pitchSpeed = self.gr_angleSpeed.plot(pen='g', name = "pitch speed")
        self.curve_yawSpeed = self.gr_angleSpeed.plot(pen='b', name = "yaw speed")

        self.curve_xaccel = self.gr_accel.plot(pen='r', name = "x acc")
        self.curve_yaccel = self.gr_accel.plot(pen='g',name = "y acc")
        self.curve_zaccel = self.gr_accel.plot(pen='b',name ="z acc")

        self.curve_altitude = self.gr_altitude.plot(pen='r', name = "altitude")

        self.curve_speed = self.gr_speed.plot(pen='r', name = "speed")

        self.gr_altitude.hide()
        self.gr_speed.hide()
        self.analysis_angular_button.setEnabled(False)
        self.analysis_alnsp_button.setEnabled(True)

    def start_angularGraph(self):
        self.gr_altitude.hide()
        self.gr_speed.hide()
        self.gr_angle.show()
        self.gr_angleSpeed.show()
        self.gr_accel.show()
        self.analysis_angular_button.setEnabled(False)
        self.analysis_alnsp_button.setEnabled(True)

        
    def start_alnspGraph(self):
            self.gr_angle.hide()
            self.gr_angleSpeed.hide()
            self.gr_accel.hide()
            self.gr_altitude.show()
            self.gr_speed.show()
            self.analysis_angular_button.setEnabled(True)
            self.analysis_alnsp_button.setEnabled(False)

    def initMenubar(self):
        self.statusBar()

        change_Action = QAction('Real-Time Viewer', self)
        change_Action.setShortcut('Ctrl+L')
        change_Action.triggered.connect(self.gomain)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.setStyleSheet("QMenuBar {background-color: rgb(130,130,130);color: rgb(255,255,255);border: 1px solid #000;}")

        filemenu = menubar.addMenu('Menu')
        filemenu.addAction(change_Action)

    def start_analysis(self):
        self.csv_name = self.csv_name_edit.text()
        try:
            alldata = read_csv(self.csv_name).to_numpy()
            init_time = alldata[0,0]*3600+alldata[0,1]*60+alldata[0,2]+alldata[0,3]*0.01
            self.timespace = alldata[:,0]*3600000+alldata[:,1]*60000+alldata[:,2]*1000+alldata[:,3]*10

            self.roll = alldata[:,4]
            self.pitch = alldata[:,5]
            self.yaw = alldata[:,6]

            self.rollSpeed = alldata[:,7]
            self.pitchSpeed = alldata[:,8]
            self.yawSpeed = alldata[:,9]

            self.xaccel = alldata[:,10]
            self.yaccel = alldata[:,11]
            self.zaccel = alldata[:,12]
            self.altitude = alldata[:,15]
            self.speed = alldata[:,16]
            print(type(self.speed))
            self.curve_roll.setData(x=self.timespace,y=self.roll)
            self.curve_pitch.setData(x=self.timespace,y=self.pitch)
            self.curve_yaw.setData(x=self.timespace,y=self.yaw)

            self.curve_rollSpeed.setData(x=self.timespace,y=self.rollSpeed)
            self.curve_pitchSpeed.setData(x=self.timespace,y=self.pitchSpeed)
            self.curve_yawSpeed.setData(x=self.timespace,y=self.yawSpeed)

            self.curve_xaccel.setData(x=self.timespace,y=self.xaccel)
            self.curve_yaccel.setData(x=self.timespace,y=self.yaccel)
            self.curve_zaccel.setData(x=self.timespace,y=self.zaccel)

            self.curve_altitude.setData(x=self.timespace,y=self.altitude)

            self.curve_speed.setData(x=self.timespace,y=self.speed)

            total_accel = (self.xaccel**2+self.yaccel**2+self.zaccel**2)**(0.5)
            self.max_altitude.setText("{:.2f} m".format(max(self.altitude)))
            self.max_speed.setText("{:.2f} m/s".format(max(self.speed)))
            self.max_accel.setText("{:.2f} g".format(max(total_accel)))

            self.start_angularGraph()

        except:
            QMessageBox.warning(self,"warning","File open error")

    def gomain(self):
        self.goto("main")

    def reset_range(self):
        if self.timespace is not None:
            self.gr_angle.setXRange(min(self.timespace),max(self.timespace))
            self.gr_angleSpeed.setXRange(min(self.timespace),max(self.timespace))
            self.gr_accel.setXRange(min(self.timespace),max(self.timespace))
            self.gr_speed.setXRange(min(self.timespace),max(self.timespace))
            self.gr_altitude.setXRange(min(self.timespace),max(self.timespace))

            self.gr_angle.setYRange(min(min(self.roll),min(self.pitch),min(self.yaw)),max(max(self.roll),max(self.pitch),max(self.yaw)))
            self.gr_angleSpeed.setYRange(min(min(self.rollSpeed),min(self.pitchSpeed),min(self.yawSpeed)),max(max(self.rollSpeed),max(self.pitchSpeed),max(self.yawSpeed)))
            self.gr_accel.setYRange(min(min(self.xaccel),min(self.yaccel),min(self.zaccel)),max(max(self.xaccel),max(self.yaccel),max(self.zaccel)))
            self.gr_speed.setYRange(min(self.speed),max(self.speed))
            self.gr_altitude.setYRange(min(self.altitude),max(self.altitude))

class window(QMainWindow):
    def __init__(self,datahub):
        self.app = QApplication(argv)
        super().__init__()
        self.datahub = datahub

        self.initUI()
        self.initWindows()
        self.goto("main")

    def initUI(self):
        self.resize(*ws.full_size)
        self.setWindowTitle('I-link')
        self.setStyleSheet(ws.mainwindow_color) 

        path = abspath(__file__)
        dir_path = dirname(path)
        file_path = join(dir_path, 'window_logo.ico')
        self.setWindowIcon(QIcon(file_path))


    def initWindows(self):
        self.mainwindow = MainWindow(self.datahub)
        self.subwindow = SubWindow(self.datahub)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.mainwindow)
        self.stacked_widget.addWidget(self.subwindow)

        self.mainwindow.gotoSignal.connect(self.goto)
        self.subwindow.gotoSignal.connect(self.goto)

    @pyqtSlot(str)
    def goto(self, name):
        if name == "main":
            self.stacked_widget.setCurrentWidget(self.mainwindow)

        if name == "sub":
            self.stacked_widget.setCurrentWidget(self.subwindow)
            self.subwindow.csv_name_edit.setText("{}".format(self.datahub.file_Name))

    def start(self):
        self.show()
        
    def setEventLoop(self):
        exit(self.app.exec_())

    def closeEvent(self, event):
        self.datahub.communication_stop()
        self.datahub.datasaver_stop()
        event.accept()