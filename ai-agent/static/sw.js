// Service Worker — AI Agent PWA
// Cache static assets for instant load on repeat visits

const CACHE = 'ai-agent-v34';

// Network-first cho JS/CSS versioned (có ?v=) để luôn nhận bản mới nhất
// Cache-first chỉ cho font/CDN ít thay đổi
const NETWORK_FIRST_PATTERNS = ['/static/app.js', '/static/style.css'];

self.addEventListener('install', e => {
  self.skipWaiting();
  // Không precache JS/CSS có ?v= — để network-first handler tự cache lần đầu
  const PRECACHE = [
    'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css',
  ];
  e.waitUntil(
    caches.open(CACHE).then(c =>
      Promise.allSettled(PRECACHE.map(url => c.add(url).catch(() => {})))
    )
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const url = e.request.url;

  // Không cache API calls
  if (url.includes('/chat') || url.includes('/pipeline') || url.includes('/computer-use')
      || url.includes('/memory') || url.includes('/models') || url.includes('/health')
      || url.includes('/abort') || url.includes('/checkpoints')) {
    return;
  }

  // Network-first cho JS/CSS (hỗ trợ ?v= versioning)
  if (NETWORK_FIRST_PATTERNS.some(p => url.includes(p))) {
    e.respondWith(
      fetch(e.request).then(res => {
        if (res.ok) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone)).catch(() => {});
        }
        return res;
      }).catch(() => caches.match(e.request))
    );
    return;
  }

  // Cache-first cho CDN fonts/CSS ít thay đổi
  if (url.includes('fonts.googleapis') || url.includes('cdnjs.cloudflare') || url.includes('fonts.gstatic')) {
    e.respondWith(
      caches.match(e.request).then(cached => {
        if (cached) return cached;
        return fetch(e.request).then(res => {
          if (res.ok && res.type !== 'opaque') {
            const clone = res.clone();
            caches.open(CACHE).then(c => c.put(e.request, clone)).catch(() => {});
          }
          return res;
        });
      })
    );
  }
});
