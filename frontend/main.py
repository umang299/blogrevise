import os
import shutil
import flet as ft

from components import define_title
from config import OutlineHome, GeneratePage

if __name__ == '__main__':
    def main(page: ft.Page):
        page.title = 'Home'
        location = ft.Text()

        def picker_fn(e: ft.FilePickerResultEvent):
            for file in e.files:
                shutil.copy(file.name, os.path.join('uploads', file.name))
                location.value = f"Saved file at {os.path.join('uploads', file.name)}"
                location.update()

        file_picker = ft.FilePicker(on_result=picker_fn)

        def route_change(route):
            page.views.clear()
            page.views.append(
                ft.View(
                    '/',
                    [
                        ft.Column(
                            controls=[
                                define_title(
                                    text='BLOG OUTLINE',
                                    size=OutlineHome.SIZE.value,
                                    font_style=OutlineHome.STYLE.value, 
                                    bold=False
                                ),

                                ft.Row(controls=[
                                        ft.Text(
                                            value='Generate or upload a outline for your blog',
                                            size=18
                                        )
                                    ],
                                    height=200,
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),

                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton(
                                            width=OutlineHome.BUTTON_WIDTH.value,
                                            height=OutlineHome.BUTTON_HEIGHT.value,
                                            content=ft.Row(controls=[
                                                ft.Text(
                                                    value='Generate',
                                                    size=OutlineHome.SIZE.value,
                                                    style=ft.TextThemeStyle.LABEL_MEDIUM)
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                            on_click=lambda _: page.go(route='/generate')
                                        ),

                                        ft.ElevatedButton(
                                            width=OutlineHome.BUTTON_WIDTH.value,
                                            height=OutlineHome.BUTTON_HEIGHT.value,
                                            content=ft.Row(controls=[
                                                ft.Text(
                                                    value='Upload',
                                                    size=OutlineHome.SIZE.value,
                                                    style=ft.TextThemeStyle.LABEL_MEDIUM)
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                            on_click=lambda _: page.go(route='/upload')
                                        )
                                    ],
                                )
                            ]
                        )
                    ]
                )
            )

            if page.route == '/generate':
                page.views.append(
                    ft.View(
                        route='/generate',
                        controls=[
                            ft.Text(
                                value='Topic',
                                size=GeneratePage.BUTTON_TEXT_SIZE.value,
                                font_family=GeneratePage.TEXT_STYLE.value
                            ),

                            ft.TextField(label='Topic name'),

                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                            width=GeneratePage.BUTTON_WIDTH.value,
                                            height=GeneratePage.BUTON_HEIGT.value,
                                            content=ft.Row(controls=[
                                                ft.Text(
                                                    value='Generate',
                                                    size=GeneratePage.BUTTON_TEXT_SIZE.value,
                                                    style=ft.TextThemeStyle.LABEL_MEDIUM)
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER)
                                        )
                                    ],
                                alignment=ft.MainAxisAlignment.END
                                ),

                            ft.Column(
                                spacing=10,
                                tight=True,
                                scroll=ft.ScrollMode.ALWAYS,
                                controls=[
                                    ft.TextField(
                                            width=GeneratePage.TEXT_FIELD_WIDTH.value,
                                            height=GeneratePage.TEST_FIELD_HEIGHT.value,
                                            multiline=True,
                                            autocorrect=True,
                                            border_radius=GeneratePage.BORDER_RADIUS.value
                                        )
                                    ],
                            )
                        ]

                    )
                )
            if page.route == '/upload':
                page.overlay.append(file_picker)
                page.views.append(
                    ft.View(
                        route='/upload',
                        controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            value='Upload your blog outline',
                                            size=26,
                                            font_family='Open Sans',
                                            text_align=ft.MainAxisAlignment.CENTER
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),

                                ft.Row([
                                    ft.ElevatedButton(
                                        'Upload File',
                                        on_click=lambda _: file_picker.pick_files()
                                        ),
                                    location
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                        ]
                    )
                )
            page.update()

        def view_pop(view):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)


ft.app(target=main)
