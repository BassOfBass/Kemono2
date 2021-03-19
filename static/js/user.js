require.config({
  paths: {
    oboe: 'https://unpkg.com/oboe@2.1.5/dist/oboe-browser.min'
  }
});

/* eslint-disable no-unused-vars */
function favorite (service, user) {
  const favorites = localStorage.getItem('favorites') ? localStorage.getItem('favorites').split(',') : [];
  if (favorites.includes(service + ':' + user)) return;
  favorites.push(service + ':' + user);
  localStorage.setItem('favorites', favorites.join(','));
  location.reload();
}

function unfavorite (service, user) {
  let favorites = localStorage.getItem('favorites') ? localStorage.getItem('favorites').split(',') : [];
  favorites = favorites.filter(i => i !== service + ':' + user);
  localStorage.setItem('favorites', favorites.join(','));
  location.reload();
}
/* eslint-enable no-unused-vars */

function loadQuery () {
  const query = document.getElementById('search-input').value;
  const pathname = window.location.pathname.split('/');
  const contentView = document.getElementById('content');
  contentView.innerHTML = '';
  const api = ({
    patreon: `/api/patreon/user/${pathname[3]}/lookup?q=${query}`,
    fanbox: `/api/fanbox/user/${pathname[3]}/lookup?q=${query}`,
    gumroad: `/api/gumroad/user/${pathname[3]}/lookup?q=${query}`,
    subscribestar: `/api/subscribestar/user/${pathname[3]}/lookup?q=${query}`,
    dlsite: `/api/dlsite/user/${pathname[3]}/lookup?q=${query}`
  })[document.getElementsByName('service')[0].content];
  require(['oboe'], function (oboe) {
    oboe(api)
      .node('!.*', function (post) {
        return renderPost(post);
      });
  });
}

(function () {
  document.getElementById('search-input').addEventListener('keyup', debounce(() => loadQuery(), 350));
  let service, api, proxy, href;
  const infoView = document.getElementById('info-block');
  const extraView = document.getElementById('extra-info-block');
  const pathname = window.location.pathname.split('/');
  switch (document.getElementsByName('service')[0].content) {
    case 'patreon':
      service = 'Patreon';
      api = `/api/lookup/cache/${pathname[3]}?service=patreon`;
      proxy = `/proxy/patreon/user/${pathname[3]}`;
      href = `https://www.patreon.com/user?u=${pathname[3]}`;
      break;
    case 'fanbox':
      service = 'Fanbox';
      api = `/api/lookup/cache/${pathname[3]}?service=fanbox`;
      href = `https://www.pixiv.net/fanbox/creator/${pathname[3]}`;
      break;
    case 'gumroad':
      service = 'Gumroad';
      api = `/api/lookup/cache/${pathname[3]}?service=gumroad`;
      href = `https://gumroad.com/${pathname[3]}`;
      break;
    case 'subscribestar':
      service = 'SubscribeStar';
      api = `/api/lookup/cache/${pathname[3]}?service=subscribestar`;
      href = `https://subscribestar.adult/${pathname[3]}`;
      break;
    case 'dlsite':
      service = 'DLsite';
      api = `/api/lookup/cache/${pathname[3]}?service=dlsite`;
      href = `https://www.dlsite.com/eng/circle/profile/=/maker_id/${pathname[3]}`;
      break;
  }
  fetch(api)
    .then(function (res) { return res.json(); })
    .then(function (cache) {
      document.title = `${cache.name} | Kemono`;
      infoView.innerHTML += `
        <li>
          Service: <a href="${href}" target="_blank" rel="noreferrer">${service}</a>
        </li>
        <li>
          User: <a href="${window.location.href.split('?')[0]}">${cache.name}</a>
        </li>
        ${localStorage.getItem('favorites') && localStorage.getItem('favorites').split(',').includes(document.getElementsByName('service')[0].content + ':' + pathname[3]) ? `
          <li class="subtitle">
            ★ Favorited <a href="javascript:unfavorite('${document.getElementsByName('service')[0].content}', '${pathname[3]}');">(☆)</a>
          </li>
        ` : `
          <li>
            <a href="javascript:favorite('${document.getElementsByName('service')[0].content}', '${pathname[3]}');">☆ Favorite</a>
          </li>
        `}
      `;
    });
  if (service === 'Patreon') {
    fetch(proxy)
      .then(function (res) { return res.json(); })
      .then(function (user) {
        extraView.innerHTML += `
          <li>
            Tagline: ${user.included[0].attributes.creation_name}
          </li>
          <li>
            CUF Enabled: ${user.included[0].attributes.is_charge_upfront ? 'Yes' : '<span style="color: #0f0">No</span>'}
          </li>
          <li>
            ${user.included[0].attributes.creation_count > Number(document.getElementsByName('count')[0].content) ? `
              <span style="color:#cc0">Missing ${user.included[0].attributes.creation_count - Number(document.getElementsByName('count')[0].content)} posts</span>
            ` : '<span style="color:#0f0">Up to date</span>'}
          </li>
        `;
      });
  }
})();
