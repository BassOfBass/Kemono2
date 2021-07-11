import { CardList, PostCard } from "@wp/components";
import { findFavouritePost, findFavouriteArtist } from "@wp/js/favorites";

/**
 * @param {HTMLElement} section 
 */
export function postsPage(section) {
  const cardListElement = section.querySelector(".card-list");
  const { cardList, cardItems } = CardList(cardListElement);

  cardItems.forEach(async (card) => {
    const { postID, userID, service } = PostCard(card);
    const favPost = await findFavouritePost(service, userID, postID);
    const favUser = await findFavouriteArtist(userID, service);

    if (favPost) {
      card.classList.add("post-card--fav");
    };

    if (favUser) {
      const header = card.querySelector(".post-card__header");
      const userName = header.querySelector(".post-card__name");

      header.classList.add("post-card__header--fav");
      userName.textContent = favUser.name;
    };

  });
}
