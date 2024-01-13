import flet as ft


def elevated_button(width, height, text, size):
    button = ft.ElevatedButton(
                width=width,
                height=height,
                content=ft.Row(controls=[
                    ft.Text(
                        value=text,
                        size=size,
                        style=ft.TextThemeStyle.LABEL_MEDIUM)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER),
                )
    return button


def define_title(text, size, font_style, bold=False):
    if bold:
        w = ft.FontWeight.BOLD
    else:
        w = None

    title = ft.Text(
        text_align=ft.TextAlign.RIGHT,
        spans=[
            ft.TextSpan(
                text,
                ft.TextStyle(
                    size=size,
                    weight=w,
                    font_family=font_style,
                )
            )
        ]
    )

    return ft.Row(
        controls=[title],
        alignment=ft.MainAxisAlignment.CENTER
    )
