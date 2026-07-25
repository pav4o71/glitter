/**
 * Glitter Professional Salon
 * Small, dependency-free enhancements. All essential content remains available
 * when JavaScript is disabled.
 */

document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector("[data-header]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const navigation = document.querySelector("[data-navigation]");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  const closeMenu = (returnFocus = false) => {
    if (!menuToggle || !navigation) return;

    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Open navigation menu");
    navigation.classList.remove("is-open");

    if (returnFocus) {
      menuToggle.focus();
    }
  };

  if (menuToggle && navigation) {
    menuToggle.addEventListener("click", () => {
      const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
      menuToggle.setAttribute("aria-expanded", String(!isOpen));
      menuToggle.setAttribute(
        "aria-label",
        isOpen ? "Open navigation menu" : "Close navigation menu"
      );
      navigation.classList.toggle("is-open", !isOpen);
    });

    navigation.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => closeMenu());
    });

    document.addEventListener("click", (event) => {
      if (
        navigation.classList.contains("is-open") &&
        !navigation.contains(event.target) &&
        !menuToggle.contains(event.target)
      ) {
        closeMenu();
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && navigation.classList.contains("is-open")) {
        closeMenu(true);
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth >= 960) {
        closeMenu();
      }
    });
  }

  const updateHeader = () => {
    if (header) {
      header.classList.toggle("is-scrolled", window.scrollY > 16);
    }
  };

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  document.querySelectorAll("[data-current-year]").forEach((element) => {
    element.textContent = String(new Date().getFullYear());
  });

  const filterButtons = Array.from(document.querySelectorAll("[data-filter]"));
  const categories = Array.from(document.querySelectorAll("[data-category]"));

  if (filterButtons.length && categories.length) {
    const announcement = document.createElement("p");
    announcement.className = "visually-hidden";
    announcement.setAttribute("aria-live", "polite");
    document.querySelector(".service-controls")?.append(announcement);
    let activeFilter = null;

    const applyFilter = (filter, announce = true) => {
      const validFilter =
        filter === "all" || categories.some((item) => item.dataset.category === filter)
          ? filter
          : "all";
      activeFilter = validFilter;

      filterButtons.forEach((button) => {
        const isActive = button.dataset.filter === validFilter;
        button.classList.toggle("is-active", isActive);
        button.setAttribute("aria-pressed", String(isActive));
      });

      categories.forEach((category) => {
        category.hidden =
          validFilter !== "all" && category.dataset.category !== validFilter;
      });

      if (announce) {
        const activeButton = filterButtons.find(
          (button) => button.dataset.filter === validFilter
        );
        announcement.textContent = `${activeButton?.textContent.trim() || "All services"} displayed.`;
      }
    };

    const filterFromLocation = () => {
      const locationHash = window.location.hash.slice(1);
      return categories.some((category) => category.id === locationHash)
        ? locationHash
        : "all";
    };

    const updateFilterUrl = (filter) => {
      const nextHash = filter === "all" ? "#service-menu" : `#${filter}`;
      if (window.location.hash !== nextHash) {
        window.history.pushState(null, "", nextHash);
      }
    };

    const syncFilterFromLocation = () => {
      const locationFilter = filterFromLocation();
      if (locationFilter !== activeFilter) {
        applyFilter(locationFilter);
      }
    };

    filterButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const nextFilter = button.dataset.filter || "all";
        updateFilterUrl(nextFilter);
        applyFilter(nextFilter);
      });
    });

    window.addEventListener("hashchange", syncFilterFromLocation);
    window.addEventListener("popstate", syncFilterFromLocation);
    applyFilter(filterFromLocation(), false);
  }

  const revealItems = document.querySelectorAll(".reveal");

  if (
    !revealItems.length ||
    reducedMotion.matches ||
    !("IntersectionObserver" in window)
  ) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  } else {
    const observer = new IntersectionObserver(
      (entries, currentObserver) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            currentObserver.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.08,
        rootMargin: "0px 0px 48px"
      }
    );

    revealItems.forEach((item) => observer.observe(item));
  }
});
