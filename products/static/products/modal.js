(function () {
  const modal = document.getElementById("wear-modal");
  const sheet = document.getElementById("wear-sheet");
  const colorEl = document.getElementById("wear-color");
  const sizeEl = document.getElementById("wear-size");

  /* ① 열기 : .wear 아이콘 클릭 */
  document.body.addEventListener("click", (e) => {
    const wear = e.target.closest(".wear");
    if (!wear) return;

    /* data-* 값 가져오기 */
    const colors = (wear.dataset.colors || "블랙").split(",");
    const sizes = (wear.dataset.sizes || "Free").split(",");
    const pid = wear.dataset.id;

    /* 드롭다운 채우기 */
    colorEl.innerHTML = colors
      .map((c) => `<option>${c.trim()}</option>`)
      .join("");
    sizeEl.innerHTML = sizes
      .map((s) => `<option>${s.trim()}</option>`)
      .join("");

    /* action URL 설정 (장고 뷰에 맞춰서!) */
    sheet.action = `/products/${pid}/toggle_wear/`;

    /* 모달 열기 */
    modal.classList.add("show");
    document.body.style.overflow = "hidden";
  });

  /* ② 닫기 : 배경이나 × 버튼 */
  modal.addEventListener("click", (e) => {
    if (
      e.target.classList.contains("wear-backdrop") ||
      e.target.classList.contains("wear-close")
    ) {
      modal.classList.remove("show");
      document.body.style.overflow = "auto";
    }
  });
})();
