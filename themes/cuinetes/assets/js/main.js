// Instagram feed
const igFeed = document.getElementById('ig-feed');
if (igFeed) {
  fetch('/instagram.json')
    .then(r => r.json())
    .then(data => {
      if (!data.posts || data.posts.length === 0) return;
      const cta = document.getElementById('ig-cta');
      if (cta) cta.remove();
      const grid = document.createElement('div');
      grid.className = 'ig-grid';
      data.posts.forEach(post => {
        if (!post.image) return;
        const a = document.createElement('a');
        a.href = post.url;
        a.target = '_blank';
        a.rel = 'noopener';
        a.className = 'ig-item';
        a.setAttribute('aria-label', post.caption || 'Instagram');
        const img = document.createElement('img');
        img.src = post.image;
        img.alt = post.caption ? post.caption.slice(0, 80) : '';
        img.loading = 'lazy';
        a.appendChild(img);
        grid.appendChild(a);
      });
      const follow = document.createElement('a');
      follow.href = data.profile;
      follow.target = '_blank';
      follow.rel = 'noopener';
      follow.className = 'ig-follow';
      follow.textContent = '@' + data.username + ' →';
      igFeed.appendChild(grid);
      igFeed.appendChild(follow);
    })
    .catch(() => {}); // Si falla, es queda el CTA estàtic
}

// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const menu   = document.getElementById('nav-menu');
if (toggle && menu) {
  toggle.addEventListener('click', () => {
    const open = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
  });
  document.addEventListener('click', e => {
    if (!toggle.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}
