(function () {
  "use strict";

  function detectTheme() {
    if (document.querySelector(".sidebar-drawer")) return "furo";
    if (document.querySelector(".wy-side-nav-search")) return "rtd";
    return null;
  }

  function detectCurrentVersion() {
    const segments = window.location.pathname.split("/").filter(Boolean);
    if (segments.length >= 2) {
      return segments[1];
    }
    return "";
  }

  function buildVersionsUrl() {
    const segments = window.location.pathname.split("/").filter(Boolean);
    if (segments.length === 0) {
      return "/versions.json";
    }
    return "/" + segments[0] + "/versions.json";
  }

  function navigateTo(slug) {
    const segments = window.location.pathname.split("/").filter(Boolean);
    if (segments.length < 1) {
      window.location.pathname = "/" + slug + "/";
      return;
    }
    const tail = segments.slice(2).join("/");
    const suffix = tail ? "/" + tail : "/";
    window.location.pathname = "/" + segments[0] + "/" + slug + suffix;
  }

  function ensureDropdownExists(theme) {
    if (document.getElementById("cc-version-select")) return;
    if (theme !== "rtd") return;
    const target = document.querySelector(".wy-side-nav-search");
    if (!target) return;
    const wrap = document.createElement("div");
    wrap.className = "sidebar-version-selector sidebar-version-selector--rtd";
    const label = document.createElement("label");
    label.htmlFor = "cc-version-select";
    label.className = "sidebar-version-selector__label";
    label.textContent = "Version";
    const select = document.createElement("select");
    select.id = "cc-version-select";
    select.className = "sidebar-version-selector__select";
    select.setAttribute("aria-label", "Select documentation version");
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "loading…";
    select.appendChild(placeholder);
    wrap.append(label, select);
    target.appendChild(wrap);
  }

  function populate(select, entries, current) {
    select.innerHTML = "";
    let matched = false;
    entries.forEach(function (entry) {
      const option = document.createElement("option");
      option.value = entry.name;
      option.textContent = entry.name;
      if (entry.name === current) {
        option.selected = true;
        matched = true;
      }
      select.appendChild(option);
    });
    if (!matched && current) {
      const option = document.createElement("option");
      option.value = current;
      option.textContent = current + " (current)";
      option.selected = true;
      select.insertBefore(option, select.firstChild);
    }
  }

  function deriveRepoUrl() {
    const host = window.location.hostname || "";
    const ghIoMatch = host.match(/^([^.]+)\.github\.io$/);
    const segments = window.location.pathname.split("/").filter(Boolean);
    if (!ghIoMatch || segments.length === 0) {
      return null;
    }
    return "https://github.com/" + ghIoMatch[1] + "/" + segments[0];
  }

  function findCopyrightEl() {
    const selectors = [
      ".copyright",
      "footer .copyright",
      "footer p",
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el && /build [a-f0-9]{7,40}/.test(el.textContent)) {
        return el;
      }
    }
    return null;
  }

  function linkifyBuildHash() {
    const copyright = findCopyrightEl();
    if (!copyright) {
      return;
    }
    const repoUrl = deriveRepoUrl();
    if (!repoUrl) {
      return;
    }
    const text = copyright.textContent;
    const match = text.match(/build ([a-f0-9]{7,40})/);
    if (!match) {
      return;
    }
    const sha = match[1];
    const link = document.createElement("a");
    link.href = repoUrl + "/commit/" + sha;
    link.textContent = sha;
    link.rel = "noopener";
    link.target = "_blank";
    link.className = "cc-build-commit";
    copyright.innerHTML = "";
    copyright.append(
      document.createTextNode(text.slice(0, match.index)),
      document.createTextNode("build "),
      link,
      document.createTextNode(text.slice(match.index + match[0].length))
    );
  }

  function injectBrandBadge(theme, current) {
    if (!current) return;
    let targets = [];
    if (theme === "furo") {
      targets = [
        document.querySelector(".sidebar-brand-text"),
        document.querySelector(".mobile-header .header-center .brand"),
      ];
    } else if (theme === "rtd") {
      targets = [
        document.querySelector(".wy-side-nav-search > a"),
        document.querySelector(".wy-nav-top > a"),
      ];
    }
    targets.forEach(function (target) {
      if (!target || target.querySelector(".cc-version-badge")) return;
      const badge = document.createElement("span");
      badge.className = "cc-version-badge";
      badge.textContent = current;
      badge.setAttribute("title", "Documentation version " + current);
      target.appendChild(badge);
    });
  }

  function init() {
    const theme = detectTheme();
    const current = detectCurrentVersion();
    ensureDropdownExists(theme);
    injectBrandBadge(theme, current);
    linkifyBuildHash();
    const select = document.getElementById("cc-version-select");
    if (!select) {
      return;
    }
    fetch(buildVersionsUrl(), { cache: "no-store" })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("versions.json HTTP " + response.status);
        }
        return response.json();
      })
      .then(function (entries) {
        populate(select, entries, current);
        select.addEventListener("change", function () {
          if (select.value) {
            navigateTo(select.value);
          }
        });
      })
      .catch(function (err) {
        console.warn("version-switcher: failed to load versions.json", err);
        select.innerHTML = "";
        const option = document.createElement("option");
        option.textContent = current || "current";
        option.selected = true;
        select.appendChild(option);
        select.disabled = true;
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
