/* ============================================================
   main.js — ClubHub
   ============================================================ */

// Apply theme before paint to avoid flash (also in <head> inline script)
(function () {
  var t = localStorage.getItem('clubhub-theme') || 'light';
  document.documentElement.setAttribute('data-theme', t);
})();

document.addEventListener('DOMContentLoaded', function () {

  // ── Theme toggle ───────────────────────────────────────
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon   = document.getElementById('themeIcon');

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('clubhub-theme', theme);
    if (themeIcon) {
      themeIcon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    }
  }

  // Sync icon with current stored theme on load
  var currentTheme = localStorage.getItem('clubhub-theme') || 'light';
  if (themeIcon) {
    themeIcon.className = currentTheme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(next);
    });
  }


  // ── Sidebar mobile toggle ──────────────────────────────
  const sidebar = document.getElementById('sidebar');
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebarClose = document.getElementById('sidebarClose');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  function openSidebar() {
    sidebar && sidebar.classList.add('is-open');
    sidebarOverlay && sidebarOverlay.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar && sidebar.classList.remove('is-open');
    sidebarOverlay && sidebarOverlay.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  sidebarToggle && sidebarToggle.addEventListener('click', openSidebar);
  sidebarClose && sidebarClose.addEventListener('click', closeSidebar);
  sidebarOverlay && sidebarOverlay.addEventListener('click', closeSidebar);

  // ── Auto-dismiss alerts ──────────────────────────────
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity .4s, transform .4s';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });

  // ── Notification dot check ─────────────────────────
  const notifDot = document.getElementById('notif-dot');
  if (notifDot) {
    fetch('/notifications/count/')
      .then(r => r.json())
      .then(data => {
        if (data.count > 0) {
          notifDot.style.display = 'block';
        }
      })
      .catch(() => {});
  }

  // ── File upload preview ────────────────────────────
  document.querySelectorAll('.file-upload-area').forEach(function (area) {
    const input = area.querySelector('.file-input-hidden') ||
                  area.parentNode.querySelector('.file-input-hidden');
    if (input) {
      area.addEventListener('click', () => input.click());
      input.addEventListener('change', function () {
        if (this.files[0]) {
          const icon = area.querySelector('i');
          const span = area.querySelector('span');
          if (span) span.textContent = this.files[0].name;
          if (icon) { icon.className = 'fa-solid fa-check'; icon.style.color = '#10B981'; }
        }
      });
    }
  });

  // ── Form: real file input trigger ─────────────────
  document.querySelectorAll('input[type="file"]').forEach(function (input) {
    if (!input.classList.contains('file-input-hidden')) {
      input.addEventListener('change', function () {
        const label = this.previousElementSibling;
        if (label && label.classList.contains('file-upload-area') && this.files[0]) {
          label.querySelector('span').textContent = this.files[0].name;
        }
      });
    }
  });

  // ── Landing: scroll nav ────────────────────────────
  const landingNav = document.getElementById('landing-nav');
  if (landingNav) {
    window.addEventListener('scroll', function () {
      landingNav.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // ── Smooth scroll for anchor links ─────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Filter form: live search delay ─────────────────
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        const form = searchInput.closest('form');
        if (form && this.value.length !== 1) form.submit();
      }, 500);
    });
  }

  // ── Confirm dialogs ────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) e.preventDefault();
    });
  });

});
