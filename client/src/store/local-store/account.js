import { storeNames, getValue, removeValue } from "./_meta";

const getLogin = getValue(storeNames.login);
const removeLogin = removeValue(storeNames.login);

export const account = {
  getLogin,
  removeLogin
};
