import flet as ft

from components import define_title
from config import OutlineHome

if __name__ == '__main__':
    def main(page: ft.Page):
        page.title = 'Home'

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
                                size=18,
                                font_family='Open Sans'
                            ),

                            ft.TextField(label='Topic name'),

                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                            width=200,
                                            height=50,
                                            content=ft.Row(controls=[
                                                ft.Text(
                                                    value='Generate',
                                                    size=18,
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
                                            width=1500,
                                            height=500,
                                            multiline=True,
                                            autocorrect=True,
                                            border_radius=2
                                        )
                                    ],
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


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
