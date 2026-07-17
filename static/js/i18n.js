/**
 * FOOTOP i18n — Système de traduction frontend
 * Détecte automatiquement la langue du système (navigator.language)
 * et persiste le choix dans localStorage pour toute la navigation.
 *
 * Langues supportées : fr (défaut), en, ar (RTL auto)
 * Usage dans le HTML : <span data-i18n="nav.home">Accueil</span>
 */

"use strict";

(function () {

  // ─── Dictionnaire de traductions ────────────────────────────────────────────
  const TRANSLATIONS = {

    fr: {
      // Navigation latérale
      "nav.home":         "Accueil",
      "nav.my_profile":   "Mon Profil",
      "nav.search":       "Rechercher Joueurs",
      "nav.search_short": "Rechercher",
      "nav.dashboard":    "Tableau de bord",
      "nav.logout":       "Déconnexion",
      "nav.login":        "Connexion",
      "nav.register":     "Inscription",

      // Footer pill
      "footer.offers":    "Offres",
      "footer.profile":   "Profil",
      "footer.edit":      "Modifier",
      "footer.logout":    "Déconnexion",
      "footer.dashboard": "Dashboard",

      // Sidebar infos
      "sidebar.welcome":  "Bienvenue sur FOOTOP",
      "sidebar.guest":    "Invité",
      "sidebar.copyright":"Tous droits réservés.",

      // Préloader
      "preloader.loading":"Chargement...",

      // Sélecteur de langue
      "lang.selector":    "Langue",
      "lang.fr":          "Français",
      "lang.en":          "English",
      "lang.ar":          "العربية",
    },

    en: {
      "nav.home":         "Home",
      "nav.my_profile":   "My Profile",
      "nav.search":       "Search Players",
      "nav.search_short": "Search",
      "nav.dashboard":    "Dashboard",
      "nav.logout":       "Logout",
      "nav.login":        "Login",
      "nav.register":     "Register",

      "footer.offers":    "Offers",
      "footer.profile":   "Profile",
      "footer.edit":      "Edit",
      "footer.logout":    "Logout",
      "footer.dashboard": "Dashboard",

      "sidebar.welcome":  "Welcome to FOOTOP",
      "sidebar.guest":    "Guest",
      "sidebar.copyright":"All rights reserved.",

      "preloader.loading":"Loading...",

      "lang.selector":    "Language",
      "lang.fr":          "Français",
      "lang.en":          "English",
      "lang.ar":          "العربية",
    },

    ar: {
      "nav.home":         "الرئيسية",
      "nav.my_profile":   "ملفي الشخصي",
      "nav.search":       "البحث عن لاعبين",
      "nav.search_short": "بحث",
      "nav.dashboard":    "لوحة التحكم",
      "nav.logout":       "تسجيل الخروج",
      "nav.login":        "تسجيل الدخول",
      "nav.register":     "إنشاء حساب",

      "footer.offers":    "العروض",
      "footer.profile":   "الملف",
      "footer.edit":      "تعديل",
      "footer.logout":    "خروج",
      "footer.dashboard": "لوحة التحكم",

      "sidebar.welcome":  "مرحباً بك في FOOTOP",
      "sidebar.guest":    "زائر",
      "sidebar.copyright":"جميع الحقوق محفوظة.",

      "preloader.loading":"جارٍ التحميل...",

      "lang.selector":    "اللغة",
      "lang.fr":          "Français",
      "lang.en":          "English",
      "lang.ar":          "العربية",
    },
  };

  // ─── Langues RTL ────────────────────────────────────────────────────────────
  const RTL_LANGS = ["ar"];

  // ─── Clé localStorage ───────────────────────────────────────────────────────
  const STORAGE_KEY = "footop_lang";

  // ─── Détecter la langue préférée ────────────────────────────────────────────
  function detectLanguage() {
    // 1. Priorité : choix sauvegardé par l'utilisateur
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && TRANSLATIONS[saved]) return saved;

    // 2. Langue du navigateur/système
    const navLang = (navigator.language || navigator.userLanguage || "fr")
      .toLowerCase()
      .split("-")[0]; // "fr-FR" → "fr", "ar-DZ" → "ar"

    if (TRANSLATIONS[navLang]) return navLang;

    // 3. Fallback français
    return "fr";
  }

  // ─── Appliquer la langue au DOM ─────────────────────────────────────────────
  function applyLanguage(lang) {
    const dict = TRANSLATIONS[lang] || TRANSLATIONS["fr"];

    // Attribut lang sur <html>
    document.documentElement.lang = lang;

    // Direction RTL/LTR (sync avec dark-rtl.js : on écrit data-dir)
    const dir = RTL_LANGS.includes(lang) ? "rtl" : "ltr";
    document.documentElement.setAttribute("dir", dir);
    // Compatibilité avec le switch RTL existant
    const rtlSwitch = document.getElementById("rtlSwitch");
    if (rtlSwitch) rtlSwitch.checked = (dir === "rtl");

    // Traduire tous les éléments marqués avec data-i18n
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      const key = el.getAttribute("data-i18n");
      if (dict[key] !== undefined) {
        // Si l'élément contient des enfants (icônes), ne pas écraser le HTML
        const hasChildren = el.children.length > 0;
        if (hasChildren) {
          // Mettre à jour uniquement le nœud texte final
          const textNodes = Array.from(el.childNodes).filter(n => n.nodeType === Node.TEXT_NODE);
          if (textNodes.length > 0) {
            textNodes[textNodes.length - 1].textContent = " " + dict[key];
          } else {
            el.insertAdjacentText("beforeend", " " + dict[key]);
          }
        } else {
          el.textContent = dict[key];
        }
      }
    });

    // Traduire les placeholders
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      const key = el.getAttribute("data-i18n-placeholder");
      if (dict[key] !== undefined) el.placeholder = dict[key];
    });

    // Traduire les aria-labels
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      const key = el.getAttribute("data-i18n-aria");
      if (dict[key] !== undefined) el.setAttribute("aria-label", dict[key]);
    });

    // Mettre à jour le sélecteur de langue (boutons actifs)
    document.querySelectorAll(".lang-switcher-btn").forEach(function (btn) {
      btn.classList.toggle("active", btn.dataset.lang === lang);
    });

    // Sauvegarder le choix
    localStorage.setItem(STORAGE_KEY, lang);
  }

  // ─── Créer le widget sélecteur de langue ─────────────────────────────────
  function createLangSwitcher() {
    // Vérifier si le widget existe déjà dans le HTML (via data-i18n-switcher)
    if (document.getElementById("footopLangSwitcher")) return;

    const container = document.createElement("div");
    container.id = "footopLangSwitcher";
    container.className = "footop-lang-switcher";
    container.setAttribute("role", "group");
    container.setAttribute("aria-label", "Language selector");

    const langs = [
      { code: "fr", label: "FR", flag: "🇫🇷" },
      { code: "en", label: "EN", flag: "🇬🇧" },
      { code: "ar", label: "AR", flag: "🇩🇿" },
    ];

    langs.forEach(function (l) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "lang-switcher-btn";
      btn.dataset.lang = l.code;
      btn.innerHTML = l.flag + " " + l.label;
      btn.title = TRANSLATIONS[l.code]["lang." + l.code] || l.label;
      btn.addEventListener("click", function () {
        applyLanguage(l.code);
      });
      container.appendChild(btn);
    });

    // Injecter dans le sidenav (avant copyright info), ou en bas de page
    const target = document.querySelector(".copyright-info") ||
                   document.querySelector(".sidenav-nav") ||
                   document.body;

    if (target && target.parentNode) {
      target.parentNode.insertBefore(container, target);
    } else {
      document.body.appendChild(container);
    }
  }

  // ─── Style inline du widget (léger) ─────────────────────────────────────
  function injectStyles() {
    if (document.getElementById("footop-i18n-styles")) return;
    const style = document.createElement("style");
    style.id = "footop-i18n-styles";
    style.textContent = `
      .footop-lang-switcher {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 12px 16px;
        margin: 8px 0;
      }
      .lang-switcher-btn {
        background: rgba(255,255,255,0.08);
        border: 1.5px solid rgba(255,255,255,0.18);
        color: rgba(255,255,255,0.75);
        border-radius: 20px;
        padding: 5px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.18s ease;
        letter-spacing: 0.02em;
      }
      .lang-switcher-btn:hover {
        background: rgba(255,255,255,0.18);
        color: #fff;
        border-color: rgba(255,255,255,0.4);
      }
      .lang-switcher-btn.active {
        background: #1db95b;
        border-color: #1db95b;
        color: #fff;
        box-shadow: 0 2px 8px rgba(29,185,91,0.35);
      }
      /* Ajustement RTL global */
      [dir="rtl"] .sidenav-nav a,
      [dir="rtl"] .footer-pill-item span {
        font-family: 'Segoe UI', 'Arial', sans-serif;
      }
    `;
    document.head.appendChild(style);
  }

  // ─── Initialisation ──────────────────────────────────────────────────────
  function init() {
    injectStyles();
    const lang = detectLanguage();
    createLangSwitcher();
    applyLanguage(lang);
  }

  // Lancer après le DOM
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Exposer globalement pour usage depuis d'autres scripts
  window.FOOTOP_I18N = {
    t: function (key) {
      const lang = localStorage.getItem(STORAGE_KEY) || "fr";
      const dict = TRANSLATIONS[lang] || TRANSLATIONS["fr"];
      return dict[key] || key;
    },
    setLang: applyLanguage,
    getLang: function () {
      return localStorage.getItem(STORAGE_KEY) || detectLanguage();
    },
  };

})();
