import { localStore } from "@wp/store";

/**
 * @param {HTMLElement} section 
 */
export function registerPage(section) {
  populate_favorites();
}

function populate_favorites() {
  var input = document.getElementById('serialized-favorites');
  var favorites = localStore.legacy.getFavorites();
  var to_serialize = [];
  if (input && favorites) {
    var artists = favorites.split(',');
    artists.forEach(function (artist) {
      var split = artist.split(':');
      if (split.length != 2) { return; }
      var elem = {
        'service': split[0],
        'artist_id': split[1]
      };
      to_serialize.push(elem);
    });
    var serialized = JSON.stringify(to_serialize);
    input.value = serialized;
  }
}
