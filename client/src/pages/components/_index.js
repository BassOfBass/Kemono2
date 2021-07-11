export { LoadingIcon } from "./loading_icon";
export { CardList } from "./card_list";
export { PostCard } from "./cards";


/**
 * @type {Map<string, HTMLElement>}
 */
const components = new Map();

/**
 * @param {HTMLElement} footer 
 */
export function initComponentFactory(footer) {
  const container = footer.querySelector(".component-container");
  /**
   * @type {NodeListOf<HTMLElement}
   */
  const componentElements = container.querySelectorAll(`#${container.id} > *`);

  componentElements.forEach((component) => {
    components.set(component.className, component);
  });
  
  container.remove();
}

/**
 * @param {string} className 
 */
export function createComponent(className) {
  const componentSkeleton = components.get(className);

  if (!componentSkeleton) {
    return console.error(`Component "${className}" doesn't exist.`);
  }

  const newInstance = componentSkeleton.cloneNode(true);
  
  return newInstance;
}
