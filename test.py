import sys
import os
import pygame
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QToolBar,
                               QDockWidget, QTreeWidget, QTreeWidgetItem,
                               QTextEdit, QSplitter, QInputDialog, QFileDialog,
                               QMessageBox)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QImage, QPixmap, QPalette, QColor


class PygameWidget(QWidget):
    """Widget qui affiche le rendu Pygame"""
    def __init__(self, width=800, height=600):
        super().__init__()
        self.width = width
        self.height = height
        self.is_running = False
        
        # Initialiser Pygame
        pygame.init()
        
        # Créer une surface Pygame hors-écran
        self.pygame_surface = pygame.Surface((width, height))
        
        # Label pour afficher l'image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(width, height)
        self.image_label.setStyleSheet("border: 2px solid #444; background-color: black;")
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Timer pour rafraîchir l'affichage
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        
        # Données du jeu
        self.entities = []
        self.clock = pygame.time.Clock()
        self.fps = 60
        
    def set_entities(self, entities):
        """Définir les entités à afficher"""
        self.entities = entities
        
    def render_scene(self):
        """Rendu de la scène Pygame"""
        # Fond
        self.pygame_surface.fill((30, 30, 35))
        
        # Dessiner une grille
        grid_color = (50, 50, 55)
        grid_size = 32
        for x in range(0, self.width, grid_size):
            pygame.draw.line(self.pygame_surface, grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, grid_size):
            pygame.draw.line(self.pygame_surface, grid_color, (0, y), (self.width, y))
        
        # Dessiner les entités
        for entity in self.entities:
            x = entity.get('x', 0)
            y = entity.get('y', 0)
            w = entity.get('width', 50)
            h = entity.get('height', 50)
            color = entity.get('color', (100, 150, 255))
            
            # Rectangle de l'entité
            pygame.draw.rect(self.pygame_surface, color, (x, y, w, h))
            pygame.draw.rect(self.pygame_surface, (200, 200, 255), (x, y, w, h), 2)
            
            # Nom de l'entité
            font = pygame.font.Font(None, 24)
            text = font.render(entity.get('name', 'Entity'), True, (255, 255, 255))
            self.pygame_surface.blit(text, (x + 5, y + 5))
    
    def update_display(self):
        """Convertir la surface Pygame en QPixmap et l'afficher"""
        self.render_scene()
        
        # Convertir la surface Pygame en QImage
        pygame_string = pygame.image.tostring(self.pygame_surface, 'RGB')
        qimage = QImage(pygame_string, self.width, self.height, self.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        
        # Afficher dans le label
        self.image_label.setPixmap(pixmap)
    
    def start_preview(self):
        """Démarre la prévisualisation"""
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000 // self.fps)  # 60 FPS
    
    def stop_preview(self):
        """Arrête la prévisualisation"""
        self.is_running = False
        self.timer.stop()


class GameThread(QThread):
    """Thread pour exécuter la boucle principale du jeu Pygame"""
    log_signal = Signal(str, str)
    
    def __init__(self, entities, width=800, height=600):
        super().__init__()
        self.entities = entities
        self.width = width
        self.height = height
        self.running = True
        
    def run(self):
        """Boucle principale du jeu"""
        try:
            # Initialiser Pygame avec une vraie fenêtre
            pygame.init()
            screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Game Running - Press ESC to quit")
            clock = pygame.time.Clock()
            
            self.log_signal.emit("Jeu démarré en mode plein écran", "success")
            
            # Variables du jeu
            player_speed = 5
            keys_pressed = {}
            
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        keys_pressed[event.key] = True
                    elif event.type == pygame.KEYUP:
                        keys_pressed[event.key] = False
                
                # Déplacer les entités (exemple simple)
                for entity in self.entities:
                    if entity.get('name') == 'Player':
                        if keys_pressed.get(pygame.K_LEFT):
                            entity['x'] -= player_speed
                        if keys_pressed.get(pygame.K_RIGHT):
                            entity['x'] += player_speed
                        if keys_pressed.get(pygame.K_UP):
                            entity['y'] -= player_speed
                        if keys_pressed.get(pygame.K_DOWN):
                            entity['y'] += player_speed
                        
                        # Limites de l'écran
                        entity['x'] = max(0, min(entity['x'], self.width - entity['width']))
                        entity['y'] = max(0, min(entity['y'], self.height - entity['height']))
                
                # Rendu
                screen.fill((30, 30, 35))
                
                # Grille
                grid_color = (50, 50, 55)
                for x in range(0, self.width, 32):
                    pygame.draw.line(screen, grid_color, (x, 0), (x, self.height))
                for y in range(0, self.height, 32):
                    pygame.draw.line(screen, grid_color, (0, y), (self.width, y))
                
                # Entités
                for entity in self.entities:
                    x = entity.get('x', 0)
                    y = entity.get('y', 0)
                    w = entity.get('width', 50)
                    h = entity.get('height', 50)
                    color = entity.get('color', (100, 150, 255))
                    
                    pygame.draw.rect(screen, color, (x, y, w, h))
                    pygame.draw.rect(screen, (200, 200, 255), (x, y, w, h), 2)
                    
                    font = pygame.font.Font(None, 24)
                    text = font.render(entity.get('name', 'Entity'), True, (255, 255, 255))
                    screen.blit(text, (x + 5, y + 5))
                
                # Instructions
                font = pygame.font.Font(None, 20)
                instructions = [
                    "Use Arrow Keys to move Player",
                    "Press ESC to quit"
                ]
                for i, instruction in enumerate(instructions):
                    text = font.render(instruction, True, (200, 200, 200))
                    screen.blit(text, (10, 10 + i * 25))
                
                pygame.display.flip()
                clock.tick(60)
            
            pygame.quit()
            self.log_signal.emit("Jeu arrêté", "info")
            
        except Exception as e:
            self.log_signal.emit(f"Erreur: {str(e)}", "error")
    
    def stop(self):
        """Arrête le thread"""
        self.running = False


class HierarchyPanel(QTreeWidget):
    """Panneau hiérarchique de la scène"""
    entitySelected = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.setHeaderLabel("Hiérarchie")
        self.entities = []
        self.itemClicked.connect(self.on_item_clicked)
        
    def add_entity(self, entity):
        """Ajoute une entité à la hiérarchie"""
        item = QTreeWidgetItem([entity.get('name', 'Entity')])
        item.setData(0, Qt.UserRole, entity)
        self.addTopLevelItem(item)
        self.entities.append(entity)
        
    def on_item_clicked(self, item):
        """Émet le signal quand une entité est sélectionnée"""
        entity = item.data(0, Qt.UserRole)
        if entity:
            self.entitySelected.emit(entity)
    
    def get_all_entities(self):
        """Retourne toutes les entités"""
        return self.entities
    
    def clear_all(self):
        """Efface toutes les entités"""
        self.clear()
        self.entities = []


class ConsoleWidget(QTextEdit):
    """Console de logs"""
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumHeight(150)
        
    def log(self, message, level="info"):
        """Ajoute un message au log"""
        color = {
            "info": "#cccccc",
            "warning": "#ffaa00",
            "error": "#ff4444",
            "success": "#44ff44"
        }.get(level, "#cccccc")
        
        self.append(f'<span style="color: {color};">[{level.upper()}] {message}</span>')


class GameEngineEditor(QMainWindow):
    """Fenêtre principale de l'éditeur avec intégration Pygame"""
    def __init__(self):
        super().__init__()
        self.game_thread = None
        
        self.setWindowTitle("Game Engine Editor - Pygame Integration")
        self.setGeometry(100, 100, 1400, 900)
        
        # Style sombre
        self.setup_dark_theme()
        
        # Menu et toolbar
        self.create_menu()
        self.create_toolbar()
        
        # Interface
        self.setup_ui()
        
        # Status bar
        self.statusBar().showMessage("Prêt")
        
        self.console.log("Éditeur initialisé avec Pygame", "success")
        
    def setup_dark_theme(self):
        """Applique un thème sombre"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(37, 37, 38))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 48))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(45, 45, 48))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)
        
    def create_menu(self):
        """Crée le menu"""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("Fichier")
        file_menu.addAction("Nouveau Projet", self.new_project)
        file_menu.addAction("Sauvegarder", self.save_project, "Ctrl+S")
        file_menu.addSeparator()
        file_menu.addAction("Quitter", self.close)
        
        edit_menu = menubar.addMenu("Édition")
        edit_menu.addAction("Ajouter Entité", self.add_entity)
        
    def create_toolbar(self):
        """Crée la toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Boutons de contrôle
        self.play_btn = QPushButton("▶ Play (Fullscreen)")
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.play_btn.clicked.connect(self.play_game)
        toolbar.addWidget(self.play_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #666;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_game)
        toolbar.addWidget(self.stop_btn)
        
        toolbar.addSeparator()
        
        preview_btn = QPushButton("👁 Preview")
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        preview_btn.clicked.connect(self.toggle_preview)
        toolbar.addWidget(preview_btn)
        
        toolbar.addSeparator()
        
        add_entity_btn = QPushButton("+ Entité")
        add_entity_btn.clicked.connect(self.add_entity)
        toolbar.addWidget(add_entity_btn)
        
    def setup_ui(self):
        """Configure l'interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Panneau gauche (Hiérarchie)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        hierarchy_label = QLabel("Hiérarchie de la Scène")
        hierarchy_label.setStyleSheet("font-weight: bold; padding: 5px; font-size: 14px;")
        left_layout.addWidget(hierarchy_label)
        
        self.hierarchy = HierarchyPanel()
        self.hierarchy.entitySelected.connect(self.on_entity_selected)
        left_layout.addWidget(self.hierarchy)
        
        main_splitter.addWidget(left_panel)
        
        # Centre (Viewport Pygame + Console)
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        
        viewport_label = QLabel("Pygame Preview")
        viewport_label.setStyleSheet("font-weight: bold; padding: 5px; font-size: 14px;")
        center_layout.addWidget(viewport_label)
        
        # Widget Pygame
        self.pygame_widget = PygameWidget(800, 600)
        center_layout.addWidget(self.pygame_widget, 1)
        
        console_label = QLabel("Console")
        console_label.setStyleSheet("font-weight: bold; padding: 5px; font-size: 14px;")
        center_layout.addWidget(console_label)
        
        self.console = ConsoleWidget()
        center_layout.addWidget(self.console)
        
        main_splitter.addWidget(center_panel)
        
        # Panneau droit (Propriétés)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        properties_label = QLabel("Propriétés")
        properties_label.setStyleSheet("font-weight: bold; padding: 5px; font-size: 14px;")
        right_layout.addWidget(properties_label)
        
        self.properties_text = QTextEdit()
        self.properties_text.setReadOnly(True)
        right_layout.addWidget(self.properties_text)
        
        main_splitter.addWidget(right_panel)
        
        # Tailles des panneaux
        main_splitter.setSizes([250, 850, 300])
        
        main_layout.addWidget(main_splitter)
        
    def add_entity(self):
        """Ajoute une nouvelle entité"""
        name, ok = QInputDialog.getText(self, "Nouvelle Entité", "Nom de l'entité:")
        
        if ok and name:
            import random
            entity = {
                "name": name,
                "x": random.randint(50, 400),
                "y": random.randint(50, 300),
                "width": 64,
                "height": 64,
                "color": (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                "type": "GameObject"
            }
            
            self.hierarchy.add_entity(entity)
            self.update_pygame_entities()
            self.console.log(f"Entité '{name}' ajoutée", "success")
    
    def on_entity_selected(self, entity):
        """Quand une entité est sélectionnée"""
        info = "\n".join([f"{key}: {value}" for key, value in entity.items()])
        self.properties_text.setPlainText(info)
        self.console.log(f"Entité '{entity.get('name')}' sélectionnée", "info")
    
    def update_pygame_entities(self):
        """Met à jour les entités dans le widget Pygame"""
        entities = self.hierarchy.get_all_entities()
        self.pygame_widget.set_entities(entities)
        self.pygame_widget.update_display()
    
    def toggle_preview(self):
        """Active/désactive la prévisualisation"""
        if self.pygame_widget.is_running:
            self.pygame_widget.stop_preview()
            self.console.log("Preview arrêtée", "info")
        else:
            self.update_pygame_entities()
            self.pygame_widget.start_preview()
            self.console.log("Preview démarrée", "success")
    
    def play_game(self):
        """Lance le jeu en mode plein écran"""
        if self.game_thread and self.game_thread.isRunning():
            QMessageBox.warning(self, "Attention", "Le jeu est déjà en cours d'exécution!")
            return
        
        entities = self.hierarchy.get_all_entities()
        if not entities:
            QMessageBox.warning(self, "Attention", "Ajoutez au moins une entité avant de lancer le jeu!")
            return
        
        # Arrêter la preview si active
        self.pygame_widget.stop_preview()
        
        # Créer et démarrer le thread du jeu
        self.game_thread = GameThread(entities, 800, 600)
        self.game_thread.log_signal.connect(self.console.log)
        self.game_thread.finished.connect(self.on_game_finished)
        self.game_thread.start()
        
        self.play_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.console.log("Lancement du jeu en mode plein écran...", "success")
    
    def stop_game(self):
        """Arrête le jeu"""
        if self.game_thread:
            self.game_thread.stop()
            self.game_thread.wait()
            self.console.log("Arrêt du jeu demandé", "warning")
    
    def on_game_finished(self):
        """Quand le jeu se termine"""
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.console.log("Jeu terminé", "info")
    
    def new_project(self):
        """Nouveau projet"""
        self.hierarchy.clear_all()
        self.pygame_widget.set_entities([])
        self.pygame_widget.update_display()
        self.console.log("Nouveau projet créé", "success")
    
    def save_project(self):
        """Sauvegarde le projet"""
        import json
        file_path, _ = QFileDialog.getSaveFileName(self, "Sauvegarder", "", "JSON (*.json)")
        if file_path:
            try:
                data = {"entities": self.hierarchy.get_all_entities()}
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                self.console.log(f"Projet sauvegardé: {file_path}", "success")
            except Exception as e:
                self.console.log(f"Erreur: {str(e)}", "error")
    
    def closeEvent(self, event):
        """Quand on ferme l'application"""
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.stop()
            self.game_thread.wait()
        event.accept()


def main():
    app = QApplication(sys.argv)
    editor = GameEngineEditor()
    editor.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()