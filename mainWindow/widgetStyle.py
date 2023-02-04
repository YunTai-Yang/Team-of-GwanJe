from pyautogui import size as max_window_size
from PyQt5.QtGui import QFont
import numpy as np
import sys, os

width, height = max_window_size()
height = int(0.95*height)

a = width
b = height
# a : 가로, b : 세로
full_size = np.array([a,b]).astype(int)

mainwindow_color = "background-color: rgb(160, 160, 160);"

webEngine_geometry = np.array([a*0.07,  b*0.04,  b*0.04, b*0.04]).astype(int)

# graph geometry
pw_angle_geometry = np.array([a*0.07,  b*0.04,  a*0.3,  b*0.28]).astype(int)
pw_angleSpeed_geometry = np.array([a*0.07,  b*0.36,  a*0.3,  b*0.28]).astype(int)
pw_accel_geometry = np.array([a*0.07,  b*0.68,  a*0.3,  b*0.28]).astype(int)

angle_title_geometry = np.array([a*0.15, b*0.015, 200, 30]).astype(int)
angleSpeed_title_geometry = np.array([a*0.15, b*0.335, 200, 30]).astype(int)
accel_title_geometry = np.array([a*0.15, b*0.655, 200, 30]).astype(int)

# checker geometry
roll_checker_geomoetry = np.array([a*0.02,  b*0.07,  100,  50]).astype(int)
pitch_checker_geomoetry = np.array([a*0.02, b*0.11,  100,  50]).astype(int)
yaw_checker_geomoetry = np.array([a*0.02,   b*0.15,  100,  50]).astype(int)

rollS_checker_geomoetry = np.array([a*0.02,  b*0.39, 100,  50]).astype(int)
pitchS_checker_geomoetry = np.array([a*0.02,  b*0.43, 100,  50]).astype(int)
yawS_checker_geomoetry = np.array([a*0.02,  b*0.47, 100,  50]).astype(int)

ax_checker_geomoetry = np.array([a*0.02,  b*0.71,  100,  30]).astype(int)
ay_checker_geomoetry = np.array([a*0.02,  b*0.75,  100,  30]).astype(int)
az_checker_geomoetry = np.array([a*0.02,  b*0.79,  100,  30]).astype(int)

# 
map_geometry = np.array([a*0.41,  b*0.04,  a*0.3,  a*0.3]).astype(int)

# serial port editer geometry
port_text_geometry = np.array([a*0.41,  a*0.26+b*0.132, a*0.04, a*0.01125]).astype(int)
port_edit_geometry = np.array([a*0.46,  a*0.26+b*0.132,  a*0.06, a*0.01125]).astype(int)

# serial baudrate editer geometry
baudrate_text_geometry = np.array([a*0.41,  a*0.28+b*0.132, a*0.04, a*0.01125]).astype(int)
baudrate_edit_geometry = np.array([a*0.46,  a*0.28+b*0.132,  a*0.06, a*0.01125]).astype(int)

# start/stop button geometry
start_geometry = np.array([a*0.41,  0.132*b+0.3*a,  0.12*a,  0.12*a ]).astype(int)
stop_geometry = np.array([a*0.56, a*0.27+b*0.132, 0.15*a, 0.15*a]).astype(int)
status_geometry = np.array([a*0.41,  0.14*b+0.42*a, 0.3*a, 35]).astype(int)

# 
model_geometry = np.array([a*0.75,  b*0.04,  a*0.2, a*0.3]).astype(int)
speed_label_geometry = np.array([a*0.8, 0.04*b+0.26*a, 250,30]).astype(int)

# 
cmd_geometry = np.array([a*0.74, 0.24*a+0.132*b,  a*0.22,  0.17*a]).astype(int)

# 
irri_logo_geometry = np.array([a*0.83, 0.89*b,  a*0.15,  0.1*b]).astype(int)


# all fonts
font_portText = QFont()
font_portText.setPointSize(11)

font_baudrate = QFont()
font_baudrate.setPointSize(11)

checker_font = QFont()
checker_font.setPointSize(12)

font_guideText = QFont()
font_guideText.setPointSize(10)

font_angle_title = QFont()
font_angle_title.setPointSize(15)

font_angleSpeed_title = QFont()
font_angleSpeed_title.setPointSize(15)

font_accel_title = QFont()
font_accel_title.setPointSize(15)

font_start_text = QFont()
font_start_text.setPointSize(20)

font_stop_text = QFont()
font_stop_text.setPointSize(20)

font_status_text = QFont()
font_status_text.setPointSize(11)

font_speed_text = QFont()
font_speed_text.setPointSize(16)

start_status = 'Program start. you can push the stop button'
stop_status = 'Program stop. you can push the start button'

guide = """
1. Enter your serial port in the text box\n
2. Pust start button\n
3. Enter your save file name for save datas and \n     push ok button\n
3. You can push a check box left the graph to \n     hide a curve\n
4. You can drag a map or scroll the map to move view\n
5. All reveiced data is saved in real-time and saved in same folder\n
6. Push stop button
"""

### Sub window ###

csv_name_geometry = np.array([a*0.8, 0.8*b,  a*0.08, a*0.02]).astype(int)
analysis_button_geometry = np.array([a*0.8, 0.85*b,  a*0.08, a*0.02]).astype(int)

gr_angle_geometry = np.array([a*0.1,  b*0.04,  a*0.6,  b*0.28]).astype(int)
gr_angleSpeed_geometry = np.array([a*0.1,  b*0.36,  a*0.6,  b*0.28]).astype(int)
gr_accel_geometry = np.array([a*0.1,  b*0.68,  a*0.6,  b*0.28]).astype(int)