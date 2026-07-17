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

      "home_title": "Élevez Votre ",
      "home_title_bold": "Carrière",
      "home_subtitle": "Combler le fossé entre talent et opportunité. La plateforme ultime pour que les joueurs se fassent repérer, que les agents trouvent des talents et que les entraîneurs construisent des équipes gagnantes.",
      "home_start": "Commencer",
      "home_login": "Se Connecter",
      
      "login_title": "Bienvenue",
      "login_subtitle": "Connectez-vous à votre compte FOOTOP",
      "login_identifier_placeholder": "Nom d'utilisateur, email ou téléphone",
      "login_password_placeholder": "Mot de passe",
      "login_forgot": "Mot de passe oublié ?",
      "login_btn": "Se connecter",
      "login_no_account": "Pas encore de compte ?",
      "login_register_link": "S'inscrire",
      
      "reg_title": "Choisissez votre Rôle",
      "reg_subtitle": "Sélectionnez le type de compte qui correspond à votre profil",
      "reg_badge_popular": "Populaire",
      "reg_badge_premium": "Premium",
      "reg_player": "Joueur",
      "reg_player_desc": "Créez votre profil et soyez découvert par des clubs",
      "reg_coach": "Entraîneur",
      "reg_coach_desc": "Présentez votre expérience et découvrez des talents",
      "reg_club": "Club",
      "reg_club_desc": "Recherchez les meilleurs talents pour votre équipe",
      "reg_agent": "Agent",
      "reg_agent_desc": "Gérez votre portefeuille de talents professionnels",
      "reg_continue": "Continuer",
      "reg_already": "Déjà inscrit ?",
      "reg_login_link": "Se connecter",
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

      "home_title": "Elevate Your ",
      "home_title_bold": "Career",
      "home_subtitle": "Bridging the gap between talent and opportunity. The ultimate platform for players to get scouted, agents to find talent, and coaches to build winning teams.",
      "home_start": "Get Started",
      "home_login": "Sign In",
      
      "login_title": "Welcome Back",
      "login_subtitle": "Sign in to your FOOTOP account",
      "login_identifier_placeholder": "Username, email or phone",
      "login_password_placeholder": "Password",
      "login_forgot": "Forgot password?",
      "login_btn": "Sign In",
      "login_no_account": "No account yet?",
      "login_register_link": "Register",
      
      "reg_title": "Choose Your Role",
      "reg_subtitle": "Select the account type that fits your profile",
      "reg_badge_popular": "Popular",
      "reg_badge_premium": "Premium",
      "reg_player": "Player",
      "reg_player_desc": "Create your profile and get discovered by clubs",
      "reg_coach": "Coach",
      "reg_coach_desc": "Showcase your experience and discover talents",
      "reg_club": "Club",
      "reg_club_desc": "Search for the best talents for your team",
      "reg_agent": "Agent",
      "reg_agent_desc": "Manage your professional talent portfolio",
      "reg_continue": "Continue",
      "reg_already": "Already registered?",
      "reg_login_link": "Sign In",
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

      "home_title": "ارتقِ بمسيرتك ",
      "home_title_bold": "المهنية",
      "home_subtitle": "جسر الهوة بين الموهبة والفرصة. المنصّة المثلى لكي يُكتشف اللاعبون ويجد الوكلاء المواهب ويبني المدرّبون فرقاً متميزة.",
      "home_start": "ابدأ الآن",
      "home_login": "تسجيل الدخول",
      
      "login_title": "مرحباً بك",
      "login_subtitle": "سجّل الدخول إلى حساب FOOTOP",
      "login_identifier_placeholder": "اسم المستخدم أو البريد أو الهاتف",
      "login_password_placeholder": "كلمة المرور",
      "login_forgot": "نسيت كلمة المرور؟",
      "login_btn": "تسجيل الدخول",
      "login_no_account": "ليس لديك حساب؟",
      "login_register_link": "إنشاء حساب",
      
      "reg_title": "اختر دورك",
      "reg_subtitle": "حدد نوع الحساب المناسب لك",
      "reg_badge_popular": "شائع",
      "reg_badge_premium": "مميز",
      "reg_player": "لاعب",
      "reg_player_desc": "أنشئ ملفك واجعل الأندية تكتشفك",
      "reg_coach": "مدرب",
      "reg_coach_desc": "اعرض خبرتك واكتشف المواهب",
      "reg_club": "نادي",
      "reg_club_desc": "ابحث عن أفضل المواهب لفريقك",
      "reg_agent": "وكيل",
      "reg_agent_desc": "أدر محفظتك من المواهب الاحترافية",
      "reg_continue": "متابعة",
      "reg_already": "مسجّل مسبقاً؟",
      "reg_login_link": "تسجيل الدخول",
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
    // Si un widget ".lang-switcher" existe déjà, on l'utilise
    const existingSwitcher = document.querySelector(".lang-switcher");
    if (existingSwitcher) {
      existingSwitcher.querySelectorAll('.lang-btn').forEach(function(btn) {
        // Enlever onclick s'il existe pour éviter le doublon
        btn.removeAttribute('onclick');
        // Cloner le bouton pour nettoyer les anciens event listeners
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);
        newBtn.addEventListener("click", function () {
          applyLanguage(newBtn.dataset.lang);
        });
      });
      return;
    }

    // Vérifier si le widget généré existe déjà dans le HTML
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
