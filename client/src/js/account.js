import { localStore } from "@wp/store";

export function logIn();
export function logOut() {
  localStore.account.removeLogin();
  localStore.favorites.removeFavouriteUsers();
  localStore.favorites.removeFavouritePosts();
  location.href = '/account/logout';
}
