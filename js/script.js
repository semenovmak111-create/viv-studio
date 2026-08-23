/* VIV Studio — интерактив лендинга */
(function () {
  'use strict';

  /* ── Тень у шапки при скролле ── */
  var header = document.getElementById('siteHeader');
  var onScroll = function () {
    header.classList.toggle('is-stuck', window.scrollY > 12);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ── Мобильное меню ── */
  var burger = document.getElementById('burger');
  var mobileNav = document.getElementById('mobileNav');

  burger.addEventListener('click', function () {
    var open = burger.getAttribute('aria-expanded') === 'true';
    burger.setAttribute('aria-expanded', String(!open));
    burger.setAttribute('aria-label', open ? 'Открыть меню' : 'Закрыть меню');
    mobileNav.hidden = open;
  });

  mobileNav.addEventListener('click', function (e) {
    if (e.target.closest('a')) {
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Открыть меню');
      mobileNav.hidden = true;
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !mobileNav.hidden) {
      burger.setAttribute('aria-expanded', 'false');
      mobileNav.hidden = true;
      burger.focus();
    }
  });

  /* ── Табы прайса ── */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));

  function activate(tab) {
    tabs.forEach(function (t) {
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      var isTarget = t === tab;
      t.classList.toggle('is-active', isTarget);
      t.setAttribute('aria-selected', String(isTarget));
      panel.classList.toggle('is-active', isTarget);
      panel.hidden = !isTarget;
    });
    revealAll(tab.getAttribute('aria-controls'));
  }

  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { activate(tab); });
    tab.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      e.preventDefault();
      var next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      next.focus();
      activate(next);
    });
  });

  /* ── Появление блоков при скролле ── */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduced) { document.documentElement.classList.add('has-reveal'); }
  var items = Array.prototype.slice.call(document.querySelectorAll('.reveal'));

  function revealAll(scopeId) {
    var scope = scopeId ? document.getElementById(scopeId) : document;
    Array.prototype.forEach.call(scope.querySelectorAll('.reveal'), function (el) {
      el.classList.add('is-visible');
    });
  }

  if (reduced || !('IntersectionObserver' in window)) {
    revealAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var siblings = Array.prototype.slice.call(el.parentElement.children).indexOf(el);
        el.style.transitionDelay = Math.min(siblings, 5) * 70 + 'ms';
        el.classList.add('is-visible');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });

    /* Страховка: если наблюдатель почему-то не сработал — показываем всё */
    setTimeout(function () {
      items.forEach(function (el) {
        if (el.getBoundingClientRect().top < window.innerHeight * 1.2) el.classList.add('is-visible');
      });
    }, 1200);
    window.addEventListener('hashchange', function () {
      setTimeout(revealAll, 60);
    });
  }

  /* ── Маска телефона ── */
  var phone = document.getElementById('fphone');

  phone.addEventListener('input', function () {
    var d = phone.value.replace(/\D/g, '');
    if (d[0] === '8') d = '7' + d.slice(1);
    if (d[0] !== '7') d = '7' + d;
    d = d.slice(0, 11);

    var out = '+7';
    if (d.length > 1) out += ' (' + d.slice(1, 4);
    if (d.length >= 5) out += ') ' + d.slice(4, 7);
    if (d.length >= 8) out += '-' + d.slice(7, 9);
    if (d.length >= 10) out += '-' + d.slice(9, 11);
    phone.value = out;

    phone.removeAttribute('aria-invalid');
    document.getElementById('phoneError').hidden = true;
  });

  /* ── Отправка формы: открываем чат с мастером с готовым сообщением ── */
  var form = document.getElementById('bookingForm');
  var success = document.getElementById('formSuccess');
  var submitBtn = document.getElementById('submitBtn');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var digits = phone.value.replace(/\D/g, '');
    if (digits.length < 11) {
      phone.setAttribute('aria-invalid', 'true');
      document.getElementById('phoneError').hidden = false;
      phone.focus();
      return;
    }
    if (!document.getElementById('fconsent').checked) {
      document.getElementById('fconsent').focus();
      return;
    }

    var name = document.getElementById('fname').value.trim() || 'Клиент';
    var service = document.getElementById('fservice').value;

    var text =
      'Здравствуйте! Меня зовут ' + name + '. ' +
      'Хочу записаться в VIV Studio: ' + service + '. ' +
      'Мой телефон: ' + phone.value + '. ' +
      'Пишу с сайта, интересует первое посещение со скидкой 50%.';

    submitBtn.disabled = true;
    submitBtn.textContent = 'Открываем чат…';
    success.hidden = false;

    window.open('https://wa.me/79219156255?text=' + encodeURIComponent(text), '_blank', 'noopener');

    setTimeout(function () {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Записаться со скидкой 50%';
    }, 2500);
  });
})();
