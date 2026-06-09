document.addEventListener("DOMContentLoaded", () => {
  const items = document.querySelectorAll(".fade-up");
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add("in-view");
    });
  }, { threshold: 0.12 });
  items.forEach((el) => observer.observe(el));
});
