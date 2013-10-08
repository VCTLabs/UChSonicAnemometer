#
# Copyright (C) 2013  UNIVERSIDAD DE CHILE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luis Alberto Herrera <herrera.luis.alberto@gmail.com>

import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import adc_reader
import generate_timeframe
import matplotlib
import uniform_sampled_signal
import utilities
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('UChSonicAnemometer Live View')

        self.autoscale = True

        self.reader = adc_reader.ADCReader()

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

        self.on_draw()
        

    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"
        
        path = unicode(QFileDialog.getSaveFileName(self, 
                        'Save file', '', 
                        file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)
    
    def on_draw(self):
        """ Redraws the figure
        """
        # clear the axes and redraw the plot anew
        #
        
        x_limits = self.axes.get_xlim()
        y_limits = self.axes.get_ylim()
        self.axes.clear()
        signal = self.reader.get_frame()
        responses = utilities.split_signal(signal)
        self.axes.plot(responses["NORTH"].get_timestamp_array(),
                       responses["NORTH"].values, '-')
        if not self.autoscale:
          self.axes.set_xlim(x_limits)
          self.axes.set_ylim(y_limits)
        self.canvas.draw()
        self.autoscale = False

    def self_on_capture(self):
      """ Callback for capture button. """
      if self.recording_check.isChecked():
        try:
          os.mkdir("records")
        except OSError:
          pass
        for i in range(self.recording_repetitions.value()):
          filename = "records/%s_%04d.bin"%(self.recording_name.text(), i)
          self.reader.dump_frame_to_file(filename)
      self.on_draw()

    def create_main_frame(self):
        self.main_frame = QWidget()

        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure(dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)

        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        self.draw_button = QPushButton("&Capture")
        self.connect(self.draw_button, SIGNAL('clicked()'), self.self_on_capture)

        self.recording_check = QCheckBox("Recording")
        self.recording_name = QLineEdit()
        self.recording_repetitions = QSpinBox()
        self.recording_repetitions.setRange(1, 99);

        #
        # Layout with box sizers
        #
        hbox = QHBoxLayout()

        for w in [self.draw_button, self.recording_check,
                  QLabel("Recording Name: "), self.recording_name,
                  QLabel("Repetitions: "), self.recording_repetitions]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        vbox.addLayout(hbox)

        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("This is a demo")
        self.statusBar().addWidget(self.status_text, 1)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plot,
            tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close,
            shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu,
            (load_file_action, None, quit_action))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
