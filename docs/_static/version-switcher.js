(function () {
  "use strict";

  function detectCurrentVersion() {
    const segments = window.location.pathname.split("/").filter(Boolean);
    // GH pages serves at /<repo>/<version>/...
    // index 0 is the repo name, index 1 is the version slug.
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

  function linkifyBuildHash() {
    const copyright = document.querySelector(".copyright");
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

  function injectBrandBadge(current) {
    if (!current) {
      return;
    }
    const targets = [
      document.querySelector(".sidebar-brand-text"),
      document.querySelector(".mobile-header .header-center .brand"),
    ];
    targets.forEach(function (target) {
      if (!target || target.querySelector(".cc-version-badge")) {
        return;
      }
      const badge = document.createElement("span");
      badge.className = "cc-version-badge";
      badge.textContent = current;
      badge.setAttribute("title", "Documentation version " + current);
      target.appendChild(badge);
    });
  }

  function init() {
    const select = document.getElementById("cc-version-select");
    const current = detectCurrentVersion();
    injectBrandBadge(current);
    linkifyBuildHash();
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
