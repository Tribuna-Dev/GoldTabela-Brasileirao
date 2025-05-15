from view.main_windown import MainWindow
from controller.controller_factory import ControllerFactory

controller_factory = ControllerFactory()

main_windon = MainWindow(controller_factory)

main_windon.main_loop()
