/**
 * JobSpark – app.js
 * =================
 * Client-side enhancements for the Django-powered portal.
 *
 * Responsibilities:
 *  - Dark mode toggle (persisted in localStorage)
 *  - Bootstrap toast notifications (triggered by Django messages)
 *  - Password show/hide toggle
 *  - Register page role radio sync
 *  - Save/bookmark AJAX calls
 *  - Dynamic job search (debounced form submit on keyup)
 */

'use strict';

// ── Dark Mode ─────────────────────────────────────────────────
function getDarkMode() { return localStorage.getItem('jp_dark_mode') === 'true'; }

function applyDarkMode() {
  document.body.classList.toggle('dark-mode', getDarkMode());
}

function toggleDarkMode() {
  localStorage.setItem('jp_dark_mode', String(!getDarkMode()));
  applyDarkMode();
  updateDarkBtn();
}

function updateDarkBtn() {
  const btn = document.getElementById('darkToggleBtn');
  if (!btn) return;
  btn.innerHTML = getDarkMode()
    ? '<i class="bi bi-sun-fill"></i>'
    : '<i class="bi bi-moon-fill"></i>';
}

// ── Toast Helper ──────────────────────────────────────────────
function showToast(msg, type) {
  type = type || 'success';
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const id    = 'toast_' + Date.now();
  const icon  = type === 'success'
    ? 'bi-check-circle-fill text-success'
    : 'bi-x-circle-fill text-danger';
  container.insertAdjacentHTML('beforeend',
    '<div id="' + id + '" class="toast align-items-center border-0 shadow-sm" role="alert">' +
      '<div class="d-flex">' +
        '<div class="toast-body d-flex align-items-center gap-2">' +
          '<i class="bi ' + icon + '"></i> ' + msg +
        '</div>' +
        '<button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>' +
      '</div>' +
    '</div>'
  );
  const el = new bootstrap.Toast(document.getElementById(id), { delay: 3500 });
  el.show();
  document.getElementById(id).addEventListener('hidden.bs.toast', function () {
    var t = document.getElementById(id); if (t) t.remove();
  });
}

// ── Show Django messages as toasts ────────────────────────────
function showDjangoMessages() {
  var msgs = document.querySelectorAll('.django-message');
  msgs.forEach(function (el) {
    var type = el.dataset.type === 'danger' ? 'error' : 'success';
    showToast(el.dataset.message, type);
    el.remove();
  });
}

// ── Password show/hide ────────────────────────────────────────
function togglePass(inputId, btn) {
  var inp  = document.getElementById(inputId);
  var show = inp.type === 'password';
  inp.type = show ? 'text' : 'password';
  btn.innerHTML = show
    ? '<i class="bi bi-eye-slash"></i>'
    : '<i class="bi bi-eye"></i>';
}

// ── Register: sync radio → hidden input ───────────────────────
function initRoleRadios() {
  var radios = document.querySelectorAll('input[name="regRoleOpt"]');
  var hidden = document.getElementById('id_role');  // Django form field id
  if (!radios.length || !hidden) return;
  radios.forEach(function (r) {
    r.addEventListener('change', function () { hidden.value = r.value; });
  });
}

// ── Save / Bookmark (AJAX) ────────────────────────────────────
function initSaveButtons() {
  document.querySelectorAll('.save-job-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var url    = btn.dataset.url;
      var csrfEl = document.querySelector('[name=csrfmiddlewaretoken]');
      var csrf   = csrfEl ? csrfEl.value : '';

      fetch(url, {
        method:  'POST',
        headers: {
          'X-CSRFToken':     csrf,
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var icon = btn.querySelector('i');
        if (data.saved) {
          btn.classList.add('saved');
          if (icon) { icon.classList.remove('bi-bookmark'); icon.classList.add('bi-bookmark-fill'); }
        } else {
          btn.classList.remove('saved');
          if (icon) { icon.classList.remove('bi-bookmark-fill'); icon.classList.add('bi-bookmark'); }
        }
        showToast(data.message, data.saved ? 'success' : 'error');
      })
      .catch(function () { showToast('Could not save. Please try again.', 'error'); });
    });
  });
}

// ── Debounced Search: auto-submit search form on keystroke ────
function initDynamicSearch() {
  var form  = document.getElementById('searchForm');
  var inputs = form ? form.querySelectorAll('input, select') : [];
  var timer;
  inputs.forEach(function (el) {
    el.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () { form.submit(); }, 500);
    });
    el.addEventListener('change', function () { form.submit(); });
  });
}

// ── Quick search tag click ────────────────────────────────────
function quickSearch(term) {
  var el = document.getElementById('id_q');
  if (el) {
    el.value = term;
    var form = document.getElementById('searchForm');
    if (form) form.submit();
  }
}

// ── DOMContentLoaded Init ─────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  applyDarkMode();
  updateDarkBtn();
  showDjangoMessages();
  initRoleRadios();
  initSaveButtons();
  initDynamicSearch();

  var darkBtn = document.getElementById('darkToggleBtn');
  if (darkBtn) darkBtn.addEventListener('click', toggleDarkMode);
});
