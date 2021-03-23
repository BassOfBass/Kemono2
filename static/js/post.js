function attemptFlag (_, api) {
  if (confirm('Are you sure you want to flag this post for reimport?')) {
    fetch(api, { method: 'post' })
      .then(function (res) {
        window.alert(res.ok ? 'Successfully flagged.' : 'Error. There might already be a flag here.');
      });
  }
}

function favorite_post(service, user, post_id) {
  fetch(`/favorites/post/${service}/${user}/${post_id}`, {
    method: 'POST'
  }).then(res => {
    if (res.redirected) {
      window.location = res.url;
    } else if (res.ok) {
      location.reload();
    } else {
      alert('Error 001 - could not save favorite');
    }
  });
}

function unfavorite_post(service, user, post_id) {
  fetch(`/favorites/post/${service}/${user}/${post_id}`, {
    method: "DELETE"
  }).then(res => {
    if (res.redirected) {
      window.location = res.url;
    } else if (res.ok) {
      location.reload();
    } else {
      alert('Error 002 - could not remove favorite');
    }
  });
}
