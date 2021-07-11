import { createComponent } from "./_index";

/**
 * @param {HTMLElement} element 
 * @param {KemonoAPI.Post} post
 */
export function PostCard(element = null, post = {}) {
  const postCard = element
    ? initFromElement(element)
    : initFromScratch(post);

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
