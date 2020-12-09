from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow


class FollowWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Follow Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

class UnFollowWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("UnFollow Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None
        self.followBtn = QPushButton("Auto Follow")
        self.followBtn.clicked.connect(self.openAutoFollowWindow)

        self.unfollowBtn = QPushButton("Auto UnFollow")
        self.unfollowBtn.clicked.connect(self.openAutoFollowWindow)

        self.centralW = QWidget()

        self.centralLayout = QVBoxLayout()
        self.centralLayout.addWidget(self.followBtn)
        self.centralLayout.addWidget(self.unfollowBtn)

        self.centralW.setLayout(self.centralLayout)


        self.setCentralWidget(self.centralW)


    def openAutoFollowWindow(self):
        if self.w is not None:
            self.w.close()
        self.w = FollowWindow()
        self.w.show()

    def openAutoUnFollowWindow(self):
        if self.w is not None:
            self.w.close()
        self.w = FollowWindow()
        self.w.show()




app = QApplication([])
w = MainWindow()
w.show()

app.exec_()