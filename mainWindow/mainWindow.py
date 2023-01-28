from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox, QInputDialog
from PyQt5.QtCore import QObject, QThread, pyqtSlot, QRunnable, QThreadPool, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import sys, os

class MapViewer_Thread(QThread):
    def __init__(self, mainwindow,datahub):
        super().__init__()
        self.mainwindow = mainwindow
        self.datahub= datahub
        # self.setWindowTitle("Real-time Dynamic Map")

        # Create the QWebEngineView widget
        self.view = QWebEngineView(self.mainwindow)
        self.view.setGeometry(240,180, 800, 600)
        
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
        print("showed")

class MainWindow(QMainWindow):
    def __init__(self, datahub):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.datahub = datahub
        self.resize(1280,960)
        
        """Set Buttons"""
        self.start_button = QPushButton("Press Start",self,)
        self.stop_button = QPushButton("Stop",self,)
        self.rf_port_edit = QLineEdit("COM8",self)
        
        self.rf_port_edit.setEnabled(True)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        """Set Buttons Connection"""
        self.start_button.clicked.connect(self.start_button_clicked)
        self.stop_button.clicked.connect(self.stop_button_clicked)
        
        """Set Geometry"""
        QLabel("Enter your Serial Port:",self).setGeometry(1050,320,200,30)
        self.rf_port_edit.setGeometry(1050,350,200,30)
        self.start_button.setGeometry(1050,400,200,150)
        self.stop_button.setGeometry(1050,600,200,150)
        
        
        """Set Viewer Thread"""
        self.mapviewer = MapViewer_Thread(self,datahub)

        self.mapviewer.start()

    # Run when start button is clicked
    def start_button_clicked(self):
        QMessageBox.information(self,"information","Program Start")
        FileName,ok = QInputDialog.getText(self,'Input Dialog', 'Enter your File Name',QLineEdit.Normal,"Your File Name")
        if ok:
            self.mySerialPort=self.rf_port_edit.text()
            self.datahub.file_Name = FileName+'.csv'
            self.datahub.communication_start()
            self.datahub.datasaver_start()
            
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.rf_port_edit.setEnabled(False)
        else:
            QMessageBox.warning(self,"warning","Cancel")
        

    # Run when stop button is clicked
    def stop_button_clicked(self):
        QMessageBox.information(self,"information","Program Stop")
        self.datahub.communication_stop()
        self.datahub.datasaver_stop()
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)     
        
    # Main Window start method
    def start(self):
        self.show()
        
    def setEventLoop(self):
        sys.exit(self.app.exec_())
        
    # Run when mainwindow is closed
    def closeEvent(self, event):
        QMessageBox.warning(self, "Warning", "Program Closed.")
        event.accept()