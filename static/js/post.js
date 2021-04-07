function attemptFlag (service, user, post_id) {
  if (confirm('Are you sure you want to flag this post for reimport?')) {
    fetch(`/api/${service}/user/${user}/post/${post_id}/flag`, { method: 'post' })
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
      window.location = add_url_param(res.url, 'redir', window.location.pathname);
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
      window.location =  add_url_param(res.url, 'redir', window.location.pathname);;
    } else if (res.ok) {
      location.reload();
    } else {
      alert('Error 002 - could not remove favorite');
    }
  });
}

Array.prototype.forEach.call(document.getElementsByClassName('flag'), function (flag) {
  flag.addEventListener('click', function (_) {
    attemptFlag(
      flag.getAttribute('data-service'),
      flag.getAttribute('data-user'),
      flag.getAttribute('data-post')
    );
  })
});
