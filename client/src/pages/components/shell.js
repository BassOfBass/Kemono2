import { localStore } from "@wp/store";

/**
 * @param {HTMLElement} header 
 * @param {SVGAnimatedBoolean} isLoggedIn 
 */
export function initShell(header, isLoggedIn) {
  const accButtons = header.querySelector("#account-buttons");

  // TODO: rewrite into without string literals
  if (isLoggedIn) {
    accButtons.innerHTML += `
      <li><a href="/favorites">[Favorites]</a></li>
      <li><a id="logout" href="/account/logout">[Logout]</a></li>
    `
    document.getElementById('logout').addEventListener('click', e => {
      e.preventDefault();
      localStore.account.removeLogin();
      localStore.favorites.removeFavouriteUsers();
      localStore.favorites.removeFavouritePosts();
      location.href = '/account/logout';
    })
  } else {
    accButtons.innerHTML += `
      <li><a href="/account/login">[Login]</a></li>
    `
  }
}
