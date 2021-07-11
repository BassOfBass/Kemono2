import { addFavouriteArtist, findFavouriteArtist, removeFavouriteArtist, findFavouritePost } from "@wp/js/favorites";
import { CardList, createComponent, PostCard } from "./components/_index";

/** 
 * @param {HTMLElement} section
 */
export async function userPage(section) {
  const artistID = document.head.querySelector("[name='id']").content;
  const artistService = document.head.querySelector("[name='service']").content;
  /**
   * @type {HTMLElement}
   */
  const buttonsPanel = section.querySelector(".user-header__actions");
  const cardListElement = section.querySelector(".card-list");

  await initButtons(buttonsPanel, artistID, artistService);
  await initCardList(cardListElement);
}

/**
 * @param {HTMLElement} panelElement 
 * @param {string} artistID 
 * @param {string} artistService 
 */
async function initButtons(panelElement, artistID, artistService) {
  /**
   * @type {HTMLButtonElement}
   */
  const favButton = createComponent("user-header__favourite");
  const favItem = await findFavouriteArtist(artistID, artistService);

  if (localStorage.getItem('logged_in') && favItem) {
    favButton.classList.add("user-header__favourite--unfav");
    const [icon, text] = favButton.children;
    icon.textContent = "★";
    text.textContent = "Unfavorite";
  }

  favButton.addEventListener("click", handleFavouriting(artistID, artistService));

  panelElement.appendChild(favButton);
}

/**
 * @param {HTMLElement} cardListElement 
 */
async function initCardList(cardListElement) {
  const { cardItems } = CardList(cardListElement);

  cardItems.forEach(async (card) => {
    const { postID, userID, service } = PostCard(card);
    const favPost = await findFavouritePost(service, userID, postID);

    if (favPost) {
      card.classList.add("post-card--fav");
    }
  });
}

/**
 * @param {string} id
 * @param {string} service
 * @returns {(event: MouseEvent) => Promise<void>}
 */
function handleFavouriting(id, service) {
  return async (event) => {
    /**
     * @type {HTMLButtonElement}
     */
    const button = event.target;
    const [icon, text] = button.children;
    /**
     * @type {HTMLElement}
     */
    const loadingIcon = createComponent("loading-icon");

    button.disabled = true;
    button.classList.add("user-header__favourite--loading");
    button.insertBefore(loadingIcon, text);
    
    try {
      if (button.classList.contains("user-header__favourite--unfav")) {
        const isRemoved = await removeFavouriteArtist(id, service);

        if (isRemoved) {
          button.classList.remove("user-header__favourite--unfav");
          icon.textContent = "☆";
          text.textContent = "Favorite";
        }
        
      } else {
        const isAdded = await addFavouriteArtist(id, service);

        if (isAdded) {
          button.classList.add("user-header__favourite--unfav");
          icon.textContent = "★";
          text.textContent = "Unfavorite";
        }

      }
    } catch (error) {
      alert(error);
      
    } finally {
      loadingIcon.remove();
      button.disabled = false;
      button.classList.remove("user-header__favourite--loading");
    }
    
  }
}
