import { CardList } from "@wp/components";

/**
 * @param {HTMLElement} section 
 */
export function postsPage(section) {
  const postCardElem = section.querySelector(".card-list");
  const cardList = CardList(postCardElem, "feature", ["feature", "mobile"]);
}
