document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.querySelector(".artist-search-form");
  const advButton = searchForm.querySelector(".artist-search-form__advanced-button");
  const advSection = searchForm.querySelector(".artist-search-form__advanced-section");

  advButton.addEventListener("click", toggleAdvancedOptions);

  function toggleAdvancedOptions(event) {
    advSection.classList.toggle("artist-search-form__advanced-section--hidden");
  }
});