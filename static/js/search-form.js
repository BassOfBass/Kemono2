document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.querySelector(".search-form");
  const advButton = searchForm.querySelector(".search-form__advanced-button");
  const advSection = searchForm.querySelector(".search-form__advanced-section");

  advButton.addEventListener("click", toggleAdvancedOptions);

  function toggleAdvancedOptions(event) {
    advSection.classList.toggle("search-form__advanced-section--hidden");
  }
});