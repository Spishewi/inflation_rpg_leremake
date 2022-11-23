from map_manager import MapManager
from camera_view import CameraView

class Game:
    def __init__(self, window):
        self.window = window

        self.map_manager = MapManager()
        self.map_manager.add_map()

        self.camera_view = CameraView(self.map_manager)
        
    def run(self):
        launched = True
        while launched:
            self.camera_view.draw(self.window)