/* 시계 */
function updateClock() {
  const d = new Date();
  document.getElementById("clock").textContent = d.toTimeString().slice(0, 5);
}
updateClock();
setInterval(updateClock, 60000);

/* 뒤로가기 */
document.getElementById("back-btn").addEventListener("click", (e) => {
  e.preventDefault();
  history.back();
});

/* 옵션 버튼 토글 */
document.querySelectorAll("#satisfaction .option").forEach((btn) =>
  btn.addEventListener("click", () => {
    setActive(btn, "satisfaction");
  })
);
document.querySelectorAll("#size .option").forEach((btn) =>
  btn.addEventListener("click", () => {
    setActive(btn, "size");
  })
);
function setActive(btn, groupId) {
  document
    .querySelectorAll("#" + groupId + " .option")
    .forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
}

/* 별점 */
const stars = document.querySelectorAll(".star");
stars.forEach((s) => {
  s.addEventListener("click", () => {
    const val = parseInt(s.dataset.val);
    stars.forEach((st) => {
      st.classList.toggle("filled", parseInt(st.dataset.val) <= val);
    });
  });
});

/* 글자수 카운터 */
const titleInput = document.getElementById("title");
const bodyInput = document.getElementById("body");
titleInput.addEventListener("input", () => {
  document.getElementById("title-count").textContent =
    titleInput.value.length + " / 30";
});
bodyInput.addEventListener("input", () => {
  document.getElementById("body-count").textContent =
    bodyInput.value.length + " / 300";
});

/* 네비 (review.html 동일) */
const STATIC_PATH = "../../static/products/productimg/";
const navItems = document.querySelectorAll(".bottom-nav .nav-item");
navItems.forEach((item) => {
  item.addEventListener("click", (e) => {
    e.preventDefault();
    navItems.forEach((n) => {
      const base = n.dataset.icon;
      n.classList.remove("active");
      n.querySelector("img").src = STATIC_PATH + base + ".png";
    });
    const base = item.dataset.icon;
    item.classList.add("active");
    item.querySelector("img").src = STATIC_PATH + base + "_red.png";
    if (base === "home") {
      window.location.href = "product.html";
    } else if (base === "user") {
      window.location.href = "mypage.html";
    }
  });
});
