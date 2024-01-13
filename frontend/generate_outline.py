import flet as ft
from components import elevated_button


class OutlineGenerator(ft.UserControl):
    def build(self):
        self.button1 = elevated_button(
                            width=200,
                            height=50,
                            text='Generate',
                            size=18,
                        )

        self.button2 = elevated_button(
                                width=200,
                                height=50,
                                text='Save',
                                size=18,
                            )
        
        generate_button = ft.Row(
            controls=[self.button1],
            alignment=ft.MainAxisAlignment.END
        )

        aux_button = ft.Row(
                controls=[self.button2],
                alignment=ft.MainAxisAlignment.END
        )

        generated_text_area = ft.Column(
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

        return ft.Column(
                    controls=[
                        ft.Text(
                            value='Topic',
                            size=18,
                            font_family='Open Sans'
                        ),
                        ft.TextField(label='Topic name'),
                        generate_button,
                        generated_text_area,
                        aux_button
                    ]
        )