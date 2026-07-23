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

  // Hero / event background video autoplay
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

    const scrollByDir = (dir) => {
      const amount = Math.max(240, track.clientWidth * 0.8) * dir;
      track.scrollBy({ left: amount, behavior: 'smooth' });
    };

    carousel.querySelector('.photo-carousel-nav.prev')?.addEventListener('click', () => scrollByDir(-1));
    carousel.querySelector('.photo-carousel-nav.next')?.addEventListener('click', () => scrollByDir(1));

    items.forEach((item, index) => {
      item.addEventListener('click', () => openLightbox(sources, alts, index));
    });
  }

  // Agenda multi-image carousel (dots + drag on desktop) + lightbox
  document.querySelectorAll('.agenda-item-media-multi').forEach((scroller) => {
    const images = Array.from(scroller.querySelectorAll('img'));
    if (images.length < 2) return;

    const sources = images.map((img) => img.src);
    const alts = images.map((img) => img.alt || '');

    const wrap = document.createElement('div');
    wrap.className = 'agenda-media-wrap';
    scroller.parentNode.insertBefore(wrap, scroller);
    wrap.appendChild(scroller);

    const goTo = (index) => {
      const i = Math.max(0, Math.min(images.length - 1, index));
      scroller.scrollTo({ left: i * scroller.clientWidth, behavior: 'smooth' });
    };

    const currentIndex = () => {
      const step = Math.max(scroller.clientWidth, 1);
      return Math.min(images.length - 1, Math.round(scroller.scrollLeft / step));
    };

    const dots = document.createElement('div');
    dots.className = 'agenda-media-dots';
    images.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.setAttribute('aria-label', `Go to photo ${i + 1}`);
      if (i === 0) dot.classList.add('active');
      dot.addEventListener('click', () => goTo(i));
      dots.appendChild(dot);
    });
    wrap.appendChild(dots);

    const syncDots = () => {
      const index = currentIndex();
      dots.querySelectorAll('button').forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
      });
    };
    scroller.addEventListener('scroll', syncDots, { passive: true });

    // Desktop: click-drag to scroll; click (no drag) opens lightbox
    let isDown = false;
    let startX = 0;
    let startLeft = 0;
    let moved = false;
    let openedByPointer = false;

    scroller.addEventListener('pointerdown', (e) => {
      if (e.pointerType === 'touch') return;
      isDown = true;
      moved = false;
      openedByPointer = false;
      startX = e.clientX;
      startLeft = scroller.scrollLeft;
      scroller.classList.add('is-dragging');
      scroller.setPointerCapture(e.pointerId);
    });

    scroller.addEventListener('pointermove', (e) => {
      if (!isDown) return;
      const dx = e.clientX - startX;
      if (Math.abs(dx) > 3) moved = true;
      scroller.scrollLeft = startLeft - dx;
    });

    const endDrag = () => {
      if (!isDown) return;
      isDown = false;
      scroller.classList.remove('is-dragging');
      goTo(currentIndex());
      if (!moved) {
        openedByPointer = true;
        openLightbox(sources, alts, currentIndex());
      }
    };

    scroller.addEventListener('pointerup', endDrag);
    scroller.addEventListener('pointercancel', () => {
      if (!isDown) return;
      isDown = false;
      scroller.classList.remove('is-dragging');
      goTo(currentIndex());
    });

    // Touch tap opens lightbox
    scroller.addEventListener('click', () => {
      if (openedByPointer) {
        openedByPointer = false;
        return;
      }
      if (moved) {
        moved = false;
        return;
      }
      openLightbox(sources, alts, currentIndex());
    });
  });

  // Single agenda images: click to enlarge
  document.querySelectorAll('.agenda-item-media:not(.agenda-item-media-multi) img').forEach((img) => {
    img.addEventListener('click', () => {
      openLightbox([img.src], [img.alt || ''], 0);
    });
  });
});
