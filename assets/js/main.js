/* ==========================================================================
   BRANDON & CO. — homepage behaviour
   Vanilla, no dependencies. Everything degrades to a working page if JS fails.
   ========================================================================== */
(function () {
  'use strict';

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // marks that scripting is live — reveal start-states are scoped to .js so the
  // page stays fully readable if this file never loads
  document.documentElement.classList.add('js');
  var money = function (n) { return '$' + n.toLocaleString('en-US'); };

  /* ---------------------------------------------------------------- store */
  var KEY = 'bandco.v1';
  var store = { cart: [], wish: [] };
  try {
    var saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (saved && Array.isArray(saved.cart) && Array.isArray(saved.wish)) store = saved;
  } catch (e) { /* private mode — stay in memory */ }

  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {}
  }

  /* --------------------------------------------------- announcement rail */
  (function announce() {
    var rail = $('[data-announce]');
    if (!rail) return;
    var msgs = $$('.announce__msg', rail);
    if (msgs.length < 2 || reduced) return;
    var i = 0;
    setInterval(function () {
      msgs[i].classList.remove('is-on');
      i = (i + 1) % msgs.length;
      msgs[i].classList.add('is-on');
    }, 4600);
  }());

  /* ------------------------------------------------------------- marquee */
  (function marquee() {
    var track = $('[data-marquee]');
    if (!track || reduced) return;
    track.innerHTML += track.innerHTML; // duplicate for a seamless -50% loop
  }());

  /* -------------------------------------------------------- sticky header */
  var header = $('[data-header]');
  var dock = $('[data-dock]');
  var totop = $('[data-totop]');

  function onScroll() {
    var y = window.pageYOffset;
    if (header) header.classList.toggle('is-stuck', y > 40);
    if (dock) dock.classList.toggle('is-on', y > window.innerHeight * 0.7);
    if (totop) totop.classList.toggle('is-on', y > window.innerHeight * 1.2);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (totop) {
    totop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
    });
  }

  /* ------------------------------------------------------------ mega menu */
  $$('[data-mega]').forEach(function (item) {
    var link = $('.nav__link', item);
    var close;
    function open(state) {
      clearTimeout(close);
      item.classList.toggle('is-open', state);
      if (link) link.setAttribute('aria-expanded', String(state));
    }
    item.addEventListener('mouseenter', function () { open(true); });
    item.addEventListener('mouseleave', function () { close = setTimeout(function () { open(false); }, 120); });
    item.addEventListener('focusin', function () { open(true); });
    item.addEventListener('focusout', function (e) {
      if (!item.contains(e.relatedTarget)) open(false);
    });
    item.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && item.classList.contains('is-open')) { open(false); link.focus(); }
    });
  });

  /* ------------------------------------------------------------- overlays */
  var scrim = $('[data-scrim]');
  var openPanel = null;
  var lastFocus = null;

  var FOCUSABLE = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';

  function show(name) {
    var panel = $('[data-panel="' + name + '"]');
    if (!panel) return;
    if (openPanel && openPanel !== panel) hide(true);
    lastFocus = document.activeElement;
    panel.classList.add('is-on');
    if (scrim) scrim.classList.add('is-on');
    document.body.classList.add('is-locked');
    openPanel = panel;
    var first = $(FOCUSABLE, panel);
    if (first) setTimeout(function () { first.focus(); }, 60);
  }

  function hide(silent) {
    if (!openPanel) return;
    openPanel.classList.remove('is-on');
    openPanel = null;
    if (scrim) scrim.classList.remove('is-on');
    document.body.classList.remove('is-locked');
    if (!silent && lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener('click', function (e) {
    var opener = e.target.closest('[data-open]');
    if (opener) { e.preventDefault(); show(opener.getAttribute('data-open')); return; }
    if (e.target.closest('[data-close]')) { hide(); return; }
    if (scrim && e.target === scrim) hide();
    // clicking the backdrop of the centred quick view closes it
    if (openPanel && openPanel.id === 'qv' && e.target === openPanel) hide();
  });

  document.addEventListener('keydown', function (e) {
    if (!openPanel) return;
    if (e.key === 'Escape') { hide(); return; }
    if (e.key !== 'Tab') return;
    var items = $$(FOCUSABLE, openPanel).filter(function (el) { return el.offsetParent !== null; });
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  // in-page links inside overlays should close them on the way out
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (a && openPanel && openPanel.contains(a)) hide(true);
  });

  /* ---------------------------------------------------------- product data */
  function readCard(card) {
    return {
      id: card.getAttribute('data-id'),
      cat: card.getAttribute('data-cat'),
      name: card.getAttribute('data-name'),
      kind: card.getAttribute('data-kind'),
      price: parseInt(card.getAttribute('data-price'), 10) || 0,
      img: card.getAttribute('data-img'),
      spec: card.getAttribute('data-spec'),
      desc: card.getAttribute('data-desc'),
      specs: ['s1', 's2', 's3', 's4'].map(function (k) {
        return card.getAttribute('data-' + k);
      }).filter(Boolean).map(function (s) { return s.split('|'); })
    };
  }

  var cards = $$('.card[data-id]');
  var catalog = cards.map(readCard);
  function find(id) {
    for (var i = 0; i < catalog.length; i++) if (catalog[i].id === id) return catalog[i];
    return null;
  }

  /* ---------------------------------------------------------------- cart */
  var cartBody = $('[data-cart-body]');
  var cartTotal = $('[data-cart-total]');

  function renderList(body, list, kind) {
    if (!body) return;
    if (!list.length) {
      body.innerHTML = '<div class="empty"><svg><use href="#i-' + (kind === 'cart' ? 'bag' : 'heart') +
        '"/></svg><p>' + (kind === 'cart' ? 'Your bag is empty.' : 'Nothing saved yet.') + '</p></div>';
      return;
    }
    body.innerHTML = list.map(function (item) {
      var price = item.price ? money(item.price) : 'By consultation';
      return '<div class="mini">' +
        '<img src="' + item.img + '" alt="" width="84" height="84">' +
        '<div class="mini__b"><h3>' + item.name + '</h3>' +
        '<span>' + item.spec + '</span><b>' + price + '</b></div>' +
        '<button class="mini__rm" type="button" data-rm="' + kind + '" data-rm-id="' + item.id + '">Remove</button>' +
        '</div>';
    }).join('');
  }

  function sync() {
    var cCount = store.cart.length;
    var wCount = store.wish.length;

    $$('[data-cart-count]').forEach(function (el) {
      el.textContent = cCount;
      el.classList.toggle('is-on', cCount > 0);
    });
    $$('[data-wish-count]').forEach(function (el) {
      el.textContent = wCount;
      el.classList.toggle('is-on', wCount > 0);
    });
    var cl = $('[data-cart-label]'); if (cl) cl.textContent = '(' + cCount + ')';
    var wl = $('[data-wish-label]'); if (wl) wl.textContent = '(' + wCount + ')';
    var dc = $('[data-dock-count]'); if (dc) dc.textContent = '(' + cCount + ')';

    var sum = store.cart.reduce(function (t, i) { return t + i.price; }, 0);
    if (cartTotal) cartTotal.textContent = money(sum);

    renderList(cartBody, store.cart, 'cart');
    renderList($('[data-wish-body]'), store.wish, 'wish');

    $$('[data-wish]').forEach(function (btn) {
      var card = btn.closest('.card');
      if (!card) return;
      var on = store.wish.some(function (i) { return i.id === card.getAttribute('data-id'); });
      btn.classList.toggle('is-on', on);
      btn.setAttribute('aria-pressed', String(on));
    });

    var dt = $('[data-dock-title]'), ds = $('[data-dock-sub]');
    if (dt && ds) {
      if (cCount) {
        dt.textContent = cCount + (cCount === 1 ? ' piece reserved' : ' pieces reserved');
        ds.textContent = 'Subtotal ' + money(sum);
      } else {
        dt.textContent = 'Shop the Collection';
        ds.textContent = 'Free insured shipping';
      }
    }
    persist();
  }

  function addToCart(id) {
    var item = find(id);
    if (!item) return;
    if (store.cart.some(function (i) { return i.id === id; })) { show('cart'); return; }
    store.cart.push(item);
    sync();
    show('cart');
  }

  function toggleWish(id) {
    var at = -1;
    store.wish.forEach(function (i, n) { if (i.id === id) at = n; });
    if (at > -1) store.wish.splice(at, 1);
    else {
      var item = find(id);
      if (item) store.wish.push(item);
    }
    sync();
  }

  document.addEventListener('click', function (e) {
    var wishBtn = e.target.closest('[data-wish]');
    if (wishBtn) {
      e.preventDefault();
      var card = wishBtn.closest('.card');
      if (card) toggleWish(card.getAttribute('data-id'));
      return;
    }
    var rm = e.target.closest('[data-rm]');
    if (rm) {
      var listName = rm.getAttribute('data-rm') === 'cart' ? 'cart' : 'wish';
      var id = rm.getAttribute('data-rm-id');
      store[listName] = store[listName].filter(function (i) { return i.id !== id; });
      sync();
    }
  });

  /* ----------------------------------------------------------- quick view */
  var qv = $('#qv');

  function fillQuick(item) {
    if (!qv) return;
    $('[data-qv-img]', qv).src = item.img;
    $('[data-qv-img]', qv).alt = item.name;
    $('[data-qv-kind]', qv).textContent = item.kind;
    $('[data-qv-name]', qv).textContent = item.name;
    $('[data-qv-price]', qv).textContent = item.price ? money(item.price) : 'From $3,500 · by consultation';
    $('[data-qv-desc]', qv).textContent = item.desc || '';
    $('[data-qv-specs]', qv).innerHTML = item.specs.map(function (pair) {
      return '<div><dt>' + pair[0] + '</dt><dd>' + pair[1] + '</dd></div>';
    }).join('');
    $('[data-qv-add]', qv).setAttribute('data-qv-add', item.id);
    $('[data-qv-add]', qv).textContent = item.price ? 'Add to Bag' : 'Request a Consultation';
  }

  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-quick]');
    if (!q) return;
    e.preventDefault();
    var card = q.closest('.card');
    var item = card && find(card.getAttribute('data-id'));
    if (!item) return;
    fillQuick(item);
    show('qv');
  });

  if (qv) {
    $('[data-qv-add]', qv).addEventListener('click', function () {
      var id = this.getAttribute('data-qv-add');
      var item = find(id);
      if (!item) return;
      if (!item.price) { hide(true); location.hash = '#appointment'; return; }
      addToCart(id);
    });
  }

  /* --------------------------------------------------------- grid filters */
  var filters = $$('[data-filter]');
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var want = btn.getAttribute('data-filter');
      filters.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('is-on', on);
        b.setAttribute('aria-selected', String(on));
      });
      cards.forEach(function (card) {
        var match = want === 'all' || card.getAttribute('data-cat') === want;
        card.hidden = !match;
        if (match) {
          card.classList.remove('is-in');
          // let the reveal replay so filtered results fade in rather than snap
          requestAnimationFrame(function () { card.classList.add('is-in'); });
        }
      });
    });
  });

  /* ---------------------------------------------------------------- search */
  var sInput = $('[data-search-input]');
  var sResults = $('[data-search-results]');
  var sList = $('[data-search-list]');

  if (sInput && sList) {
    sInput.addEventListener('input', function () {
      var q = sInput.value.trim().toLowerCase();
      if (q.length < 2) { sResults.hidden = true; sList.innerHTML = ''; return; }
      var hits = catalog.filter(function (p) {
        return (p.name + ' ' + p.kind + ' ' + p.spec + ' ' + p.cat).toLowerCase().indexOf(q) > -1;
      });
      sResults.hidden = false;
      sList.innerHTML = hits.length
        ? hits.map(function (p) {
            return '<li><a href="#featured" data-close>' + p.name + ' — ' +
              (p.price ? money(p.price) : 'by consultation') + '</a></li>';
          }).join('')
        : '<li><a href="#appointment" data-close>No match — ask a specialist instead</a></li>';
    });
    $('[data-search-form]').addEventListener('submit', function (e) { e.preventDefault(); });
  }

  /* -------------------------------------------------------------- slider */
  (function slider() {
    var root = $('[data-slider]');
    if (!root) return;
    var track = $('[data-track]', root);
    var slides = $$('.says__slide', track);
    var prev = $('[data-prev]', root);
    var next = $('[data-next]', root);
    var index = 0;

    function perView() { return window.innerWidth >= 900 ? 2 : 1; }
    function maxIndex() { return Math.max(0, slides.length - perView()); }

    function go(i) {
      index = Math.min(Math.max(i, 0), maxIndex());
      track.style.transform = 'translateX(-' + (index * (100 / perView())) + '%)';
      prev.disabled = index === 0;
      next.disabled = index === maxIndex();
      slides.forEach(function (s, n) {
        var visible = n >= index && n < index + perView();
        s.setAttribute('aria-hidden', String(!visible));
      });
    }

    prev.addEventListener('click', function () { go(index - 1); });
    next.addEventListener('click', function () { go(index + 1); });
    window.addEventListener('resize', function () { go(index); });

    // touch swipe
    var x0 = null;
    track.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) go(index + (dx < 0 ? 1 : -1));
      x0 = null;
    });

    go(0);
  }());

  /* ---------------------------------------------------------------- forms */
  $$('[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = $('[data-note]', form);
      var invalid = $$('input[required],select[required]', form).filter(function (f) {
        return !f.value.trim() || (f.type === 'email' && f.value.indexOf('@') < 1);
      });
      if (invalid.length) {
        if (note) note.textContent = 'Please complete the highlighted fields.';
        invalid[0].focus();
        return;
      }
      if (note) note.textContent = 'Thank you — a specialist will reply within one business day.';
      form.reset();
    });
  });

  /* -------------------------------------------------------- scroll reveal */
  (function reveal() {
    var targets = $$('.rv, .rv-img, .rv-line');
    if (!targets.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
    targets.forEach(function (el) { io.observe(el); });
  }());

  sync();
}());
