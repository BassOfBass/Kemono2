import "./global.scss";
import { localStore } from "@wp/store";
import { initSections } from "@wp/pages";
import { initFavorites } from "@wp/js/favorites";


const isLoggedIn = localStore.account.getLogin() === "yes";

if (isLoggedIn) {
  initFavorites()
}

initSections(isLoggedIn);
