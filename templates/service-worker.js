const CACHE_NAME = 'footop-v1';
const OFFLINE_URL = '/offline/';

const PRECACHE_ASSETS = [
  '/',
  '/static/css/bootstrap.min.css',
  '/static/css/style.css',
  '/static/js/bootstrap.bundle.min.js',
  '/static/js/active.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS);
    }).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  if (!event.request.url.startsWith('http')) return;

  const url = new URL(event.request.url);

  // 1. Cache-First pour les assets statiques et médias
  if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/media/')) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse; // Retourne immédiatement depuis le cache (très rapide)
        }
        // Sinon, va sur le réseau et met en cache
        return fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.ok) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseClone));
          }
          return networkResponse;
        });
      })
    );
    return; // Stop ici pour les assets
  }

  // 2. Network-First pour le HTML et l'API (assure des données à jour)
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Mettre en cache seulement les pages HTML complètes
        if (response.ok && event.request.mode === 'navigate') {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseClone));
        }
        return response;
      })
      .catch(() => {
        // En cas de panne réseau, renvoyer la version en cache ou la page hors ligne
        return caches.match(event.request).then((cached) => {
          if (cached) return cached;
          if (event.request.mode === 'navigate') {
            return caches.match(OFFLINE_URL);
          }
        });
      })
  );
});
