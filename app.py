# Desarrollado por: Carlos Leguizamon
# Librerias necesarias flet 1.1.2, requests 2.34.2

import flet as ft
import requests, asyncio

async def fetch_lyrics(artist, title):
    try:
        url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
        response = await asyncio.to_thread(requests.get, url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": "Cancion no encontrada."}
    except:
          return {"error": "Error de conexion. Verificicar tu internet."}
    
async def main(page: ft.Page):
    page.title = "Lyrics Finder"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.background_color = ft.Colors.GREY_900
    page.window_width = 1000
    page.window_height = 750

    artist_field = ft.TextField(
        label="Artista",
        hint_text="ej. Adele",
        border_color=ft.Colors.PURPLE_400,
        focused_border_color=ft.Colors.PURPLE_300,
        cursor_color=ft.Colors.PURPLE_300,
        text_size=16,
        filled=True,
        bgcolor=ft.Colors.GREY_800,
        border_radius=12,
    )
    title_field = ft.TextField(
        label="Cancion",
        hint_text="ej. Hello",
        border_color=ft.Colors.PURPLE_400,
        focused_border_color=ft.Colors.PURPLE_300,
        cursor_color=ft.Colors.PURPLE_300,
        text_size=16,
        filled=True,
        bgcolor=ft.Colors.GREY_800,
        border_radius=12,
    )
    search_btn = ft.Button(
        content="Buscar letra",
        icon=ft.Icons.SEARCH,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.PURPLE_400,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        height=50,
        width=200,
    )
    loading = ft.ProgressRing(
        width=25,
        height=25,
        stroke_width=3,
        color=ft.Colors.PURPLE_400,
        visible=False,
    )
    result_text = ft.Text(value="", selectable=True, size=15, color=ft.Colors.WHITE)
    copy_btn = ft.ElevatedButton(
        text="Copiar letra",
        icon=ft.icons.COPY,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.PURPLE_600,
            padding=15,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        visible=False
    ) 
    async def search_click(e):
        if not artist_field.value or not artist_field.value.strip() or not title_field.value or not title_field.value.strip():
            result_text.value = "Por favor ingrese el artista y la cancion."
            result_text.color = ft.Colors.RED_300
            page.update()
            return

        search_btn.disabled = loading.visible = True
        result_text.value = "Buscando letra..."
        result_text.color = ft.Colors.PURPLE_300
        page.update()

        data = await fetch_lyrics(artist_field.value.strip(), title_field.value.strip())

        if "error" in data:
            result_text.value = data["error"]
            result_text.color = ft.Colors.RED_300
        else:
            result_text.value = data.get("lyrics", "Letra no encontrada.")
            result_text.color = ft.Colors.WHITE

        search_btn.disabled = loading.visible = False
        page.update()

    search_btn.on_click = search_click

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.MUSIC_NOTE, size=60, color=ft.Colors.PURPLE_300),
                    ft.Text("Lyrics Finder", size=36, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Encuentra las letras de tus canciones favoritas",
                        size=14,
                        color=ft.Colors.GREY_400,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=30,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[ft.Colors.PURPLE_900, ft.Colors.DEEP_PURPLE_900, ft.Colors.INDIGO_900],
            ),
            border_radius=20,
            width=750,
        ),
        ft.Container(content=artist_field, width=750),
        ft.Container(content=title_field, width=750),
        ft.Row([search_btn, loading], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
        result_text,
    )

ft.run(main)
