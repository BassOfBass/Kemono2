export const storeNames = {
  userFavs: "favs",
  postFavs: "post_favs",
  login: "logged_in",
};

export const legacyNames = {
  favorites: "favorites",
}

/**
 * @param {string} storageName 
 * @returns 
 */
export function getValue(storageName) {
  return () => {
    const string = localStorage.getItem(storageName);
    return string;
  }
}

/**
 * @param {string} storageName 
 * @returns {(value: string) => boolean}
 */
export function setValue(storageName) {
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
export function removeValue(storageName) {
  return () => {
    localStorage.removeItem(storageName);
  }
}
