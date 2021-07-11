import { createComponent } from "./_index";

/**
 * TODO: layout switch button.
 * @param {HTMLElement} element 
 * @param {string} layout 
 */
export function CardList(element=null, layout="feature") {
  const {cardList, cardItems} = element
    ? initFromElement(element)
    : initFromScratch();
  let currentLayout = layout;

  return {
    cardList, 
    cardItems
  };
}

/**
 * @param {HTMLElement} element 
 */
function initFromElement(element) {
  /**
   * @type {NodeListOf<HTMLElement>}
   */
  const itemListElements = element.querySelectorAll(".card-list__items > *");

  return {
    cardList: element,
    cardItems: Array.from(itemListElements)
  };
}

function initFromScratch() {
  /**
   * @type {HTMLElement}
   */
  const cardList = createComponent("card-list");
  /**
   * @type {HTMLElement[]}
   */
  const cardItems = [];

  return {
    cardList,
    cardItems
  };
}
