import { createComponent } from "./_index";

/**
 * @param {HTMLElement} element 
 * @returns {HTMLElement}
 */
export function Paginator(element) {
  /**
   * @type {HTMLElement}
   */
  const paginator = element
    ? element
    : createComponent("paginator");
  
  const pages = paginator.querySelector(".paginator__pages");
  /**
   * @type {HTMLFormElement}
   */
  const selectorForm = paginator.querySelector(".paginator__selector");
  /**
   * @type {[ HTMLLabelElement, HTMLButtonElement, HTMLInputElement, HTMLButtonElement, HTMLButtonElement ]}
   */
  const [ label, decrement, input, increment, submit ] = selectorForm.children;

  selectorForm.addEventListener("click", handlePageSelect(input, increment, decrement));
  selectorForm.addEventListener("submit", handlePageChange);

  return paginator;
};

/**
 * @param {HTMLInputElement} input 
 * @param {HTMLButtonElement} increment 
 * @param {HTMLButtonElement} decrement 
 * @returns {(event: MouseEvent) => void}
 */
function handlePageSelect(input, increment, decrement) {
  
  return (event) => {
    event.stopPropagation();

    /**
     * @type {HTMLButtonElement}
     */
    const button = event.target;

    if (button === decrement) {
      input.stepDown();
    }
    
    if (button === increment) {
      input.stepUp();
    }
  }
}

/**
 * @param {Event} event 
 */
function handlePageChange(event) {
  event.preventDefault();
}
