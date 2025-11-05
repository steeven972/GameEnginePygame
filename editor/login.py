
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTreeWidget, QTreeWidgetItem, 
                               QTextEdit, QToolBar, QDockWidget, QLabel,
                               QListWidget, QSplitter, QPushButton, QFileDialog,
                               QMenuBar, QMenu, QStatusBar, QMessageBox,
                               QInputDialog, QTabWidget, QScrollArea)
from PySide6.QtCore import Qt, QSize, QTimer, Signal
from PySide6.QtGui import QAction, QIcon, QColor, QPalette, QPixmap, QPainter, QPen
import json
import os


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Hello !")
        self.setGeometry(100, 100, 1420, 680)

        self.create_menu()
        self.create_toolbar()

    def create_toolbar(self):
        """Crée la toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Boutons
        play_btn = QPushButton("▶ Play")
        play_btn.clicked.connect(self.play_scene)
        toolbar.addWidget(play_btn)
        
        pause_btn = QPushButton("⏸ Pause")
        toolbar.addWidget(pause_btn)
        
        stop_btn = QPushButton("⏹ Stop")
        toolbar.addWidget(stop_btn)
        
        toolbar.addSeparator()
        
        add_entity_btn = QPushButton("+ Entité")
        add_entity_btn.clicked.connect(self.add_entity)
        toolbar.addWidget(add_entity_btn)
        
    def create_menu(self):
        """Crée le menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        
        new_action = QAction("New Project", self)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("open Project", self)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Close", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Édition
        edit_menu = menubar.addMenu("Edition")
        
        add_entity_action = QAction("Add Entity", self)
        add_entity_action.triggered.connect(self.add_entity)
        edit_menu.addAction(add_entity_action)
        
        # Menu Vue
        view_menu = menubar.addMenu("Show")
        
   
    def play_scene(self):
        """Lance la scène"""
        self.console.log("Lancement de la scène...", "info")
        QMessageBox.information(self, "Play", "Fonctionnalité à implémenter:\nLancement du jeu avec Pygame")
        
    def new_project(self):
        """Crée un nouveau projet"""
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier du projet")
        if folder:
            self.project_path = folder
            self.console.log(f"Nouveau projet créé: {folder}", "success")
            self.hierarchy.clear_all()
            self.viewport.entities = []
            self.viewport.update()
            
    def open_project(self):
        """Ouvre un projet existant"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Ouvrir un projet", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.current_scene = data
                    
                    # Charger les entités
                    self.hierarchy.clear_all()
                    self.viewport.entities = []
                    
                    for entity in data.get('entities', []):
                        self.hierarchy.add_entity(entity)
                        self.viewport.entities.append(entity)
                    
                    self.viewport.update()
                    self.console.log(f"Projet chargé: {file_path}", "success")
            except Exception as e:
                self.console.log(f"Erreur lors du chargement: {str(e)}", "error")
                
    def save_project(self):
        """Sauvegarde le projet"""
        if not self.project_path:
            file_path, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le projet", "", "JSON Files (*.json)")
            if not file_path:
                return
        else:
            file_path = os.path.join(self.project_path, "scene.json")
        
        try:
            self.current_scene['entities'] = self.hierarchy.get_all_entities()
            
            with open(file_path, 'w') as f:
                json.dump(self.current_scene, f, indent=2)
            
            self.console.log(f"Projet sauvegardé: {file_path}", "success")
        except Exception as e:
            self.console.log(f"Erreur lors de la sauvegarde: {str(e)}", "error")

    def add_entity(self):

        
        """Ajoute une nouvelle entité"""
        name, ok = QInputDialog.getText(self, "Nouvelle Entité", "Nom de l'entité:")
        
        if ok and name:
            entity = {
                "name": name,
                "x": 100,
                "y": 100,
                "width": 64,
                "height": 64,
                "type": "GameObject",
                "components": []
            }
            
            self.hierarchy.add_entity(entity)
            self.viewport.entities.append(entity)
            self.viewport.update()
            self.console.log(f"Entité '{name}' ajoutée", "success")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()
    sys.exit(app.exec())