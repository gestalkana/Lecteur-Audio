import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QSlider, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lecteur Audio')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.web_view = QWebEngineView()
        self.web_view.setHtml(self.get_html())
        layout.addWidget(self.web_view)

        self.setLayout(layout)

        self.list_widget.currentItemChanged.connect(self.update_current_item)

    def get_html(self):
        html = """
        <html>
            <head>
                <style>
                    .button {
                        background-color: #3498db;
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        margin: 5px;
                        border-radius: 5px;
                        font-size: 14px;
                    }
                    .button:hover {
                        background-color: #2980b9;
                    }
                    .button:active {
                        background-color: #2c3e50;
                    }
                </style>
            </head>
            <body>
                <button id="playButton" class="button">Play</button>
                <button id="pauseButton" class="button">Pause</button>
                <button id="stopButton" class="button">Stop</button>
            </body>
            <script>
                var playButton = document.getElementById("playButton");
                var pauseButton = document.getElementById("pauseButton");
                var stopButton = document.getElementById("stopButton");

                playButton.addEventListener("click", function() {
                    alert("Play button clicked!");
                });

                pauseButton.addEventListener("click", function() {
                    alert("Pause button clicked!");
                });

                stopButton.addEventListener("click", function() {
                    alert("Stop button clicked!");
                });
            </script>
        </html>
        """
        return html

    def update_current_item(self, current, previous):
        if current:
            print("Selected:", current.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec_())
