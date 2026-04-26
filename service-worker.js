const CACHE_NAME = 'boxx-reg-v119'; // v3.8.11 Bold amounts in summary
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './LOGO.png'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    Promise.all([
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME) {
              return caches.delete(cacheName);
            }
          })
        );
      }),
      self.clients.claim()
    ])
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  const isNavigation = event.request.mode === 'navigate';
  const isRoot = url.pathname === '/' || url.pathname.endsWith('/index.html') || url.pathname.endsWith('/');

  if (isNavigation && isRoot) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // If network is successful, update cache and return
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put('./index.html', copy));
          return response;
        })
        .catch(() => {
          // If offline, return from cache
          return caches.match('./index.html');
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
