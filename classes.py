import sys
import os
absolute_path = os.path.abspath(sys.argv[0])
directory_path = os.path.dirname(absolute_path)

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, QGridLayout, QPushButton, QFileDialog, QToolBar, QAction, QStatusBar, QTabWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor, QMovie, QImage
from PyQt5.QtCore import QFile, QTextStream, QTimer, QSettings, QDateTime, QTime, Qt, QSize
from images import *
from text_files import *

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(self.palette)
        self.setFixedWidth(70)
        self.setFixedHeight(70)

class Une_Partie(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialisation des attributs
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.move(200, 200)
        self.show()
        
        self.joueur_actif = "bleu"  # Définir le joueur actif
        self.pion_selectionne = None  # Pour stocker le pion sélectionné
        self.cases_suggerees = []  # Pour stocker les cases suggérées pour le déplacement

        # Création des boutons de la grille
        for i in range(10):
            for j in range(10):
                self.bouton_100 = QPushButton(self)
                self.bouton_100.setMinimumSize(75,75)
                self.layout.addWidget(self.bouton_100, i, j)  
                self.bouton_100.coords = (i, j) 
                self.bouton_100.clicked.connect(lambda _, b=self.bouton_100: self.deplacements_pions(b))

                # Configurer les boutons en fonction de la position
                if i%2 == 0 and 3<i<6:
                    if j%2 == 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: darkgrey; color:darkgrey; border-radius: 5px")
                        self.bouton_100.coords = (i,j)
                    elif j%2 != 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: black; border-radius: 5px")
                        self.bouton_100.coords = (i,j)
                        
                if i%2 != 0 and 3<i<6:
                    if j%2 == 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: black; border-radius: 5px")
                        self.bouton_100.coords = (i,j)
                    elif j%2 != 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: darkgrey; color:darkgrey; border-radius: 5px")
                        self.bouton_100.coords = (i,j)
                    
                if i%2 == 0 and 0<=i<4:
                    if j%2 == 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: darkgrey; color:darkgrey; border-radius: 5px")
                        self.bouton_100.coords = (i,j)
                    elif j%2 != 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: black; border-radius: 5px")
                        self.bouton_100.setIcon(QIcon(os.path.join(directory_path, 'images/pion-bleu.png')))
                        self.bouton_100.setIconSize(QSize(50, 50))
                        self.bouton_100.coords = (i,j)

                if i%2 != 0 and 0<=i<4:
                    if j%2 == 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: black; border-radius: 5px")
                        self.bouton_100.setIcon(QIcon(os.path.join(directory_path, 'images/pion-bleu.png')))
                        self.bouton_100.setIconSize(QSize(50, 50))
                        self.bouton_100.coords = (i,j)
                    else:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: darkgrey; color:darkgrey; border-radius: 5px") 
                        self.bouton_100.coords = (i,j)

                if i%2 != 0 and 10>i>5:
                    if j%2 == 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: black; border-radius: 5px")
                        self.bouton_100.setIcon(QIcon(os.path.join(directory_path, 'images/pion-noir.png')))
                        self.bouton_100.setIconSize(QSize(50, 50))
                        self.bouton_100.coords = (i,j)
                    elif j%2 != 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: darkgrey; color:darkgrey; border-radius: 5px")
                        self.bouton_100.coords = (i,j)
                        
                if i%2 == 0 and 10>i>5:
                    if j%2 == 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: darkgrey; color:darkgrey; border-radius: 5px")
                        self.bouton_100.coords = (i,j)
                    elif j%2 != 0:
                        self.layout.addWidget(self.bouton_100,i,j)
                        self.bouton_100.setStyleSheet("background-color: black; border-radius: 5px")
                        self.bouton_100.setIcon(QIcon(os.path.join(directory_path, 'images/pion-noir.png')))
                        self.bouton_100.setIconSize(QSize(50, 50))
                        self.bouton_100.coords = (i,j)

        self.changer_joueur_actif()
        
    def deplacements_pions(self, bouton_100):
        print("Clic sur le bouton :", bouton_100.coords)
        if bouton_100.icon() and not bouton_100.icon().isNull():
            # Si un pion est sélectionné, afficher les cases suggérées pour le déplacement
            self.afficher_cases_suggerees(bouton_100)
        elif bouton_100 in self.cases_suggerees:
            # Si une case suggérée est sélectionnée, déplacer le pion sélectionné vers cette case
            self.deplacer_pion(self.pion_selectionne, bouton_100)
            # Réinitialiser la sélection et les cases suggérées
            self.pion_selectionne = None
            self.vider_cases_suggerees()
            # Changer de joueur
            self.changer_joueur_actif()

    def afficher_cases_suggerees(self, bouton_depart):
        # Réinitialiser les cases suggérées précédentes
        self.vider_cases_suggerees()
        # Récupérer les coordonnées du pion sélectionné
        i, j = bouton_depart.coords
        # Ajouter les cases suggérées pour le déplacement diagonal
        directions = [(1, -1), (1, 1)]
        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]
            if 0 <= new_i < 10 and 0 <= new_j < 10:
                neighbor_button = self.layout.itemAtPosition(new_i, new_j).widget()
                if not neighbor_button.icon():
                    self.cases_suggerees.append(neighbor_button)
                    neighbor_button.setStyleSheet("background-color: lightblue; border-radius: 5px")

    def deplacer_pion(self, bouton_depart, bouton_arrivee):
        print("Déplacement du pion :", bouton_depart.coords, "->", bouton_arrivee.coords)
        # Échanger les icônes entre le bouton de départ et le bouton d'arrivée
        bouton_arrivee.setIcon(bouton_depart.icon())
        bouton_depart.setIcon(QIcon())
        # Réinitialiser la taille de l'icône
        bouton_depart.setIconSize(QSize())
    
    def vider_cases_suggerees(self):
        # Réinitialiser les styles des cases suggérées
        for case in self.cases_suggerees:
            case.setStyleSheet("")
        # Vider la liste des cases suggérées
        self.cases_suggerees = []

    def changer_joueur_actif(self):
        self.joueur_actif = "noir" if self.joueur_actif == "bleu" else "bleu"
        print(f"Joueur actif : {self.joueur_actif}")

class Minuteur(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.time = QTime(00,00,00)
        self.widget = QWidget()
        self.glayout = QGridLayout()
        
        self.label_intro_time = QLabel("Le minuteur démarrera ici: ")
        self.label_intro_time.setAlignment(Qt.AlignCenter)
        self.label_intro_time.setStyleSheet("font-size: 20px; font-style:bold")
        self.label_intro_date = QLabel("Voici la date d'aujourd'hui: ")
        self.label_intro_date.setAlignment(Qt.AlignCenter)
        self.label_intro_date.setStyleSheet("font-size: 20px; font-style:bold")
        self.label_time = QLabel("Time")
        self.label_time.setAlignment(Qt.AlignCenter)
        self.label_time.setStyleSheet("color: red; font-size: 20px; font-style:italic")
        self.label_date = QLabel("Boom l'heure")
        self.label_date.setAlignment(Qt.AlignCenter)
        self.label_date.setStyleSheet("font-size: 20px; font-style:italic")
       
        self.widget.setLayout(self.glayout)
        self.setCentralWidget(self.widget)
        
        time_now = QDateTime.currentDateTime()
        self.time_display_now = time_now.toString("dddd MM-dd-yyyy hh:mm:ss")
        self.label_date.setText(self.time_display_now)
        self.glayout.addWidget(self.label_intro_date,0,0)
        self.glayout.addWidget(self.label_intro_time,1,0)
        self.glayout.addWidget(self.label_date,0,1)
        self.glayout.addWidget(self.label_time,1,1)
        
        self.move(300,300)
        self.bouton_start = QPushButton("Start",self)
        self.bouton_start.setStyleSheet("color: purple")
        self.bouton_stop = QPushButton("Stop",self)
        self.bouton_stop.setStyleSheet("color: purple")
        self.show()     
        
        self.timer.timeout.connect(self.showTime)
        self.bouton_start.move(75,75)
        self.bouton_stop.move(50,50)
        self.glayout.addWidget(self.bouton_start)
        self.bouton_start.clicked.connect(self.startTimer)
        self.glayout.addWidget(self.bouton_stop)
        self.bouton_stop.clicked.connect(self.stopTimer)
        
    def showTime(self):
        self.time = self.time.addSecs(1)
        self.time_display = self.time.toString("hh:mm:ss")
        self.label_time.setText(self.time_display)
        
    def startTimer(self):
        self.timer.start(1000)
        self.bouton_start.setEnabled(False)
        self.bouton_stop.setEnabled(True)
        
    def stopTimer(self):
        self.timer.stop()
        self.bouton_start.setEnabled(True)
        self.bouton_stop.setEnabled(False)           

class Interface_presentation(QMainWindow):
    def __init__(self):
        
        super().__init__()
        self.setWindowTitle("Menu du jeu de dame")
        self.setStyleSheet("background-color: gainsboro")
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.label_HvsH = QLabel("")
        self.label_HvsH.setAlignment(Qt.AlignCenter)
        self.label_HvsM = QLabel("")
        self.label_HvsM.setAlignment(Qt.AlignCenter)
        self.move(300,300)
        self.toolbar = QToolBar("Barre d'outils Menu du jeu de dame")
        self.addToolBar(self.toolbar)
        self.show()
        
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        self.movie_HvsH = QMovie(os.path.join(directory_path, "images/Kirito vs Boss Floor.gif"))
        self.movie_HvsM = QMovie(os.path.join(directory_path, "images/Humans vs Decepticon Transformer.gif"))
        
        self.bouton_HvsH = QPushButton("Jeu entre vous et un autre joueur",self)
        self.bouton_HvsH.setStyleSheet("color: purple;font: 19px bold; border-radius: 5px; border-style: outset; border-color: black; border-width: 2px")
        self.bouton_HvsH.setStatusTip("Un petite game entre 2 joueurs compétents!")
        self.bouton_HvsM = QPushButton("Jeu entre vous et une machine virtuel",self)
        self.bouton_HvsM.setStyleSheet("color: purple; font: 19px bold; border-radius: 5px; border-style: outset; border-color: black; border-width: 2px")
        self.bouton_HvsM.setStatusTip("Qui remportera cette manche ?Joueur ou Machine?")
        
        self.layout.addWidget(self.label_HvsH)
        self.layout.addWidget(self.bouton_HvsH)
        self.bouton_HvsH.clicked.connect(self.click_HvsH)
        self.label_HvsH.setMovie(self.movie_HvsH)
        self.layout.addWidget(self.label_HvsM)
        self.layout.addWidget(self.bouton_HvsM)
        self.bouton_HvsM.clicked.connect(self.click_HvsM)
        self.label_HvsM.setMovie(self.movie_HvsM)
        
        self.label_HvsH.setScaledContents(True)
        self.movie_HvsH.start()
        self.movie_HvsM.start()
        
        self.Manuel = QAction(QIcon(os.path.join(directory_path, "images/book--pencil.png")), "Manuel", self)
        self.Manuel.setStatusTip("Manuel pour se servir du jeu !")
        self.Manuel.triggered.connect(self.Lecture_Manuel)
        
        self.Apropos = QAction(QIcon(os.path.join(directory_path, "images/information-octagon.png")), "A propos", self)
        self.Apropos.setStatusTip("A props de notre Projet Final d'IHM")
        self.Apropos.triggered.connect(self.Lecture_A_propos)
        
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        self.menuAide = self.menuBar().addMenu("&Aide")
        self.menuAide.addAction(self.Manuel)
        self.menuAide.addAction(self.Apropos) 
        
        self.toolbar.addAction(self.Manuel)
        self.toolbar.addAction(self.Apropos)
    
    def click_HvsH(self):
        print("Ouverture de l'inteface Joueur vs Joueur (Jeu de dame)\n")
        print("Bonne chance chers joueurs! Vous en aurez besoin!")
        self.Window = jeu_de_dame_JvsJ()
        self.Window.show()
        self.close()
        
    def click_HvsM(self):
        print("Ouverture de l'inteface Joueur vs Ordinateur (Jeu de dame)\n")
        print("Bonne chance cher joueur! Vous en aurez besoin, la bataille sera rude!")
        self.Window = jeu_de_dame_JvsM()
        self.Window.show()
        self.close()
        
    def Lecture_A_propos(self):
        File = open(os.path.join(directory_path, "text_files/Message-A-propos.txt"), "r", encoding = "utf-8")
        Texte = ""
        for ligne in File.readlines():
            Texte += ligne
            self.read = QMessageBox(QMessageBox.Information, "Présentation du projet", Texte)
            self.read.show()  
    
    def Lecture_Manuel(self):
        File = open(os.path.join(directory_path, "text_files/Manuel de jeu.txt"), "r", encoding = "utf-8")
        Texte = ""
        for ligne in File.readlines():
            Texte += ligne
            self.read = QMessageBox(QMessageBox.NoIcon, "Présentation du projet", Texte)
            self.read.show()
            
class jeu_de_dame_JvsJ(QMainWindow):     
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joueur vs Joueur version 'Jeu de dame'")
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.setStyleSheet("background-color :gainsboro")
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.move(200, 200)
        self.toolbar = QToolBar("Barre d'outils")
        self.addToolBar(self.toolbar)
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.setFixedSize(760,860)
        self.show()
        
        #Dictionnaire pour stocker les positions des pions
        self.positions_pions = {}

        #Initialiser le plateau
        self.initialiser_plateau()
        self.pion_selectionne = None
        self.cases_suggerees = []

        self.Nouvellepartie = QAction(QIcon(os.path.join(directory_path, "images/new-text.png")), "Nouvelle Partie", self)
        self.Nouvellepartie.setStatusTip("Commencer une nouvelle Partie !")
        self.Nouvellepartie.triggered.connect(self.Nvllepartie)
            
        self.Chargerpartie = QAction(QIcon(os.path.join(directory_path, "images/blue-folder-horizontal-open.png")), "Charger une partie", self)
        self.Chargerpartie.setStatusTip("Charger une partie en cours !")
        self.Chargerpartie.triggered.connect(self.Charger_Partie)
         
        self.Sauvegarder = QAction(QIcon(os.path.join(directory_path, "images/downloading-bar-final.png")),"Sauvegarder", self)
        self.Sauvegarder.setStatusTip("Sauvegarder une partie !")
        self.Sauvegarder.triggered.connect(self.Sauvegarder_Partie)
        
        self.DeplacementLive = QAction(QIcon(os.path.join(directory_path, "images/pions-loupe-v1.jpg")),"Déplacements Live", self)
        self.DeplacementLive.setStatusTip("Affiche chaque déplacement lorsqu’il est effectué !")
        #self.DeplacementLive.triggered.connect(self.)
        
        self.EnsembleDeplacement = QAction(QIcon(os.path.join(directory_path, "images/stratégie-pions_v1.jpg")),"Déplacements de la partie", self)
        self.EnsembleDeplacement.setStatusTip("Affiche l'historique des déplacements de la partie en cours !")
        
        self.HistoriqueDeplacement = QAction(QIcon(os.path.join(directory_path, "images/sablier-pions-v1.png")),"Déplacements Parties Précédentes", self)
        self.HistoriqueDeplacement.setStatusTip("Affiche l'historique des déplacements d'une partie précédente !")
        
        self.SauvegarderHistorique = QAction(QIcon(os.path.join(directory_path, "images/disk.png")),"Sauvegarder Deplacements", self)
        self.SauvegarderHistorique.setStatusTip("Sauvegarde l'historique des déplacements !")
        
        self.Manuel = QAction(QIcon(os.path.join(directory_path, "images/book--pencil.png")), "Manuel", self)
        self.Manuel.setStatusTip("Manuel pour se servir du jeu !")
        self.Manuel.triggered.connect(self.Lecture_Manuel)
        
        self.Apropos = QAction(QIcon(os.path.join(directory_path, "images/information-octagon.png")), "A propos", self)
        self.Apropos.setStatusTip("A props de notre Projet Final d'IHM")
        self.Apropos.triggered.connect(self.Lecture_A_propos)
      
        self.menuFichier = self.menuBar().addMenu("&Fichier")
        self.menuFichier.addAction(self.Nouvellepartie)
        self.menuFichier.addAction(self.Chargerpartie)
        self.menuFichier.addAction(self.Sauvegarder)
        
        self.menuHistorique = self.menuBar().addMenu("&Historique")
        self.menuHistorique.addAction(self.DeplacementLive)
        self.menuHistorique.addAction(self.EnsembleDeplacement)
        self.menuHistorique.addAction(self.HistoriqueDeplacement)
        self.menuHistorique.addAction(self.SauvegarderHistorique)
        
        self.menuAide = self.menuBar().addMenu("&Aide")
        self.menuAide.addAction(self.Manuel)
        self.menuAide.addAction(self.Apropos) 
        
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        self.toolbar.addAction(self.Nouvellepartie)
        self.toolbar.addAction(self.Chargerpartie)
        self.toolbar.addAction(self.Sauvegarder)
        self.toolbar.addAction(self.DeplacementLive)
        self.toolbar.addAction(self.EnsembleDeplacement)
        self.toolbar.addAction(self.HistoriqueDeplacement)
        self.toolbar.addAction(self.Manuel)
        self.toolbar.addAction(self.Apropos)
        
        self.label1 = QLabel("Joueur 1: ")
        self.label1.setStyleSheet("color: purple; font-size: 15px bold")
        self.label2 = QLabel('Joueur 2: ')
        self.label2.setStyleSheet("color: purple; font-size: 15px bold")
        self.statusbar.addWidget(self.label1)
        self.statusbar.addPermanentWidget(self.label2)
        
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.Fermer_Onglet)
        self.configuration = QSettings("Projet final IHM", "Jeu de dame", self)

    def initialiser_plateau(self):
        for i in range(10):
            for j in range(10):
                bouton_100 = QPushButton(self)
                bouton_100.setMinimumSize(75, 75)
                self.layout.addWidget(bouton_100, i, j)
                bouton_100.coords = (i, j)
                bouton_100.clicked.connect(self.gestion_clic)
                # Initialiser les pions bleus
                if i % 2 != j % 2 and 0 <= i < 4:
                    self.ajouter_pion(bouton_100, 'bleu')
                # Initialiser les pions noirs
                elif i % 2 != j % 2 and 6 <= i < 10:
                    self.ajouter_pion(bouton_100, 'noir')

    def ajouter_pion(self, bouton, couleur):
        if couleur == 'bleu':
            bouton.setIcon(QIcon(os.path.join(directory_path, 'images/pion-bleu.png')))
            bouton.setStyleSheet("background-color: black; border-radius: 5px")
        else:
            bouton.setIcon(QIcon(os.path.join(directory_path, 'images/pion-noir.png')))
            bouton.setStyleSheet("background-color: black; border-radius: 5px")
        bouton.setIconSize(QSize(50, 50))
        self.positions_pions[bouton.coords] = couleur

    def afficher_cases_suggerees(self):
        self.effacer_cases_suggerees()
        x, y = self.pion_selectionne.coords
        
        self.ajouter_case_suggeree(x + 1, y - 1)
        self.ajouter_case_suggeree(x + 1, y + 1)
        for case in self.cases_suggerees:
            case.setStyleSheet("background-color: yellow; border-radius: 5px")

    def ajouter_case_suggeree(self, x, y):
        if 0 <= x < 10 and 0 <= y < 10:
            bouton = self.layout.itemAtPosition(x, y).widget()
            if bouton.icon().isNull():
                bouton.setStyleSheet("background-color: green")
                self.cases_suggerees.append(bouton)

    def effacer_cases_suggerees(self):
        for bouton in self.cases_suggerees:
            bouton.setStyleSheet("")
        self.cases_suggerees = []

    def gestion_clic(self):
        bouton = self.sender()
        self.pion_selectionne = bouton.coords
        print("Position des cases: ", self.pion_selectionne)
        print("La position des pions est: ", self.positions_pions)
        print("Voici les cases suggérées: ", self.cases_suggerees)

        if self.pion_selectionne and bouton in self.cases_suggerees:
            coord_depart = self.pion_selectionne.coords
            coord_arrivee = bouton.coords
            print("Déplacement du pion bleu de", coord_depart, "à", coord_arrivee)
            self.effacer_cases_suggerees()
            self.positions_pions[coord_arrivee] = self.positions_pions[coord_depart]
            del self.positions_pions[coord_depart]
            self.actualiser_affichage()
            self.pion_selectionne = None
        else:
            if bouton.icon().isNull(): 
                return
            pixmap = bouton.icon().pixmap(QSize(50, 50))
            image = pixmap.toImage()
            if image.pixelColor(0, 0) == QColor('blue'):
                self.pion_selectionne = bouton
                self.afficher_cases_suggerees()
                print("Pion bleu sélectionné aux coordonnées:", bouton.coords)
                print("Cases suggérées:", [case.coords for case in self.cases_suggerees])

    def actualiser_affichage(self):
        for coords, couleur in self.positions_pions.items():
            bouton = self.layout.itemAtPosition(coords[0], coords[1]).widget()
            if couleur == 'bleu':
                bouton.setIcon(QIcon(os.path.join(directory_path, 'images/pion-bleu.png')))
            else:
                bouton.setIcon(QIcon(os.path.join(directory_path, 'images/pion-noir.png')))
            bouton.setIconSize(QSize(50, 50))
        
    def Fermer_Onglet(self,fermer):
        self.close = self.tabs.widget(fermer)
        self.close.deleteLater()
        
    def Nvllepartie(self):
        self.tabs.addTab(Une_Partie(),"New Game")
        self.tabs.addTab(Minuteur(),"Minuteur")
        self.setCentralWidget(self.tabs)
        
    def Lecture_A_propos(self):
        File = open(os.path.join(directory_path, "text_files/Message-A-propos.txt"), "r", encoding = "utf-8")
        Texte = ""
        for ligne in File.readlines():
            Texte += ligne
            self.read = QMessageBox(QMessageBox.NoIcon, "Présentation du projet", Texte)
            self.read.show()
            self.scroll(0,1)
                
    def Lecture_Manuel(self):
        File = open(os.path.join(directory_path, "text_files/Manuel de jeu.txt"), "r", encoding = "utf-8")
        Texte = ""
        for ligne in File.readlines():
            Texte += ligne
            self.read = QMessageBox(QMessageBox.NoIcon, "Présentation du projet", Texte)
            self.read.show()
            self.scroll(0,1)

#------------------------Partie déplacements de pions-------------------------#
#--------------------------------Pions bleus----------------------------------#
    def deplacements_pions_bleus(self, bouton_100):
        i, j = bouton_100.coords
        # Directions possibles pour le déplacement des pions bleus
        directions = [(1, -1), (1, 1)]
        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]
            if 0 <= new_i < 10 and 0 <= new_j < 10:  
                neighbor_button = self.layout.itemAtPosition(new_i, new_j).widget()
                if neighbor_button.styleSheet() == "background-color: black; border-radius: 5px" and neighbor_button.icon().isNull():
                    neighbor_button.setStyleSheet("background-color: lightblue; border-radius: 5px")
                    neighbor_button.clicked.connect(lambda _, b=bouton_100, nb=neighbor_button: self.move_piece(b, nb, "bleu"))

#--------------------------------Pions noirs----------------------------------#
    def deplacements_pions_noirs(self, bouton_100):
        i, j = bouton_100.coords
        # Directions possibles pour le déplacement des pions noirs
        directions = [(-1, -1), (-1, 1)]
        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]
            if 0 <= new_i < 10 and 0 <= new_j < 10:
                neighbor_button = self.layout.itemAtPosition(new_i, new_j).widget()
                if neighbor_button.styleSheet() == "background-color: black; border-radius: 5px" and neighbor_button.icon().isNull():
                    neighbor_button.setStyleSheet("background-color: lightblue; border-radius: 5px")
                    neighbor_button.clicked.connect(lambda _, b=bouton_100, nb=neighbor_button: self.move_piece(b, nb, "noir"))
    
    def move_piece(self, start_button, end_button, pion):
        # Efface le bouton de départ
        start_button.setIcon(QIcon())
        # Déplace le pion vers la case de destination
        if pion == "bleu":
            end_button.setIcon(QIcon(os.path.join(directory_path, 'images/pion-bleu.png')))
        if pion == "noir":
            end_button.setIcon(QIcon(os.path.join(directory_path, 'images/pion-noir.png')))
        end_button.clicked.disconnect()  # Désactive le clic sur la case de destination

    def Charger_Partie(self):
        OpenPartie = QFileDialog()
        path =  OpenPartie.getOpenFileName(parent = None, caption = "Charger une partie", filter = 'Fichier avec extension (*.jd)')
        print(path)
        
       #Charger_partie = self.configuration.value("Jeu de dame chargée")
        file = QFile(os.path.join(directory_path, "Sauvegarde de la partie.jd"))
        f = file.open(QFile.ReadOnly)
        if f:
            flux = QTextStream(file)
            flux.readAll()
            file.close()
            print("La partie est en train de se charger. Veuillez patientez...")
            self.statusBar().showMessage("Vous pouvez reprendre la partie")
        else:
            print("Erreur de lecture du fichier.\n")
            print("La partie ne peut pas se charger car vous n'avez peut-être pas sauvegarder auparavant. Restez vigilant la prochaine fois XD !")
            print("Cliquer sur le bouton <Sauvegarder> pour charger votre partie sans aucune perte de données.")
   
    def Sauvegarder_Partie(self):
        self.configuration.setValue("Jeu de dame", Une_Partie())
        fichier_sauvegarder = self.configuration.value("Jeu de dame")
        file = QFile(os.path.join(directory_path, "Sauvegarde de la partie.jd"))
        f = file.open(QFile.WriteOnly)
        if f:
            flux = QTextStream(file)
            flux << fichier_sauvegarder
            file.close()
            print("La sauvegarde de la partie a bien été effectuée.")
            print("Vous pouvez la reprendre en cliquant sur <Charger une partie>.")
        else:
            print("Il se peut que la sauvegarde n'ait pas eu lieu, ou mette du temps.")

class jeu_de_dame_JvsM(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joueur vs Ordinateur version 'Jeu de dame'")
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.setStyleSheet("background-color :gainsboro")
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.move(200, 200)
        self.toolbar = QToolBar("Barre d'outils")
        self.addToolBar(self.toolbar)
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.setFixedSize(760,860)
        self.show()
        
        self.Nouvellepartie = QAction(QIcon(os.path.join(directory_path, "images/new-text.png")), "Nouvelle Partie", self)
        self.Nouvellepartie.setStatusTip("Commencer une nouvelle Partie !")
        self.Nouvellepartie.triggered.connect(self.Nvllepartie)
            
        self.Chargerpartie = QAction(QIcon(os.path.join(directory_path, "images/blue-folder-horizontal-open.png")), "Charger une partie", self)
        self.Chargerpartie.setStatusTip("Charger une partie en cours !")
        self.Chargerpartie.triggered.connect(self.Charger_Partie)
         
        self.Sauvegarder = QAction(QIcon(os.path.join(directory_path, "images/downloading-bar-final.png")),"Sauvegarder", self)
        self.Sauvegarder.setStatusTip("Sauvegarder une partie !")
        self.Sauvegarder.triggered.connect(self.Sauvegarder_Partie)
        
        self.DeplacementLive = QAction(QIcon(os.path.join(directory_path, "images/pions-loupe-v1.jpg")),"Déplacements Live", self)
        self.DeplacementLive.setStatusTip("Affiche chaque déplacement lorsqu’il est effectué !")
        #self.DeplacementLive.triggered.connect(self.)
        
        self.EnsembleDeplacement = QAction(QIcon(os.path.join(directory_path, "images/stratégie-pions_v1.jpg")),"Déplacements de la partie", self)
        self.EnsembleDeplacement.setStatusTip("Affiche l'historique des déplacements de la partie en cours !")
        
        self.HistoriqueDeplacement = QAction(QIcon(os.path.join(directory_path, "images/sablier-pions-v1.png")),"Déplacements Parties Précédentes", self)
        self.HistoriqueDeplacement.setStatusTip("Affiche l'historique des déplacements d'une partie précédente !")
        
        self.SauvegarderHistorique = QAction(QIcon(os.path.join(directory_path, "images/disk.png")),"Sauvegarder Deplacements", self)
        self.SauvegarderHistorique.setStatusTip("Sauvegarde l'historique des déplacements !")
        
        self.Manuel = QAction(QIcon(os.path.join(directory_path, "images/book--pencil.png")), "Manuel", self)
        self.Manuel.setStatusTip("Manuel pour se servir du jeu !")
        self.Manuel.triggered.connect(self.Lecture_Manuel)
        
        self.Apropos = QAction(QIcon(os.path.join(directory_path, "images/information-octagon.png")), "A propos", self)
        self.Apropos.setStatusTip("A props de notre Projet Final d'IHM")
        self.Apropos.triggered.connect(self.Lecture_A_propos)
      
        self.menuFichier = self.menuBar().addMenu("&Fichier")
        self.menuFichier.addAction(self.Nouvellepartie)
        self.menuFichier.addAction(self.Chargerpartie)
        self.menuFichier.addAction(self.Sauvegarder)
        
        self.menuHistorique = self.menuBar().addMenu("&Historique")
        self.menuHistorique.addAction(self.DeplacementLive)
        self.menuHistorique.addAction(self.EnsembleDeplacement)
        self.menuHistorique.addAction(self.HistoriqueDeplacement)
        self.menuHistorique.addAction(self.SauvegarderHistorique)
        
        self.menuAide = self.menuBar().addMenu("&Aide")
        self.menuAide.addAction(self.Manuel)
        self.menuAide.addAction(self.Apropos) 
        
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        self.toolbar.addAction(self.Nouvellepartie)
        self.toolbar.addAction(self.Chargerpartie)
        self.toolbar.addAction(self.Sauvegarder)
        self.toolbar.addAction(self.DeplacementLive)
        self.toolbar.addAction(self.EnsembleDeplacement)
        self.toolbar.addAction(self.HistoriqueDeplacement)
        self.toolbar.addAction(self.Manuel)
        self.toolbar.addAction(self.Apropos)
        
        self.label1 = QLabel("Joueur 1: ")
        self.label1.setStyleSheet("color: purple; font-size: 15px bold")
        self.label2 = QLabel('Joueur 2: ')
        self.label2.setStyleSheet("color: purple; font-size: 15px bold")
        self.statusbar.addWidget(self.label1)
        self.statusbar.addPermanentWidget(self.label2)
        
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.Fermer_Onglet)
        
        self.configuration = QSettings("Projet final IHM", "Jeu de dame", self)
        
    def Fermer_Onglet(self,fermer):
        self.close = self.tabs.widget(fermer)
        self.close.deleteLater()
        
    def Nvllepartie(self):
        self.tabs.addTab(Une_Partie(),"New Game")
        self.tabs.addTab(Minuteur(),"Minuteur")
        self.setCentralWidget(self.tabs)
        
    def Lecture_A_propos(self):
        File = open(os.path.join(directory_path, "text_files/Message-A-propos.txt"), "r", encoding = "utf-8")
        Texte = ""
        for ligne in File.readlines():
            Texte += ligne
            self.read = QMessageBox(QMessageBox.NoIcon, "Présentation du projet", Texte)
            self.read.show()
                
    def Lecture_Manuel(self):
        File = open(os.path.join(directory_path, "text_files/Manuel de jeu.txt"), "r", encoding = "utf-8")
        Texte = ""
        for ligne in File.readlines():
            Texte += ligne
            self.read = QMessageBox(QMessageBox.NoIcon, "Présentation du projet", Texte)
            self.read.show()
            self.scroll(0,1)
        
#------------------------Partie difficile lol-------------------------
    def deplacements_pions_bleus(self):#Pour les pions bleus
        self.bouton_100.setIcon(QIcon())
        """
        sender = self.sender().coords
        for i in range(10):
            for j in range(10):
                if self.bouton_100.coords == (i,j):
                    sender += (i,j)
        """
    def Charger_Partie(self):
        OpenPartie = QFileDialog()
        path =  OpenPartie.getOpenFileName(parent = None, caption = "Charger une partie", filter = 'Fichier avec extension (*.jd)')
        print(path)
        
       #Charger_partie = self.configuration.value("Jeu de dame chargée")
        file = QFile(os.path.join(directory_path, "Sauvegarde de la partie.jd"))
        f = file.open(QFile.ReadOnly)
        if f:
            flux = QTextStream(file)
            flux.readAll()
            file.close()
            print("La partie est en train de se charger. Veuillez patientez...")
            self.statusBar().showMessage("Vous pouvez reprendre la partie")
        else:
            print("Erreur de lecture du fichier.\n")
            print("La partie ne peut pas se charger car vous n'avez peut-être pas sauvegarder auparavant. Restez vigilant la prochaine fois XD !")
            print("Cliquer sur le bouton <Sauvegarder> pour charger votre partie sans aucune perte de données.")
   
    def Sauvegarder_Partie(self):
        self.configuration.setValue("Jeu de dame", Une_Partie())
        fichier_sauvegarder = self.configuration.value("Jeu de dame")
        file = QFile(os.path.join(directory_path, "Sauvegarde de la partie.jd"))
        f = file.open(QFile.WriteOnly)
        if f:
            flux = QTextStream(file)
            flux << fichier_sauvegarder
            file.close()
            print("La sauvegarde de la partie a bien été effectuée.")
            print("Vous pouvez la reprendre en cliquant sur <Charger une partie>.")
        else:
            print("Il se peut que la sauvegarde n'ait pas eu lieu, ou mette du temps.")     