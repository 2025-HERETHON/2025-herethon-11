/* 시계 */
const setClock = () => {
  document.getElementById("clock").textContent = new Date()
    .toTimeString()
    .slice(0, 5);
};
setClock();
setInterval(setClock, 60000);

/* 캐러셀 */
const imgs = [...document.querySelectorAll("#carousel img")];
const dots = [...document.querySelectorAll("#dots .dot")];
dots.forEach((dot) => {
  dot.addEventListener("click", () => {
    const idx = +dot.dataset.idx;
    imgs.forEach((img, i) => img.classList.toggle("hidden", i !== idx));
    dots.forEach((d) => d.classList.toggle("active", d === dot));
  });
});

/* 찜 하트 */
document.getElementById("wish").addEventListener("click", (e) => {
  e.currentTarget.classList.toggle("on");
});

/* 드롭다운 */
document.querySelectorAll(".dropdown").forEach((dd) => {
  const btn = dd.querySelector(".drop-btn");
  const list = dd.querySelector(".option-list");
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    dd.classList.toggle("open");
  });
  list.querySelectorAll("button").forEach((opt) => {
    opt.addEventListener("click", () => {
      btn.textContent = opt.textContent;
      dd.classList.remove("open");
    });
  });
});
document.addEventListener("click", () =>
  document
    .querySelectorAll(".dropdown.open")
    .forEach((d) => d.classList.remove("open"))
);

const hasSize = false; // ← 서버 데이터로 판단

if (!hasSize) {
  document.getElementById("optionBox").style.display = "none";
} else {
  document.getElementById("prodDesc").style.display = "none";
}

const isFreeSize = new URLSearchParams(location.search).get("free") === "1";

const prodDesc = document.getElementById("prodDesc");
const dropdowns = document.querySelectorAll(".options .dropdown");

if (isFreeSize) {
  prodDesc.style.display = "block"; // 안내문 보여줌
  dropdowns[1].style.display = "none"; // 두 번째 드롭다운(사이즈) 숨김!
} else {
  prodDesc.style.display = "none";
  dropdowns[1].style.display = "flex"; // 다시 보여줌!
}
