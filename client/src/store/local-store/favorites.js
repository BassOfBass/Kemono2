import { storeNames, getValue, removeValue, setValue } from "./_meta";

const getFavouriteUsers = getValue(storeNames.userFavs);
const getFavouritePosts = getValue(storeNames.postFavs);
const setFavouriteUsers = setValue(storeNames.userFavs);
const setFavouritePosts = setValue(storeNames.postFavs);
const removeFavouriteUsers = removeValue(storeNames.userFavs);
const removeFavouritePosts = removeValue(storeNames.postFavs);

export const favorites = {
  getFavouriteUsers,
  getFavouritePosts,
  setFavouriteUsers,
  setFavouritePosts,
  removeFavouriteUsers,
  removeFavouritePosts,
};
