import { createComponent } from "./_index";

/**
 * @param {HTMLElement} element 
 * @param {KemonoAPI.Post} post
 */
export function PostCard(element = null, post = {}) {
  const postCard = element
    ? initFromElement(element)
    : initFromScratch(post);

  const view = postCard.postCardElement.querySelector(".post-card__view");

  if (view) {
    /**
     * @type {HTMLButtonElement}
     */
    const button = view.querySelector(".post-card__button");
    /**
     * @type {HTMLAnchorElement}
     */
    const link = postCard.postCardElement.querySelector(".post-card__link");

    button.addEventListener("click", handlePostView(link));
  }

  return postCard;
};

/**
 * @param {HTMLElement} element 
 */
function initFromElement(element) {
  const { id, service, user } = element.dataset;
  return {
    postCardElement: element,
    postID: id,
    service,
    userID: user
  }
}

/**
 * @param {KemonoAPI.Post} post 
 */
function initFromScratch(post) {
  /**
   * @type {HTMLElement}
   */
  const postCardElement = createComponent("post-card");

  return {
    postCardElement,
    postID: post.id,
    service: post.service,
    userID: post.user
  }
}

/**
 * @param {HTMLAnchorElement} link
 * @returns {(event: MouseEvent) => void}
 */
function handlePostView(link) {
  return (event) => {
    link.focus();
  }
}
