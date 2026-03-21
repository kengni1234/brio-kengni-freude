/* ═══════════════════════════════════════════════════════════════
   k-Ni Store — Service Worker PWA
   Version : 1.0.0
   Stratégie : Cache-First pour assets statiques,
               Network-First pour les pages dynamiques
═══════════════════════════════════════════════════════════════ */

const CACHE_VERSION = 'kni-v1.0.0';

/* Assets statiques à mettre en cache immédiatement (précache) */
const PRECACHE_ASSETS = [
  '/shop',
  '/static/manifest.json',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  /* Polices Google (CDN) */
  'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap',
  /* Font Awesome */
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
];

/* URLs qui ne doivent JAMAIS être mises en cache (API dynamique) */
const NO_CACHE_PATTERNS = [
  /\/shop\/api\//,
  /\/shop\/admin/,
  /\/dashboard/,
  /\/logout/,
  /\/login/,
];

/* ── Installation : précache des assets essentiels ── */
self.addEventListener('install', function(event) {
  console.log('[k-Ni SW] Installation…');
  event.waitUntil(
    caches.open(CACHE_VERSION).then(function(cache) {
      return cache.addAll(PRECACHE_ASSETS).catch(function(err) {
        console.warn('[k-Ni SW] Précache partiel :', err);
      });
    }).then(function() {
      /* Activer immédiatement sans attendre le rechargement */
      return self.skipWaiting();
    })
  );
});

/* ── Activation : nettoyer les anciens caches ── */
self.addEventListener('activate', function(event) {
  console.log('[k-Ni SW] Activation…');
  event.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys
          .filter(function(key) { return key !== CACHE_VERSION; })
          .map(function(key) {
            console.log('[k-Ni SW] Suppression ancien cache :', key);
            return caches.delete(key);
          })
      );
    }).then(function() {
      return self.clients.claim();
    })
  );
});

/* ── Fetch : intercepter les requêtes ── */
self.addEventListener('fetch', function(event) {
  const url = event.request.url;
  const method = event.request.method;

  /* Ignorer les non-GET */
  if (method !== 'GET') return;

  /* Ignorer les API dynamiques */
  for (let i = 0; i < NO_CACHE_PATTERNS.length; i++) {
    if (NO_CACHE_PATTERNS[i].test(url)) return;
  }

  /* Stratégie selon le type de ressource */
  if (isStaticAsset(url)) {
    /* Cache-First pour CSS, JS, images, fonts */
    event.respondWith(cacheFirst(event.request));
  } else {
    /* Network-First pour les pages HTML */
    event.respondWith(networkFirst(event.request));
  }
});

/* ── Helpers ── */
function isStaticAsset(url) {
  return /\.(css|js|woff2?|ttf|otf|eot|png|jpg|jpeg|gif|webp|svg|ico)(\?.*)?$/.test(url) ||
         url.includes('fonts.googleapis.com') ||
         url.includes('fonts.gstatic.com') ||
         url.includes('cdnjs.cloudflare.com');
}

/* Cache-First : renvoie depuis le cache, sinon fetch et met en cache */
function cacheFirst(request) {
  return caches.match(request).then(function(cached) {
    if (cached) return cached;
    return fetch(request).then(function(response) {
      if (!response || response.status !== 200 || response.type === 'opaque') {
        return response;
      }
      const clone = response.clone();
      caches.open(CACHE_VERSION).then(function(cache) {
        cache.put(request, clone);
      });
      return response;
    }).catch(function() {
      /* Ressource indisponible offline : rien */
    });
  });
}

/* Network-First : essaie le réseau, fallback cache */
function networkFirst(request) {
  return fetch(request).then(function(response) {
    if (!response || response.status !== 200) return response;
    const clone = response.clone();
    caches.open(CACHE_VERSION).then(function(cache) {
      cache.put(request, clone);
    });
    return response;
  }).catch(function() {
    /* Hors ligne : servir depuis le cache si disponible */
    return caches.match(request).then(function(cached) {
      if (cached) return cached;
      /* Page offline de fallback */
      return caches.match('/shop');
    });
  });
}

/* ── Notification de mise à jour disponible ── */
self.addEventListener('message', function(event) {
  if (event.data && event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});
