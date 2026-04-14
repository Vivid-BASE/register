const CACHE_NAME = 'boxx-reg-v12'; // Added in-app update notification support
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-v11.png',
  './apple-touch-icon-v11.png'
];

self.addEventListener('install', (event) => {
  // Removed self.skipWaiting() to allow manual update trigger
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
      .then((response) => response || fetch(event.request))
  );
});

// Listener for the UI to trigger activation of the new service worker
self.addEventListener('message', (event) => {
  if (event.data === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
