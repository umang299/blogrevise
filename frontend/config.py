import flet as ft
from enum import Enum


class Alignment:
    CENTER = ft.MainAxisAlignment.CENTER
    END = ft.MainAxisAlignment.END
    START = ft.MainAxisAlignment.START


class OutlineHome(Enum):
    SIZE = 50
    STYLE = 'Open Sans'
    BUTTON_WIDTH = 340
    BUTTON_HEIGHT = 138
    ALIGNMENT = Alignment.CENTER
