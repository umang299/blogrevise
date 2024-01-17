import flet as ft

from config import OutlineHome
from components import define_title, elevated_button


class BlogOutline(ft.UserControl):
    def build(self):
        self.title_row = define_title(
                            text='BLOG OUTLINE',
                            size=OutlineHome.SIZE.value,
                            font_style=OutlineHome.STYLE.value,
                            bold=False
        )

        self.text_region = ft.Row(controls=[
                    ft.Text(
                        value='Generate or upload a outline for your blog',
                        size=18
                    )
                ],
                height=200,
                alignment=ft.MainAxisAlignment.CENTER
            )

        self.gen_button = elevated_button(
                            width=OutlineHome.BUTTON_WIDTH.value,
                            height=OutlineHome.BUTTON_HEIGHT.value,
                            text='Generate',
                            size=OutlineHome.SIZE.value
                        )

        self.upload_button = elevated_button(
                            width=OutlineHome.BUTTON_WIDTH.value,
                            height=OutlineHome.BUTTON_HEIGHT.value,
                            text='Upload',
                            size=OutlineHome.SIZE.value
                        )

        self.buttons = ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[self.gen_button, self.upload_button],
        )

        return ft.Column(
                    controls=[
                        self.title_row,
                        self.text_region,
                        self.buttons
                    ],
                )