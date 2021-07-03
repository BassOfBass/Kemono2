import { legacyNames, getValue, removeValue } from "./_meta";

const getFavorites = getValue(legacyNames.favorites);
const removeFavorites = removeValue(legacyNames.favorites);

export const legacy = {
  getFavorites,
  removeFavorites,
}
