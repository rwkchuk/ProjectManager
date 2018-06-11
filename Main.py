#Robert Kowalchuk
''' THis python file kicks off the project manager '''
import GUI_Helper
import ProjectManager
import sys
from PyQt4 import QtGui


def main():
    app = QtGui.QApplication(sys.argv)

    projectManager = ProjectManager.Manager()
    gui = GUI_Helper.MainWindow(projectManager)

    sys.exit(app.exec_())



if __name__ == '__main__':
    main()