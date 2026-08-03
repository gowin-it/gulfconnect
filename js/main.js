// Gulf Connect � Shared JavaScript

document.addEventListener('DOMContentLoaded', () => {
  // Header: transparent on homepage only, solid elsewhere
  const header = document.querySelector('.site-header');
  if (header) {
    const isHome = document.body.classList.contains('home');
    const updateHeader = () => {
      if (isHome) {
        header.classList.toggle('scrolled', window.scrollY > 40);
      } else {
        header.classList.toggle('scrolled', window.scrollY > 10);
      }
    };
    updateHeader();
    window.addEventListener('scroll', updateHeader, { passive: true });
  }

  // Mobile menu toggle
  const toggle = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('.nav-mobile');
  if (toggle && mobileNav) {
    toggle.addEventListener('click', () => {
      mobileNav.classList.toggle('open');
      toggle.classList.toggle('active');
    });

    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        toggle.classList.remove('active');
      });
    });
  }

  // Event page section nav highlight
  const eventNav = document.querySelector('.event-nav');
  if (eventNav) {
    const links = eventNav.querySelectorAll('a');
    const sections = Array.from(links).map(link => {
      const id = link.getAttribute('href').slice(1);
      return document.getElementById(id);
    }).filter(Boolean);

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          links.forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === '#' + entry.target.id);
          });
        }
      });
    }, { rootMargin: '-40% 0px -50% 0px' });

    sections.forEach(section => observer.observe(section));
  }

  // Hero / event / media video autoplay
  document.querySelectorAll('.hero-video, .event-hero-video').forEach((heroVideo) => {
    heroVideo.muted = true;
    heroVideo.defaultMuted = true;
    heroVideo.setAttribute('playsinline', '');
    heroVideo.setAttribute('webkit-playsinline', '');

    const tryPlay = () => {
      const playPromise = heroVideo.play();
      if (playPromise && typeof playPromise.catch === 'function') {
        playPromise.catch(() => {});
      }
    };

    tryPlay();
    heroVideo.addEventListener('loadeddata', tryPlay, { once: true });
    heroVideo.addEventListener('canplay', tryPlay, { once: true });
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) tryPlay();
    });
    window.addEventListener('pageshow', tryPlay);
  });

  // Media section: discourage video download via context menu
  document.querySelectorAll('.media-video').forEach((video) => {
    video.addEventListener('contextmenu', (e) => e.preventDefault());
  });

  // Shared lightbox for Media gallery + Agenda photos
  const lightbox = document.getElementById('photo-lightbox');
  let lightboxSources = [];
  let lightboxAlts = [];
  let lightboxCurrent = 0;

  const openLightbox = (sources, alts, index) => {
    if (!lightbox || !sources.length) return;
    lightboxSources = sources;
    lightboxAlts = alts;
    lightboxCurrent = ((index % sources.length) + sources.length) % sources.length;
    const lightboxImg = lightbox.querySelector('.lightbox-image');
    lightboxImg.src = lightboxSources[lightboxCurrent];
    lightboxImg.alt = lightboxAlts[lightboxCurrent] || '';
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
  };

  const closeLightbox = () => {
    if (!lightbox) return;
    lightbox.hidden = true;
    lightbox.querySelector('.lightbox-image')?.removeAttribute('src');
    document.body.style.overflow = '';
  };

  const stepLightbox = (dir) => {
    if (!lightboxSources.length) return;
    openLightbox(lightboxSources, lightboxAlts, lightboxCurrent + dir);
  };

  if (lightbox) {
    lightbox.querySelector('.lightbox-close')?.addEventListener('click', closeLightbox);
    lightbox.querySelector('.lightbox-nav.prev')?.addEventListener('click', () => stepLightbox(-1));
    lightbox.querySelector('.lightbox-nav.next')?.addEventListener('click', () => stepLightbox(1));
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', (e) => {
      if (lightbox.hidden) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') stepLightbox(-1);
      if (e.key === 'ArrowRight') stepLightbox(1);
    });
  }

  // Media photo carousel
  const carousel = document.querySelector('.photo-carousel');
  if (carousel) {
    const track = carousel.querySelector('.photo-carousel-track');
    const items = Array.from(carousel.querySelectorAll('.photo-carousel-item'));
    const sources = items.map((item) => item.querySelector('img')?.src).filter(Boolean);
    const alts = items.map((item) => item.querySelector('img')?.alt || '');

    items.forEach((item, index) => {
      item.addEventListener('click', () => openLightbox(sources, alts, index));
    });

    if (carousel.classList.contains('photo-carousel-auto') && track && items.length > 1) {
      let paused = false;
      let rafId = 0;
      let lastTs = 0;
      const speed = 320; // px per second

      carousel.addEventListener('mouseenter', () => { paused = true; });
      carousel.addEventListener('mouseleave', () => { paused = false; lastTs = 0; });
      carousel.addEventListener('touchstart', () => { paused = true; }, { passive: true });
      carousel.addEventListener('touchend', () => {
        window.setTimeout(() => { paused = false; lastTs = 0; }, 2500);
      }, { passive: true });

      const tick = (ts) => {
        if (!paused && track.scrollWidth > track.clientWidth) {
          if (lastTs) {
            const delta = (ts - lastTs) / 1000;
            track.scrollLeft += speed * delta;
      
            const loopPoint = track.scrollWidth - track.clientWidth;
            if (track.scrollLeft >= loopPoint - 1) {
              track.scrollLeft = 0;
            }
          }
          lastTs = ts;
        } else  {
          lastTs = ts;
        }
        rafId = requestAnimationFrame(tick);
      };
      rafId = requestAnimationFrame(tick);
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) cancelAnimationFrame(rafId);
        else {
          lastTs = 0;
          rafId = requestAnimationFrame(tick);
        }
      });
    } else {
      const scrollByDir = (dir) => {
        const amount = Math.max(240, track.clientWidth * 0.8) * dir;
        track.scrollBy({ left: amount, behavior: 'smooth' });
      };
      carousel.querySelector('.photo-carousel-nav.prev')?.addEventListener('click', () => scrollByDir(-1));
      carousel.querySelector('.photo-carousel-nav.next')?.addEventListener('click', () => scrollByDir(1));
    }
  }

  // Agenda images: click to enlarge
  document.querySelectorAll('.agenda-item-media img').forEach((img) => {
    img.addEventListener('click', () => {
      openLightbox([img.src], [img.alt || ''], 0);
    });
  });
});
