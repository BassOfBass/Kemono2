/* eslint-disable no-unused-vars */
function favorite_artist(service, user) {
  fetch(`/favorites/artist/${service}/${user}`, {
    method: 'POST'
  }).then(res => {
    if (res.redirected) {
      window.location =  add_url_param(res.url, 'redir', window.location.pathname);;
    } else if (res.ok) {
      location.reload();
    } else {
      alert('Error 003 - could not save favorite');
    }
  });
}

function unfavorite_artist(service, user) {
  fetch(`/favorites/artist/${service}/${user}`, {
    method: "DELETE"
  }).then(res => {
    if (res.redirected) {
      window.location =  add_url_param(res.url, 'redir', window.location.pathname);;
    } else if (res.ok) {
      location.reload();
    } else {
      alert('Error 004 - could not remove favorite');
    }
  });
}
/* eslint-enable no-unused-vars */
