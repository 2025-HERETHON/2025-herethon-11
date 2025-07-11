/* 시계 */
function updateClock() {
  const d = new Date();
  document.getElementById("clock").textContent = d.toTimeString().slice(0, 5);
}
updateClock();
setInterval(updateClock, 60000);

/* 더미 데이터로 카드 생성 (원한다면 AJAX로 대체) */
const wornProducts = [
  {
    img: "products/productimg/sample1.jpg",
    brand: "더잠",
    title: "이지핏 스퀘어 브라탑 · 팬티 세트",
    color: "블랙",
    size: "M",
    price: 23000,
  },
  {
    img: "products/productimg/sample1.jpg",
    brand: "더잠",
    title: "이지핏 스퀘어 브라탑 · 팬티 세트",
    color: "블랙",
    size: "M",
    price: 23000,
  },
  {
    img: "products/productimg/sample1.jpg",
    brand: "더잠",
    title: "이지핏 스퀘어 브라탑 · 팬티 세트",
    color: "블랙",
    size: "M",
    price: 23000,
  },
  {
    img: "products/productimg/sample1.jpg",
    brand: "더잠",
    title: "이지핏 스퀘어 브라탑 · 팬티 세트",
    color: "블랙",
    size: "M",
    price: 23000,
  },
  {
    img: "products/productimg/sample1.jpg",
    brand: "더잠",
    title: "이지핏 스퀘어 브라탑 · 팬티 세트",
    color: "블랙",
    size: "M",
    price: 23000,
  },
  {
    img: "products/productimg/sample1.jpg",
    brand: "더잠",
    title: "이지핏 스퀘어 브라탑 · 팬티 세트",
    color: "블랙",
    size: "M",
    price: 23000,
  },
];
// const makeCard = (p) => `
//         <div class="review-item">
//           <img src="${p.img}" alt="${p.title}" />
//           <div class="item-info">
//             <div class="title">[${p.brand}] ${p.title}</div>
//             <div class="opt">${p.color} · ${p.size}</div>
//             <div class="price">${p.price.toLocaleString()}원</div>
//           </div>
//           <a href="#" class="btn-write">리뷰 작성</a>
//         </div>`;
// document.getElementById("review-wrap").innerHTML = wornProducts
//   .map(makeCard)
//   .join("");

/* === 바텀 네비게이션 (product.html 동일 로직) === */
// const STATIC_PATH = "../../static/products/productimg/";
// const navItems = document.querySelectorAll(".bottom-nav .nav-item");
// navItems.forEach((item) => {
//   item.addEventListener("click", (e) => {
//     e.preventDefault();
//     /* 1. 모든 아이콘 & 글자 초기화 */
//     navItems.forEach((n) => {
//       const base = n.dataset.icon;
//       n.classList.remove("active");
//       n.querySelector("img").src = STATIC_PATH + base + ".png";
//     });
//     /* 2. 선택된 아이콘만 빨간색 + 살짝 확대 */
//     const base = item.dataset.icon;
//     item.classList.add("active");
//     item.querySelector("img").src = STATIC_PATH + base + "_red.png";

//     /* 3. 페이지 이동 or 기능 */
//     if (base === "home") {
//       window.location.href = "product.html"; // 홈
//     } else if (base === "user") {
//       window.location.href = "mypage.html"; // 마이페이지
//     } else {
//       // 리뷰 페이지 → 현재 페이지, 아무 동작 없음
//     }
//   });
// });

/* JS 맨 아래쪽 정도에 추가 */
// document.querySelectorAll(".btn-write").forEach((btn) => {
//   btn.addEventListener("click", (e) => {
//     e.preventDefault(); // a 태그 기본 이동 막고
//     window.location.href = "review_form.html"; // 작성 페이지로 GO!
//   });
// });
