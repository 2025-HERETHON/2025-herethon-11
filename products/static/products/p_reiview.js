/* 시계 */
const setClock = () =>
  (document.getElementById("clock").textContent = new Date()
    .toTimeString()
    .slice(0, 5));
setClock();
setInterval(setClock, 60000);

/* 찜 하트 */
document.getElementById("wish").onclick = (e) =>
  e.currentTarget.classList.toggle("on");

/* 좋아요 */
document.addEventListener("DOMContentLoaded", () => {
  /* 모든 따봉 버튼 찾기 */
  document.querySelectorAll(".like-btn").forEach((btn) => {
    /* 초기 변수 세팅 */
    const img = btn.querySelector(".thumb");
    const cntEl = btn.querySelector(".cnt");
    const base = parseInt(btn.dataset.base, 10); // data-base 값
    let liked = false;

    /* 클릭 이벤트! */
    btn.addEventListener("click", () => {
      liked = !liked; // 토글

      /* 아이콘 교체 */
      img.src = liked
        ? "../../static/products/productimg/thumb_red.png" // ON 이미지
        : "../../static/products/productimg/thumb.png"; // OFF 이미지

      /* 숫자 증감 */
      cntEl.textContent = base + (liked ? 1 : 0);
    });
  });
});

/* 체형정보 토글 */
const tgl = document.querySelector(".body-toggle");
const det = document.querySelector(".body-detail");
tgl.onclick = () => {
  const open = det.style.display === "block";
  det.style.display = open ? "none" : "block";
  tgl.textContent = `체형정보 ${open ? "보기 ▾" : "접기 ▴"}`;
};
