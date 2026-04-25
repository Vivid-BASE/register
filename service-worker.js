const CACHE_NAME = 'boxx-reg-v88'; // v3.4.3 EU Amazon support
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './LOGO.png'
];

self.addEventListener('install', (event) => {
  self.skipWaiting(); // Force active immediately after download
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME) {
              return caches.delete(cacheName);
            }
          })
        );
      }),
      // Take control of all pages immediately
      self.clients.claim()
    ])
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Normalize navigation requests (Home Screen start-up)
  const isNavigation = event.request.mode === 'navigate';
  const isRoot = url.pathname === '/' || url.pathname.endsWith('/index.html');

  if (isNavigation && isRoot) {
    event.respondWith(
      caches.match('./index.html').then((response) => {
        if (!response) return fetch(event.request);
        
        // DEEP CLEANING: Safari will block responses with ANY redirect metadata.
        // We decompose the response into a raw Blob and rebuild it from scratch.
        return response.blob().then((blob) => {
          return new Response(blob, {
            status: response.status,
            statusText: response.statusText,
            headers: response.headers
          });
        });
      })
    );
    return;
  }

  // Standard fetch for other assets
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(event.request).then((fetchResponse) => {
          // General redirection fix for Safari's strict policy
          if (fetchResponse.redirected) {
            return fetchResponse.blob().then((blob) => {
              return new Response(blob, {
                status: fetchResponse.status,
                statusText: fetchResponse.statusText,
                headers: fetchResponse.headers
              });
            });
          }
          return fetchResponse;
        });
      })
  );
});

self.addEventListener('message', (event) => {
  if (event.data === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
