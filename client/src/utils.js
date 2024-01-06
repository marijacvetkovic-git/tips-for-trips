export function parseJwt(token) {
  if (token == null) {
    return;
  }
  var base64Url = token.split(".")[1];
  var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  var jsonPayload = decodeURIComponent(
    atob(base64)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );
  return JSON.parse(jsonPayload);
}
export function getUsername() {
  var user = localStorage.getItem("token");
  if (user == null) {
    return;
  }
  const username=parseJwt(user)?.username
  console.log(username)
  return username;
}
export function getUserId() {
  var user = localStorage.getItem("token");
  if (user == null) {
    return;
  }
  const id=parseJwt(user)?.id
  console.log(id)
  return id;
}
export function getExpiration() {
  var user = localStorage.getItem("token");
  if (user == null) {
    return;
  }
  const exp=parseJwt(user)?.exp
  console.log(exp)
  return exp;
}