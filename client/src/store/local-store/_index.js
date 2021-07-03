import { legacy } from "./legacy";
import { favorites } from "./favorites";
import { account } from "./account";

export const localStore = {
  account,
  favorites,
  legacy
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
