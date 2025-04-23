import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QSlider, QListWidget, QListWidgetItem,QGridLayout
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QSize, QFileInfo
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer, Qt, QPoint


class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lecteur Audio Informatiako')
        self.setGeometry(100, 100, 400, 300)
        self.setMinimumSize(555,355)
        layout = QVBoxLayout()

        # Créer un en-tête pour la liste de lecture
        #self.list_header = QLabel("Liste de lecture")
        #self.list_header.setStyleSheet("font-weight: bold; font-size: 16px;")  # Style de l'en-tête
        #layout.addWidget(self.list_header)

        self.list_widget = QListWidget()
        #self.list_widget.setModelColumn(2)
        #self.list_widget.setStyleSheet("QListWidget { background-color: #CCCCCC; }")  # Changement de couleur de fond
        layout.addWidget(self.list_widget, stretch=9)
        self.list_widget.hide()  # Cacher la liste de lecture par défaut

        # Fond noir pour cacher la liste de lecture
        self.black_background = QLabel()
        self.black_background.setStyleSheet("background-color: black;")
        layout.addWidget(self.black_background, stretch=9)

        # Charger l'icône par défaut
        pixmap = QPixmap("icons8-music-240.png")
        self.black_background.setPixmap(pixmap)  # Définir l'icône sur le label
        self.black_background.setAlignment(Qt.AlignCenter)  # Centrer le contenu du label

        #Affichage du titre du media en lecture
        self.current_Mediaplaying_label = QLabel("Titre actuel")
        self.current_Mediaplaying_label.setStyleSheet("font-weight: bold; font-size: 16px;")  # Style de l'en-tête
        self.current_Mediaplaying_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_Mediaplaying_label)

        # Bouton pour basculer la visibilité de la liste de lecture
        self.toggle_button = QPushButton("Basculer")
        self.toggle_button.clicked.connect(self.toggle_list_visibility)


        self.media_player = QMediaPlayer()
        self.media_player.setVolume(50)

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("play.png"))
        self.play_button.clicked.connect(self.play)

        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon("pause.png"))
        self.pause_button.clicked.connect(self.pause)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon("stop.png"))
        self.stop_button.clicked.connect(self.stop)

        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon("previous.png"))
        self.prev_button.clicked.connect(self.prev_track)

        self.open_button = QPushButton('Ouvrir')
        #self.open_button.setIcon(QIcon("icons8-bibliothèque-musicale-100.png"))
        self.open_button.clicked.connect(self.open_file)

        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon("next.png"))
        self.next_button.clicked.connect(self.next_track)

        self.file_label = QLabel()

        self.duration_label = QLabel()
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.position_slider.sliderPressed.connect(self.change_position)
        self.position_slider.mousePressEvent = self.slider_mousePressEvent  # Nouveau gestionnaire d'événements

        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_slider.mousePressEvent = self.volume_slider_mousePressEvent  # Nouveau gestionnaire d'événements

        self.volume_label = QLabel("50%") #Volume de la media
        self.duration_label = QLabel("00:00")
        #self.volume_label.setAlignment(Qt.AlignBottom)

        self.current_position_label = QLabel("00:00")

        button_layout = QHBoxLayout()
        #button_layout.addWidget(self.play_button)
        #button_layout.addWidget(self.pause_button)
        #button_layout.addWidget(self.stop_button)
        #button_layout.addWidget(self.prev_button)
        #button_layout.addWidget(self.next_button)
        #button_layout.addWidget(self.toggle_button)
        #button_layout.addWidget(self.open_button)

        button_layout.addStretch(1)  # Ajouter un stretch avant les boutons pour les pousser à gauche
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.open_button)
        button_layout.addStretch(1)  # Ajouter un stretch après les boutons pour les pousser à droite

        # Ajoutez ces lignes pour définir la taille minimale des boutons
        self.play_button.setMaximumSize(50, 50)
        self.pause_button.setMaximumSize(50, 50)
        self.stop_button.setMaximumSize(50, 50)
        self.prev_button.setMaximumSize(50, 50)
        self.next_button.setMaximumSize(50, 50)
        self.toggle_button.setMinimumSize(70, 50)  # Ajustez la largeur pour s'adapter au texte "Basculer"
        self.open_button.setMinimumSize(70, 50)

        #layout.addWidget(self.duration_label)
        #layout.addWidget(self.current_position_label)
        #layout.addWidget(self.position_slider)
        #layout.addWidget(self.volume_label)
        #layout.addWidget(self.volume_slider)

        lecture_layout = QHBoxLayout()

        lecture_layout.addWidget(self.current_position_label)
        lecture_layout.addWidget(self.position_slider)
        lecture_layout.addWidget(self.duration_label)

        layout.addLayout(lecture_layout)


        volume_layout = QHBoxLayout()

        button_layout.addWidget(self.volume_label)
        button_layout.addWidget(self.volume_slider) #Pour que le volume se place au même ligne que les boutons


        layout.addLayout(volume_layout)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.positionChanged.connect(self.update_current_position)
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)

        # Appliquer le style QSS
        self.setStyleSheet("""
            QPushButton {
                background-color: #008b8b; /*darkCyan*/
                border: none;
                color: white;
                padding: 10px 20px;
                margin: 5px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2c3e50;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
            QSlider {
                background-color: #d8bfd8; /*thistle*/
            }
            QSlider::groove:horizontal {
                height: 5px;
                margin: 0px;
            }
            QSlider::handle:horizontal {
                background-color: #3498db;
                border: 1px solid #2980b9;
                width: 15px;
                height: 15px;
                margin: -5px 0px;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #008b8b;
            }
            QSlider::add-page:horizontal {
                background: #bdc3c7;
            }
            QSlider::add-page:horizontal:disabled {
                background: #bdc3c7;
            }
            QSlider::handle:horizontal:hover {
                background-color: #2980b9;
                border: 1px solid #2980b9;
            }
           QListWidget {
                background-color: #FFFFFF; /* Couleur de fond */
                border: 1px solid #CCCCCC; /* Bordure */
                padding: 5px; /* Espacement intérieur */
            }
            QListWidget::item {
            /*background-color: #FFFFFF; *//* Couleur de fond des éléments */
            padding: 5px; /* Espacement intérieur des éléments */
            }
            QListWidget::item:selected {
            background-color: #3498db; /* Couleur de fond des éléments sélectionnés */
            color: #FFFFFF; /* Couleur du texte des éléments sélectionnés */
            }
        """)

        # Connecter le signal itemClicked de QListWidget à la méthode play_from_list
        self.list_widget.itemDoubleClicked.connect(self.play_from_list)

    def play(self):
        current_item = self.list_widget.currentItem()
        if current_item is not None:
            file_path = current_item.data(Qt.UserRole)
            if self.media_player.state() == QMediaPlayer.StoppedState:
                self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.media_player.play()
            # Affichage du titre de la musique
            file_info = QFileInfo(file_path)
            title = file_info.fileName()
            self.current_Mediaplaying_label.setText(title)
            self.current_Mediaplaying_label.adjustSize()  # Ajuster la taille du label pour s'adapter au texte

    def pause(self):
        self.media_player.pause()

    def stop(self):
        self.media_player.stop()

    def open_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)  # Permettre la sélection de plusieurs fichiers
        file_dialog.setNameFilter("Audio Files (*.mp3 *.wav)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()  # Récupérer la liste des chemins des fichiers sélectionnés
            for file_path in file_paths:
                file_info = QFileInfo(file_path)
                title = file_info.fileName()
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, file_path)
                self.list_widget.addItem(item)
                if self.media_player.state() != QMediaPlayer.PlayingState:
                    self.play()
                if self.list_widget.count() == 1:
                    self.list_widget.setCurrentItem(item)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def update_position(self, position):
        self.position_slider.setValue(position)

    def update_duration(self, duration):
        self.position_slider.setRange(00, duration)
        minutes = int(duration / 60000)
        seconds = int((duration - minutes * 60000) / 1000)
        self.duration_label.setText(f"{minutes} : {seconds} ") #Durée totale de la musique

    def change_position(self):
        position = self.position_slider.value()
        self.media_player.setPosition(position)

    def change_volume(self, volume):
        self.media_player.setVolume(volume)
        self.volume_label.setText(f"{volume}%") #Volume de la media

    def prev_track(self):
        self.stop()
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            self.list_widget.setCurrentRow(current_row - 1)
            self.play()

    def next_track(self):
        self.stop()
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1:
            self.list_widget.setCurrentRow(current_row + 1)
            self.play()

    def slider_mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            position = int(self.position_slider.minimum() + ((self.position_slider.maximum() - self.position_slider.minimum()) * event.x()) / self.position_slider.width())
            self.media_player.setPosition(position)

    def slider_mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            position = int(self.position_slider.minimum() + ((self.position_slider.maximum() - self.position_slider.minimum()) * event.x()) / self.position_slider.width())
            self.media_player.setPosition(position)

    def volume_slider_mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            volume = self.volume_slider.maximum() - int((self.volume_slider.maximum() * event.y()) / self.volume_slider.height())
            self.volume_slider.setValue(volume)
            self.media_player.setVolume(volume)
            self.volume_label.setText(f" {volume}%") #Volume de la media

    def update_current_position(self, position):
        minutes = int(position / 60000)
        seconds = int((position - minutes * 60000) / 1000)
        self.current_position_label.setText(f" {minutes} : {seconds}") #Durée Ecoulé de la lecture

    def play_from_list(self, item):
        self.stop()
        file_path = item.data(Qt.UserRole)
        if self.media_player.state() == QMediaPlayer.StoppedState:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.media_player.play()
       #affichage du titre de la media
        file_info = QFileInfo(file_path)
        title = file_info.fileName()
        self.current_Mediaplaying_label.setText(title)
        self.current_Mediaplaying_label.adjustSize()  # Ajuster la taille du label pour s'adapter au texte

    def toggle_list_visibility(self):
        if self.list_widget.isVisible():
            self.list_widget.hide()
            pixmap = QPixmap("icons8-music-240.png")  # Charger l'icône
            self.black_background.setPixmap(pixmap)  # Définir l'icône sur le label
            self.black_background.setAlignment(Qt.AlignCenter)  # Centrer le contenu du label
            self.black_background.show()
            self.current_Mediaplaying_label.show()
        else:
            self.list_widget.show()
            self.black_background.clear()  # Efface l'image précédente
            self.black_background.hide()
            self.current_Mediaplaying_label.hide()

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.next_track()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec_())