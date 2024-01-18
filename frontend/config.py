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


class GeneratePage(Enum):
    BUTTON_WIDTH = 200
    BUTON_HEIGT = 50
    BUTTON_TEXT_SIZE = 18
    TEXT_STYLE = 'Open Sans'

    TEXT_FIELD_WIDTH = 1500
    TEST_FIELD_HEIGHT = 500
    BORDER_RADIUS = 2
