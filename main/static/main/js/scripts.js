const searchInput = document.getElementById('searchInput');
const clearSearch = document.getElementById('clearSearch');
const categoryGrid = document.getElementById('categoryGrid');

function updateFilter() {
  const query = searchInput.value.trim().toLowerCase();
  const cards = categoryGrid.querySelectorAll('.category-card');
  cards.forEach(card => {
    const title = card.dataset.title;
    const subtitle = card.dataset.subtitle;
    const match = title.includes(query) || subtitle.includes(query);
    card.style.display = match ? 'block' : 'none';
  });
}

searchInput.addEventListener('input', () => {
  updateFilter();
});

clearSearch.addEventListener('click', () => {
  searchInput.value = '';
  updateFilter();
  searchInput.focus();
});

window.addEventListener('DOMContentLoaded', () => {
  updateFilter();
});
