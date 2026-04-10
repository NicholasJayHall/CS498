document.addEventListener('DOMContentLoaded', function () {

  // ── Image upload preview ─────────────────────────────────────
  const imgInput = document.getElementById('id_image');
  const imgPreview = document.getElementById('img-preview');

  if (imgInput && imgPreview) {
    imgInput.addEventListener('change', function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          imgPreview.src = e.target.result;
          imgPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      } else {
        imgPreview.style.display = 'none';
        imgPreview.src = '';
      }
    });
  }

  // ── Live search & filter (item list page) ──────────────────────
  const searchInput = document.getElementById('search-input');

  if (searchInput) {
    const filterForm = searchInput.closest('form');
    const urlParams = new URLSearchParams(window.location.search);

    // 1. Persistence: Keep focus even if query is empty after refresh
    // We check the URL for 'q' to see if the user was just searching
    if (urlParams.has('q')) {
      searchInput.focus();
      const textLength = searchInput.value.length;
      searchInput.setSelectionRange(textLength, textLength);
    }

    // 2. Auto-refresh for dropdowns (Category and Status)
    filterForm.querySelectorAll('select').forEach(select => {
      select.addEventListener('change', () => {
        filterForm.submit();
      });
    });

    // 3. Auto-refresh for search typing (Debounced)
    let debounceTimer;
    searchInput.addEventListener('input', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        filterForm.submit();
      }, 600);
    });
  } 

  // ── Fade-in animation on cards ───────────────────────────────
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = entry.target.style.transform.replace('translateY(16px)', 'translateY(0)');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.item-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = (card.style.transform || '') + ' translateY(16px)';
    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease, box-shadow 0.2s ease';
    observer.observe(card);
  });

  // ── Auto-dismiss alerts after 5s ────────────────────────────
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => {
      el.style.transition = 'opacity 0.5s ease';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    });
  }, 5000);

  // ── Confirm delete ───────────────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // ── Waffle menu bar for smaller screen 

const waffle = document.querySelector('.nav-waffle');
const navLinks = document.querySelector('.nav-links');

if (waffle && navLinks) {
  waffle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
  });
}


});
