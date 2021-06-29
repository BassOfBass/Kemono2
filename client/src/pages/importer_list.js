/**
 * @param {HTMLElement} section 
 */
export function importerPage(section) {
  /**
   * @type {HTMLFormElement}
   */
  const form = section.querySelector(".form");
  const discordSection = form.querySelector("#discord-section");

  form.addEventListener("change", switchDiscordSection(discordSection));
}

/**
 * @param {HTMLElement} discordSection
 * @returns {(event: Event) => void}
 */
function switchDiscordSection(discordSection) {
  return (event) => {
    if (event.target.id === "service") {
      event.stopPropagation();
  
      /**
       * @type {HTMLSelectElement}
       */
      const select = event.target;
  
      if (select.value === "discord") {
        discordSection.classList.remove("form__section--hidden");
      } else {
        discordSection.classList.add("form__section--hidden");
      }
    }
  }
  
}
