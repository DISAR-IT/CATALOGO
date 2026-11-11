# DISAR + Pages CMS — piloto técnico (sin Supabase)

Este piloto se generó a partir del HTML de Catálogo DISAR compartido en la conversación.
Incluye el diseño público original, los **108 productos** iniciales convertidos a archivos
JSON independientes y un archivo `.pages.yml` para editarlos visualmente en Pages CMS.
**No está desplegado ni vinculado a ningún repositorio.** La conexión y la prueba real
del panel se completan en GitHub/Pages CMS.

## Cómo configurarlo la primera vez

1. Crea un repositorio GitHub (idealmente privado) y coloca el contenido de este ZIP en
   la **raíz** del repositorio: `index.html`, `.pages.yml`, `content/`, `scripts/`, etc.
   Usa la rama `main` o adapta el flujo de despliegue si usas otra.
2. **Muy importante:** añade al repositorio la carpeta `images/` con las fotografías
   originales. El HTML recibido solo contenía referencias como `images/30910.png`.
   Estas fotografías no venían en la carga y por tanto NO están dentro del ZIP.
3. Entra a https://app.pagescms.org/ e inicia sesión con GitHub.
4. Instala la aplicación de GitHub de Pages CMS, otorgando acceso únicamente al
   repositorio del catálogo si no necesita acceso a otros repositorios.
5. Abre ese repositorio y la rama `main`. Pages CMS leerá `.pages.yml` y mostrará
   **Productos del catálogo DISAR**. Abre un producto para comprobar que puede
   editarse visualmente y subir fotografías.
6. Da acceso a la encargada solo al repositorio necesario. Consulta los métodos de
   colaboradores/invitaciones disponibles en Pages CMS y prueba con su cuenta.

## Dónde publicar el sitio público

**Opción A: Cloudflare Pages (recomendada si quieres independizar el hosting del CMS)**

- Conecta el repositorio GitHub al proyecto de Cloudflare Pages.
- Configura el comando de compilación: `python3 scripts/build_site.py`.
- Directorio de salida: `dist`.
- Cada guardado en Pages CMS crea un cambio en GitHub; la integración automática
  vuelve a ejecutar la compilación y publica el catálogo actualizado.

**Opción B: GitHub Pages (sin plataforma adicional)**

- En Settings > Pages, elige la fuente `GitHub Actions`.
- Este ZIP incluye `.github/workflows/publicar.yml` para generar `dist/` y publicarlo
  automáticamente en cada commit de `main`.
- El flujo puede tardar un poco en completar el nuevo despliegue.

**IMPORTANTE**: Si usas Cloudflare Pages, puedes mantener el workflow de GitHub Pages
sin habilitar GitHub Pages, pero recomendamos quitarlo si solo utilizarás Cloudflare.

## Qué edita la encargada

En Pages CMS > Productos del catálogo DISAR:

- Código del producto, nombre, marca y categoría.
- Precio opcional (USD).
- Fotografía JPG/PNG/WebP subida desde su computadora, o URL externa.
- Descripción y palabras clave.
- Interruptor Mostrar en el catálogo (oculta sin borrar).
- Puede crear o eliminar fichas. El nombre del archivo no necesita editarse.

**Los artículos existentes se diferencian mediante el nombre de su archivo**.
En el HTML original hay 108 registros, pero hay códigos que se repiten. No uses
el código comercial como identificador único del archivo ni sobrescribas por código.

## Migración y datos

- `content/productos/*.json`: un producto por archivo, 108 de origen.
- `.pages.yml`: esquema visual de Pages CMS y gestión de imágenes.
- `scripts/build_site.py`: reúne los productos visibles en `dist/data/productos.json`.
- `index.html`: interfaz pública de lectura; carga `data/productos.json`.
- `images/`: fotografías (se deben copiar aparte desde el proyecto original).
- `.github/workflows/publicar.yml`: despliegue automático para GitHub Pages.

La base de datos de productos ya NO se toma de `localStorage` en la página pública.
El botón Administrar anterior se oculta porque no publicaba cambios para los visitantes.

## Cómo comprobar el piloto antes de publicar

En un equipo con Python 3:

```bash
python scripts/build_site.py
cd dist
python -m http.server 8000
```

Abre http://localhost:8000 y revisa que aparezcan los 108 productos.
Si no aparecen imágenes, comprueba que estén los archivos en `images/`.

El desarrollo está preparado para las 10 categorías originales. Crear departamentos
nuevos (distintos a esas categorías) requeriría ampliar la configuración de navegación,
porque los grupos y las portadas aún se definen en JavaScript en el diseño original.

## Limitaciones del piloto

- La experiencia definitiva en Pages CMS y la publicación automática deben probarse
  con el repositorio real: aquí solo se validó la generación local de los archivos.
- La gestión de portadas de categorías y marcas todavía no está en Pages CMS.
- No se incluyen fotografías originales, salvo el arte embebido en el HTML.
- El panel público de edición antiguo sigue en el código pero permanece oculto.
- Si la encargada necesita editar desde el navegador sin cuenta GitHub, revisa las
  invitaciones soportadas por Pages CMS antes de habilitar usuarios.
