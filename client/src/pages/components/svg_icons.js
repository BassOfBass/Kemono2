import { createComponent } from "./_index";
import svgSpritesheet from "@wp/assets/svg-spritesheet.svg";

/**
 * @param {string} id 
 * @param {string} className 
 * @returns {HTMLSpanElement | HTMLDivElement}
 */
export function SVGIcon(id, className=undefined) {
  /**
   * @type {HTMLSpanElement}
   */
  const icon = createComponent("svg-icon");
  /** 
   * @type {SVGUseElement}
   */
  const useElem = icon.querySelector("svg-icon__use");

  if (className) {
    icon.classList.add(className);
  }

  
  useElem.href = `${svgSpritesheet}#${id}`;

  return icon;
}
