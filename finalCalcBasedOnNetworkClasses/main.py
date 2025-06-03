# main.py

from model import Network
from view import NetworkView
from controller import NetworkController

if __name__ == "__main__":
    view = NetworkView()
    controller = NetworkController(Network, view)

    controller.run()
