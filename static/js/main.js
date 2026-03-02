document.addEventListener('DOMContentLoaded', () => {
  setupUploadForm();
  setupPublicFilesSearch();
  setupDashboardSearch();
});

function setupUploadForm() {
  const uploadForm = document.getElementById('upload-form');
  if (!uploadForm) return;

  const fileInput = document.getElementById('file-input');
  const nameInput = uploadForm.querySelector('input[name="name"]');

  if (fileInput && nameInput) {
    fileInput.addEventListener('change', () => {
      const file = fileInput.files[0];
      if (file && !nameInput.value.trim()) {
        nameInput.value = file.name.replace(/\.[^/.]+$/, '');
      }
    });
  }

  uploadForm.addEventListener('submit', (e) => {
    if (!fileInput) return;
    const file = fileInput.files[0];
    if (file && file.size > 10 * 1024 * 1024) {
      e.preventDefault();
      alert('Fichier trop volumineux (max 10 Mo).');
    }
  });
}

function setupPublicFilesSearch() {
  const input = document.getElementById('search-input');
  if (!input) return;

  const cards = Array.from(document.querySelectorAll('[data-public-file]'));
  const counter = document.getElementById('home-count');
  const empty = document.getElementById('public-empty');

  const applyFilter = () => {
    const query = input.value.trim().toLowerCase();
    let visible = 0;

    cards.forEach((card) => {
      const name = card.dataset.name || '';
      const description = card.dataset.description || '';
      const match = !query || name.includes(query) || description.includes(query);
      card.classList.toggle('hidden', !match);
      if (match) visible += 1;
    });

    if (counter) {
      counter.textContent = `${visible} fichier(s)`;
    }

    if (empty) {
      empty.classList.toggle('hidden', visible !== 0);
    }
  };

  input.addEventListener('input', applyFilter);
  applyFilter();
}

function setupDashboardSearch() {
  const input = document.getElementById('dashboard-search');
  if (!input) return;

  const rows = Array.from(document.querySelectorAll('[data-private-file]'));
  const empty = document.getElementById('dashboard-empty');

  const applyFilter = () => {
    const query = input.value.trim().toLowerCase();
    let visible = 0;

    rows.forEach((row) => {
      const name = row.dataset.name || '';
      const match = !query || name.includes(query);
      row.classList.toggle('hidden', !match);
      if (match) visible += 1;
    });

    if (empty) {
      empty.classList.toggle('hidden', visible !== 0);
    }
  };

  input.addEventListener('input', applyFilter);
  applyFilter();
}
