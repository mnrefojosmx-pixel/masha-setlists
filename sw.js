// Guarda la app en el teléfono para que funcione sin internet.
// La página se pide primero a la red (así llegan los cambios) y, si no hay conexión, sale de la copia guardada.
const CACHE = "masha-setlists-202610300327";
const FILES = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png"];

self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});

const save = (req, res) => { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res; };

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const isPage = e.request.mode === "navigate" || e.request.url.endsWith("/index.html");
  if (isPage) {
    e.respondWith(fetch(e.request, {cache: "no-store"}).then(res => save(e.request, res))
      .catch(() => caches.match(e.request).then(hit => hit || caches.match("./index.html"))));
    return;
  }
  e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request).then(res => save(e.request, res))));
});
