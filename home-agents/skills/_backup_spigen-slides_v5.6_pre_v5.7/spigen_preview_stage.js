(function() {
  const STORAGE_KEY_PREFIX = 'spigen-preview-slide-';

  class SpigenDeckStage extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
      this._currentSlide = 0;
      this._slides = [];
      this._storageKey = STORAGE_KEY_PREFIX + (location.pathname || 'default');
    }

    connectedCallback() {
      this._width = parseInt(this.getAttribute('width')) || 720;
      this._height = parseInt(this.getAttribute('height')) || 405;
      this._render();

      const init = () => {
        this._collectSlides();
        this._setupEventListeners();
        this._restoreSlide();
        this._updateDisplay();
      };

      if (this.ownerDocument.readyState === 'loading') {
        this.ownerDocument.addEventListener('DOMContentLoaded', init, { once: true });
      } else {
        requestAnimationFrame(init);
      }
    }

    _render() {
      this.shadowRoot.innerHTML = `
        <style>
          :host {
            display: block;
            position: fixed;
            inset: 0;
            background: #0a0a0a;
            overflow: hidden;
            font-family: 'Noto Sans KR', system-ui, sans-serif;
          }
          .stage {
            position: absolute;
            top: 50%;
            left: 50%;
            transform-origin: top left;
            will-change: transform;
            background: #000;
            border: 1px solid #303030;
            box-shadow: 0 12px 48px rgba(0,0,0,0.7);
          }
          .slide-wrapper {
            width: 100%;
            height: 100%;
            position: relative;
          }
          ::slotted(section) {
            display: none;
            width: 100%;
            height: 100%;
            position: absolute;
            inset: 0;
            overflow: hidden;
          }
          ::slotted(section.active) {
            display: block;
          }
          .counter {
            position: fixed;
            right: 20px;
            bottom: 20px;
            background: rgba(0, 0, 0, 0.65);
            color: #fff;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-variant-numeric: tabular-nums;
            opacity: 0.72;
            z-index: 100;
          }
          .nav-zone {
            position: fixed;
            top: 0;
            bottom: 0;
            width: 15%;
            cursor: pointer;
            z-index: 50;
          }
          .nav-zone.left { left: 0; }
          .nav-zone.right { right: 0; }
          .nav-hint {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 44px;
            height: 44px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            color: rgba(255,255,255,0.65);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            opacity: 0;
            transition: opacity 0.2s;
            user-select: none;
          }
          .nav-zone.left .nav-hint { left: 20px; }
          .nav-zone.right .nav-hint { right: 20px; }
          .nav-zone:hover .nav-hint { opacity: 1; }
          @media print {
            :host {
              position: static;
              background: #fff;
            }
            .counter, .nav-zone { display: none !important; }
            .stage {
              position: static;
              transform: none !important;
              box-shadow: none;
              border: none;
              page-break-after: always;
            }
            ::slotted(section) {
              display: block !important;
              position: relative !important;
              page-break-after: always;
            }
          }
        </style>
        <div class="stage" id="stage" style="width:${this._width}px;height:${this._height}px;">
          <div class="slide-wrapper">
            <slot></slot>
          </div>
        </div>
        <div class="nav-zone left" id="navLeft"><div class="nav-hint">‹</div></div>
        <div class="nav-zone right" id="navRight"><div class="nav-hint">›</div></div>
        <div class="counter" id="counter">1 / 1</div>
      `;
    }

    _collectSlides() {
      this._slides = Array.from(this.querySelectorAll(':scope > section'));
      this._slides.forEach((slide, idx) => {
        if (!slide.hasAttribute('data-screen-label')) {
          slide.setAttribute('data-screen-label', String(idx + 1).padStart(2, '0'));
        }
      });
    }

    _setupEventListeners() {
      window.addEventListener('resize', () => this._updateScale());
      document.addEventListener('keydown', (e) => {
        if (e.target.matches('input, textarea, [contenteditable]')) return;
        switch (e.key) {
          case 'ArrowRight':
          case ' ':
          case 'PageDown':
            e.preventDefault();
            this.next();
            break;
          case 'ArrowLeft':
          case 'PageUp':
            e.preventDefault();
            this.prev();
            break;
          case 'Home':
            e.preventDefault();
            this.goTo(0);
            break;
          case 'End':
            e.preventDefault();
            this.goTo(this._slides.length - 1);
            break;
        }
      });
      this.shadowRoot.getElementById('navLeft').addEventListener('click', () => this.prev());
      this.shadowRoot.getElementById('navRight').addEventListener('click', () => this.next());
      window.addEventListener('hashchange', () => this._handleHash());
      if (location.hash) setTimeout(() => this._handleHash(), 0);
    }

    _restoreSlide() {
      const hash = this._hashIndex();
      const saved = parseInt(localStorage.getItem(this._storageKey) || '0', 10);
      const idx = Number.isFinite(hash) ? hash : (Number.isFinite(saved) ? saved : 0);
      this.goTo(idx, { persist: false, updateHash: false });
    }

    _hashIndex() {
      const m = String(location.hash || '').match(/slide-(\d+)/);
      return m ? Math.max(0, parseInt(m[1], 10) - 1) : null;
    }

    _handleHash() {
      const idx = this._hashIndex();
      if (idx !== null) this.goTo(idx, { persist: true, updateHash: false });
    }

    _updateScale() {
      const stage = this.shadowRoot.getElementById('stage');
      const scale = Math.min(window.innerWidth / this._width, window.innerHeight / this._height);
      const x = (window.innerWidth - this._width * scale) / 2;
      const y = (window.innerHeight - this._height * scale) / 2;
      stage.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
    }

    _updateDisplay() {
      this._slides.forEach((slide, idx) => slide.classList.toggle('active', idx === this._currentSlide));
      const counter = this.shadowRoot.getElementById('counter');
      counter.textContent = `${this._currentSlide + 1} / ${this._slides.length}`;
      this._updateScale();
    }

    goTo(index, options = {}) {
      if (!this._slides.length) return;
      const { persist = true, updateHash = true } = options;
      this._currentSlide = Math.max(0, Math.min(index, this._slides.length - 1));
      if (persist) localStorage.setItem(this._storageKey, String(this._currentSlide));
      if (updateHash) history.replaceState(null, '', `#slide-${this._currentSlide + 1}`);
      this._updateDisplay();
    }

    next() { this.goTo(this._currentSlide + 1); }
    prev() { this.goTo(this._currentSlide - 1); }
  }

  if (!customElements.get('spigen-deck-stage')) {
    customElements.define('spigen-deck-stage', SpigenDeckStage);
  }
})();
