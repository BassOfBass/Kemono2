const storeNames = {
  userFavs: "favs",
  postFavs: "post_favs",
  login: "logged_in",
};

const legacyNames = {
  favorites: "favorites",
}

export const localStore = {
  account: {
    getLogin: getValue(storeNames.login),
    removeLogin: removeValue(storeNames.login)
  },
  favorites: {
    getFavouriteUsers: getValue(storeNames.userFavs),
    setFavouriteUsers: setValue(storeNames.userFavs),
    removeFavouriteUsers: removeValue(storeNames.userFavs),
    getFavouritePosts: getValue(storeNames.postFavs),
    setFavouritePosts: setValue(storeNames.postFavs),
    removeFavouritePosts: removeValue(storeNames.postFavs),
  },
  legacy: {
    getFavorites: getValue(legacyNames.favorites),
    removeFavorites: removeValue(legacyNames.favorites),
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
