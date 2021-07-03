import { kemonoAPI } from "@wp/api";
import { localStore } from "@wp/store";

export async function initFavorites() {
  let userFavs = localStore.favorites.getFavouriteUsers();
  let postFavs = localStore.favorites.getFavouritePosts();

  if (!userFavs) {
    /**
     * @type {string}
     */
    const favs = await kemonoAPI.favorites.retrieveFavoriteArtists();

    if (favs) {
      localStore.favorites.setFavouriteUsers(favs);
    }
  }

  if (!postFavs) {
    /**
     * @type {string}
     */
    const favs = await kemonoAPI.favorites.retrieveFavoritePosts();

    if (favs) {
      localStore.favorites.setFavouritePosts(favs);
    }
  }
}

async function saveFavouriteArtists() {
  try {
    const favs = await kemonoAPI.favorites.retrieveFavoriteArtists();
    
    if (!favs) {
      alert("Could not retrieve favorite artists");
      return false;
    }

    localStore.favorites.setFavouriteUsers(favs);
    return true;

  } catch (error) {
    console.error(error);
    return false;
  }
}

async function saveFavouritePosts() {
  try {
    const favs = await kemonoAPI.favorites.retrieveFavoritePosts();
    
    if (!favs) {
      alert("Could not retrieve favorite posts");
      return false;
    }

    localStore.favorites.setFavouritePosts(favs);
    return true;

  } catch (error) {
    console.error(error);
    return false;
  }
}

/**
 * @param {string} id 
 * @param {string} service
 * @returns {Promise<KemonoAPI.Favorites.Artist | undefined>}
 */
export async function findFavouriteArtist(id, service) {
  /**
   * @type {KemonoAPI.Favorites.Artist[]}
   */
  let favList;

  try {
    favList = JSON.parse(localStore.favorites.getFavouriteUsers());

  } catch (error) {
    // corrupted entry
    if (error instanceof SyntaxError) {
      const isSaved = await saveFavouriteArtists();

      if (!isSaved) {
        return undefined;
      }

      return await findFavouriteArtist(id, service);
    }
  }

  if (!favList) {
    return undefined;
  }
  
  const favArtist = favList.find((favItem) => {
    return favItem.id === id && favItem.service === service;
  });

  return favArtist;
}

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} postID 
 * @returns {Promise<KemonoAPI.Favorites.Post | undefined>}
 */
export async function findFavouritePost(service, user, postID) {
  /**
   * @type {KemonoAPI.Favorites.Post[]}
   */
  let favList;
 
  try {
    
    favList = JSON.parse(localStore.favorites.getFavouritePosts());
    
    if (!favList) {
      return undefined;
    }

    const favPost = favList.find((favItem) => {
      const isMatch = favItem.id === postID 
        && favItem.service === service
        && favItem.user === user;
      return isMatch;
    });
  
    return favPost;

  } catch (error) {
    // corrupted entry
    if (error instanceof SyntaxError) {
      const isSaved = await saveFavouritePosts();

      if (!isSaved) {
        return undefined;
      }

      return await findFavouritePost(service, user, postID);
    }
  }
}

/**
 * @param {string} id 
 * @param {string} service 
 */
export async function addFavouriteArtist(id, service) {
  const isFavorited = await kemonoAPI.favorites.favoriteArtist(service, id);

  if (!isFavorited) {
    return false;
  }

  const newFavs = await kemonoAPI.favorites.retrieveFavoriteArtists();
  localStore.favorites.setFavouriteUsers(newFavs);

  return true;
}

/**
 * @param {string} id 
 * @param {string} service 
 */
export async function removeFavouriteArtist(id, service) {
  const isUnfavorited = await kemonoAPI.favorites.unfavoriteArtist(service, id);

  if (!isUnfavorited) {
    return false
  }

  const favItems = await kemonoAPI.favorites.retrieveFavoriteArtists();
  localStore.favorites.setFavouriteUsers(favItems);

  return true;
}

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} postID 
 */
export async function addFavouritePost(service, user, postID) {
  const isFavorited = await kemonoAPI.favorites.favoritePost(service, user, postID);

  if (!isFavorited) {
    return false;
  }

  const newFavs = await kemonoAPI.favorites.retrieveFavoritePosts();
  localStore.favorites.setFavouritePosts(newFavs)

  return true;
};

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} postID 
 * @returns 
 */
export async function removeFavouritePost(service, user, postID) {
  const isUnfavorited = await kemonoAPI.favorites.unfavoritePost(service, user, postID);

  if (!isUnfavorited) {
    return false
  }

  const favItems = await kemonoAPI.favorites.retrieveFavoritePosts();
  localStore.favorites.setFavouritePosts(favItems);

  return true;
};
