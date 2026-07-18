/**
 * Holistyczny Broker — Global Language Switcher
 * Reads translations.json, applies to all [data-i18n] elements.
 * Language preference persisted in localStorage.
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'hb_lang';
  const DEFAULT_LANG = 'pl';
  let translations = {};
  let currentLang = localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG;

  // ── Core: apply translations to the page ─────────────────────────────────
  function applyTranslations(lang) {
    currentLang = lang;
    localStorage.setItem(STORAGE_KEY, lang);
    document.documentElement.setAttribute('lang', lang);

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      const key = el.getAttribute('data-i18n');
      const text = getNestedValue(translations[lang], key);
      if (text !== undefined) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.setAttribute('placeholder', text);
        } else {
          el.innerHTML = text;
        }
      }
    });

    document.querySelectorAll('[data-i18n-title]').forEach(function (el) {
      const key = el.getAttribute('data-i18n-title');
      const text = getNestedValue(translations[lang], key);
      if (text !== undefined) el.setAttribute('title', text);
    });

    document.querySelectorAll('[data-i18n-meta]').forEach(function (el) {
      const key = el.getAttribute('data-i18n-meta');
      const text = getNestedValue(translations[lang], key);
      if (text !== undefined) el.setAttribute('content', text);
    });

    // Update page <title>
    const titleKey = document.body.getAttribute('data-page-title-i18n');
    if (titleKey) {
      const titleText = getNestedValue(translations[lang], titleKey);
      if (titleText) document.title = titleText;
    }

    updateSwitcherUI(lang);
  }

  function getNestedValue(obj, keyPath) {
    if (!obj || !keyPath) return undefined;
    return keyPath.split('.').reduce(function (acc, k) {
      return acc && acc[k] !== undefined ? acc[k] : undefined;
    }, obj);
  }

  // ── Switcher UI ───────────────────────────────────────────────────────────
  function updateSwitcherUI(lang) {
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      const btnLang = btn.getAttribute('data-lang');
      if (btnLang === lang) {
        btn.classList.add('lang-btn--active');
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.classList.remove('lang-btn--active');
        btn.setAttribute('aria-pressed', 'false');
      }
    });
  }

  // ── Public API ────────────────────────────────────────────────────────────
  window.setLang = function (lang) {
    if (translations[lang]) {
      applyTranslations(lang);
    }
  };

  window.getCurrentLang = function () {
    return currentLang;
  };

  // ── Bootstrap ─────────────────────────────────────────────────────────────
  function init() {
    // Resolve path to translations.json relative to current page location
    const scriptTags = document.getElementsByTagName('script');
    let basePath = '';
    for (let i = 0; i < scriptTags.length; i++) {
      const src = scriptTags[i].getAttribute('src') || '';
      if (src.includes('lang-switcher.js')) {
        basePath = src.replace('lang-switcher.js', '');
        break;
      }
    }

    fetch(basePath + 'translations.json?v=' + Date.now())
      .then(function (r) { return r.json(); })
      .then(function (data) {
        translations = data;
        applyTranslations(currentLang);
      })
      .catch(function (err) {
        console.warn('[LangSwitcher] Could not load translations.json:', err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
