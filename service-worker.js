const CACHE_NAME = 'boxx-reg-v14'; // Force update once to stabilize manual update UI and Safari fix
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-v11.png',
  './apple-touch-icon-v11.png'
];

self.addEventListener('install', (event) => {
  self.skipWaiting(); // Temporarily restored to force immediate activation for baseline stability
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim());
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(event.request).then((fetchResponse) => {
          // Fix for Safari: If the response is redirected, rebuild it to 'clean' the flag
          if (fetchResponse.redirected) {
            return new Response(fetchResponse.body, {
              status: fetchResponse.status,
              statusText: fetchResponse.statusText,
              headers: fetchResponse.headers
            });
          }
          return fetchResponse;
        });
      })
  );
});

// Listener for the UI to trigger activation of the new service worker
self.addEventListener('message', (event) => {
  if (event.data === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
