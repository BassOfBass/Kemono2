import { createComponent } from "./_index";

const defaultLayouts = [
  "feature",
  "mobile",
  "phone",
  "tablet",
  "laptop",
  "desktop",
]

/**
 * TODO: layout switch button.
 * @param {HTMLElement} element 
 * @param {string[]} layouts 
 * @param {string} layout 
 */
export function CardList(element=null, layout=defaultLayouts[0], layouts=defaultLayouts) {
  /**
   * @type {HTMLElement}
   */
  const cardList = element
    ? element
    : createComponent("card-list");
  let currentLayout = layout;

  return cardList;
}
