const storeNames = {
  userFavs: "favs",
  postFavs: "post_favs",
  login: "logged_in",
};

const legacyNames = {
  favorites: "favorites",
}

const getLogin = getValue(storeNames.login);
const removeLogin = removeValue(storeNames.login);
const getFavorites = getValue(legacyNames.favorites);
const removeFavorites = removeValue(legacyNames.favorites);
const getFavouriteUsers = getValue(storeNames.userFavs);
const setFavouriteUsers = setValue(storeNames.userFavs);
const getFavouritePosts = getValue(storeNames.postFavs);
const setFavouritePosts = setValue(storeNames.postFavs);
const removeFavouriteUsers = removeValue(storeNames.userFavs);
const removeFavouritePosts = removeValue(storeNames.postFavs);

export const localStore = {
  account: {
    getLogin,
    removeLogin
  },
  favorites: {
    getFavouriteUsers,
    getFavouritePosts,
    setFavouriteUsers,
    setFavouritePosts,
    removeFavouriteUsers,
    removeFavouritePosts,
  },
  legacy: {
    getFavorites,
    removeFavorites,
  }
}

/**
 * @param {string} storageName 
 * @returns 
 */
function getValue(storageName) {
  return () => {
    const string = localStorage.getItem(storageName);
    return string;
  }
}

/**
 * @param {string} storageName 
 * @returns {(value: string) => boolean}
 */
function setValue(storageName) {
  return (value) => {
    try {
      localStorage.setItem(storageName, value);
      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  }
}

/**
 * @param {string} storageName 
 * @returns 
 */
function removeValue(storageName) {
  return () => {
    localStorage.removeItem(storageName);
  }
}

/*
  function isStorageAvailable() {
    try {
      localStorage.setItem("__storage_test__", "__storage_test__");
      localStorage.removeItem("__storage_test__");
      return true;
    } catch (error) {
      return false;
    }
  }
*/
