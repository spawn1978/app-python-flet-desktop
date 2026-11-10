# Lyrics Finder

Aplicacion de escritorio desarrollada en Python y Flet para buscar letras de canciones por artista y titulo. Los resultados se consultan en el servicio externo [lyrics.ovh](https://lyrics.ovh/) y se pueden copiar al portapapeles.

## Funcionalidades

- Busca una letra a partir del nombre del artista y de la cancion.
- Valida que ambos campos tengan contenido antes de iniciar la busqueda.
- Muestra un indicador mientras espera la respuesta del servicio.
- Presenta la letra o un mensaje cuando no se encuentra o falla la conexion.
- Permite copiar el resultado al portapapeles.
- Interfaz de escritorio con tema oscuro.

## Requisitos

- Python 3.14 (version usada para probar el proyecto: 3.14.7).
- Flet 1.1.2.
- Requests 2.34.2.
- Conexion a Internet para consultar lyrics.ovh.

## Instalacion

Desde la carpeta del proyecto, crea y activa un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias con las versiones usadas por el proyecto:

```bash
python -m pip install flet==1.1.2 requests==2.34.2
```

En Windows PowerShell, activa el entorno con:

```powershell
.venv\Scripts\Activate.ps1
```

## Ejecucion

Con el entorno virtual activado, ejecuta:

```bash
python app.py
```

Tambien puedes invocar directamente el interprete del entorno:

```bash
.venv/bin/python app.py
```

En el primer inicio, Flet puede descargar o preparar el runtime de escritorio. La ventana permanece abierta mientras la aplicacion esta en uso; detenla desde la ventana o con `Ctrl+C` en la terminal.

## Uso

1. Escribe el nombre del artista en el campo **Artista**.
2. Escribe el titulo de la cancion en **Cancion**.
3. Pulsa **Buscar letra** y espera la respuesta.
4. Si se encuentra una letra, usa **Copiar letra** para copiarla al portapapeles.

La aplicacion muestra un mensaje si faltan datos, si el servicio no encuentra la cancion o si ocurre un problema de conexion.

## Como funciona

`app.py` crea la interfaz con Flet. La funcion `fetch_lyrics()` hace una solicitud GET al endpoint:

```text
https://api.lyrics.ovh/v1/{artista}/{titulo}
```

La solicitud de red se ejecuta en un hilo de trabajo para no bloquear la interfaz durante la espera. La respuesta se interpreta como JSON y se muestra en el area de resultados. La busqueda requiere que el servicio externo este disponible y que el equipo tenga acceso a Internet.

## Funciones y flujo interno

### `fetch_lyrics(artist, title)`

Esta funcion asincrona se encarga de consultar el servicio de letras:

1. Construye la URL con el artista y el titulo recibidos.
2. Ejecuta `requests.get()` en un hilo mediante `asyncio.to_thread()`. Asi la solicitud HTTP no bloquea el ciclo de eventos de Flet mientras espera la respuesta.
3. Usa un tiempo maximo de espera de 10 segundos.
4. Si el servidor responde con estado HTTP 200, devuelve el contenido JSON. La interfaz espera que la letra este en la clave `lyrics`.
5. Si recibe otro estado HTTP, devuelve un diccionario con el mensaje de cancion no encontrada. Si ocurre una excepcion durante la solicitud o el procesamiento, devuelve un mensaje de error de conexion.

El resultado tiene una de estas formas:

```python
{"lyrics": "Texto de la letra..."}
{"error": "Mensaje del problema"}
```

### `main(page)`

Es la funcion principal de la interfaz y recibe el objeto `Page` que Flet crea para la ventana de la aplicacion. Configura el titulo, el tema oscuro, el fondo, el espacio interior y el tamano de ventana. Tambien crea y agrega los controles visibles:

- `artist_field` y `title_field`: campos donde se ingresan artista y cancion.
- `search_btn`: inicia la busqueda y se desactiva mientras esta en curso.
- `loading`: indicador circular que se muestra durante la consulta.
- `result_text`: area donde aparecen el resultado y los mensajes de validacion o error.
- `copy_btn`: boton oculto inicialmente; se muestra cuando la respuesta contiene una letra.
- `copy_snack`: notificacion breve que confirma que se solicito la copia.

La funcion tambien conecta cada boton con su callback y agrega los controles a la pagina. La cabecera, los campos, los botones y el area de resultados se organizan con contenedores y filas de Flet.

### `search_click(e)`

Es el callback asincrono del boton **Buscar letra**. Su flujo es:

1. Comprueba que artista y cancion tengan texto despues de quitar espacios en los extremos. Si falta alguno, muestra un mensaje y oculta el boton de copia.
2. Desactiva el boton de busqueda, muestra el indicador de carga y actualiza el texto de estado.
3. Llama a `fetch_lyrics()` con los valores ingresados.
4. Si recibe una clave `error`, muestra ese mensaje en rojo. En caso contrario, muestra el valor de `lyrics` (o el texto alternativo si esa clave no esta presente), configura la accion `CopyToClipboard` del boton y lo hace visible.
5. Al terminar, vuelve a habilitar el boton de busqueda, oculta el indicador y actualiza la pagina.

### `copy_click(e)`

Es el callback del boton **Copiar letra**. Al pulsarlo, abre la notificacion `copy_snack`, cambia el color del texto del resultado y actualiza la pagina. La copia del texto se configura en `search_click` con `ft.CopyToClipboard(result_text.value)`, para que Flet la ejecute como accion del boton cuando el usuario lo pulsa.

### Inicio de la aplicacion

La ultima linea, `ft.run(main)`, inicia el runtime de Flet. Cuando se crea una ventana/sesion, Flet invoca `main(page)` y la funcion construye la interfaz para esa pagina.

## Estructura

```text
app-flet/
|-- app.py      # Interfaz y logica de busqueda
`-- README.md   # Documentacion del proyecto
```

## Solucion de problemas

- **`No module named 'flet'` o `No module named 'requests'`:** activa `.venv` e instala las dependencias en ese mismo entorno.
- **No se abre la ventana o el primer inicio tarda:** comprueba que Flet pueda descargar y preparar su runtime de escritorio y vuelve a ejecutar `python app.py`.
- **No se encuentra la cancion:** revisa la escritura del artista y del titulo. La disponibilidad de las letras depende del servicio lyrics.ovh.
- **Error de conexion:** verifica el acceso a Internet y que el servicio externo este disponible.

## Autor

Carlos Leguizamon
