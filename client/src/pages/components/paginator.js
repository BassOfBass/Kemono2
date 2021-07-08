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
  const pageSelector = selectorForm.querySelector(".form__input");

  selectorForm.addEventListener("submit", );

  return paginator;
};
