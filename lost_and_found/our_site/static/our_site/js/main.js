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

  // ── Live search filter (item list page) ──────────────────────
  const searchInput = document.getElementById('search-input');
  const itemCards = document.querySelectorAll('.item-card-link');

  if (searchInput && itemCards.length > 0) {
    // Debounce helper
    let debounceTimer;
    searchInput.addEventListener('input', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        // Let the server handle it – just auto-submit the form
        this.closest('form').submit();
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

});
