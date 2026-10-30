# Arma la app instalable (app/) a partir de generador-setlists.html.
# Uso: python3 build-app.py  → luego copiar app/* al repo masha-setlists y hacer push a main.
import datetime, os, re

here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "generador-setlists.html")).read()
now = datetime.datetime.now(datetime.timezone.utc)
version = now.strftime("%Y%m%d%H%M")
label = now.strftime("%d/%m/%Y")

# sello de versión visible en el pie de página
src = src.replace('<p class="foot">', f'<p class="foot">Versión {label}. ', 1)

head = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#161514">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Setlist Gen">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-192.png">
<style>:root{padding-block:env(safe-area-inset-top,0px) env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>
</head>
<body>
"""
tail = """
<script>
// Con internet carga siempre la última versión; sin internet usa la guardada.
if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
  let reloaded = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => { if (!reloaded) { reloaded = true; location.reload(); } });
  navigator.serviceWorker.register("sw.js").then(r => r.update()).catch(() => {});
}
</script>
</body>
</html>
"""
os.makedirs(os.path.join(here, "app"), exist_ok=True)
open(os.path.join(here, "app", "index.html"), "w").write(head + src + tail)

sw = open(os.path.join(here, "app", "sw.js")).read()
sw = re.sub(r'const CACHE = "masha-setlists-[^"]*";', f'const CACHE = "masha-setlists-{version}";', sw)
open(os.path.join(here, "app", "sw.js"), "w").write(sw)
print("app/ lista, versión", version)
