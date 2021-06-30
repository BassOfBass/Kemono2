/**
 * @param {HTMLElement} section 
 */
export function newRequestsPage(section) {
  const form = document.forms[0];
  
  /** 
   * @type {HTMLFieldSetElement}
   */
  const radioSet = form.querySelector("#conditions");
  const conditionElement = radioSet.querySelector("fieldset");
  
  radioSet.addEventListener("change", handleConditions(conditionElement));
}

/**
 * @param {HTMLFieldSetElement} conditionElement
 * @returns {(event: Event) => void} 
 */
function handleConditions(conditionElement) {
  return (event) => {
    event.stopPropagation();
    /**
     * @type {HTMLInputElement}
     */
    const radio = event.target;

    if (radio.value === "specific") {
      conditionElement.disabled = false;
    } else {
      conditionElement.disabled = true;
    }
  }
  
}
