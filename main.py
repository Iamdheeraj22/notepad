from tkinter import *
from app import App
from models.app_config import AppConfig
from services.resource_manager import ResourceManager

if __name__ == '__main__':
    config = AppConfig()
    rm = ResourceManager()
    app = App(config=config, resource_manager=rm)
    app.runApp()
