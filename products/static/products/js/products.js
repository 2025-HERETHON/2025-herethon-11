(() => {
  // const recentViewed = [
  //   {
  //     id: 1,
  //     price: 21000,
  //     brand: "마론파이브",
  //     desc: "날마다 브라탑 모달 곶지 유넥",
  //     img: "https://placehold.co/200x200",
  //   },
  //   {
  //     id: 2,
  //     price: 12000,
  //     brand: "리무브",
  //     desc: "모달 멜로우 팬티",
  //     img: "https://placehold.co/200x200",
  //   },
  //   {
  //     id: 3,
  //     price: 15000,
  //     brand: "마론파이브",
  //     desc: "쉬어 트렁크 모달 - 블랙",
  //     img: "https://placehold.co/200x200",
  //   },
  // // ];
  // const makeCard = (p) =>
  //   `<div class="item-card"><div class="item-img-wrap"><img src="${
  //     p.img
  //   }" alt="${
  //     p.desc
  //   }"><span class="heart"></span><span class="wear"></span></div><div class="item-info"><div class="item-price">${p.price.toLocaleString()}</div><div class="item-brand">${
  //     p.brand
  //   }</div><div class="item-desc">${p.desc}</div></div></div>`;
  // document.getElementById("recent-wrap").innerHTML = recentViewed
  //   .map(makeCard)
  //   .join("");
  // 하트
  //   document.addEventListener("DOMContentLoaded", function () {
  //     document.querySelectorAll(".heart").forEach((h) =>
  //       h.addEventListener("click", () => h.classList.toggle("liked"))
  //     );
  //   });

  /* 착용 제품 */ document
    .querySelectorAll(".wear")
    .forEach((w) =>
      w.addEventListener("click", () => w.classList.toggle("checked"))
    );
  /** 사용자 이름 삽입 */
  const userName = "멋사"; // 서버나 로컬Storage 등에서 받아온 값
  const nameSpan = document.getElementById("user-name");
  if (nameSpan) nameSpan.textContent = userName;

  /* 시계 */ function updateClock() {
    const d = new Date();
    document.getElementById("clock").textContent = d.toTimeString().slice(0, 5);
  }
  updateClock();
  setInterval(updateClock, 60000);

  /* === 바텀 네비게이션 === */
  const STATIC_PATH = "{% static 'products/productimg/' %}";
  const navItems = document.querySelectorAll(".bottom-nav .nav-item");

  navItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      /* 1. 모든 아이콘 & 글자 초기화 */
      navItems.forEach((n) => {
        const base = n.dataset.icon;
        n.classList.remove("active");
        n.querySelector("img").src = STATIC_PATH + base + ".png";
      });
      /* 2. 선택된 아이콘만 빨간색으로 */
      const base = item.dataset.icon;
      item.classList.add("active");
      item.querySelector("img").src = STATIC_PATH + base + "_red.png";

      if (base === "home") {
        window.scrollTo({ top: 0, behavior: "smooth" }); // 홈은 스크롤 맨 위
      } else if (base === "review") {
        window.location.href = "review.html";
      } else if (base === "user") {
        window.location.href = "mypage.html";
      } else {
        alert("준비 중인 페이지입니다"); // 그 외에는 알림
      }
    });
  });

  /* ───────────────────── 0. 모달 열기 / 닫기 ───────────────────── */
  const btnOpen = document.querySelector(".btn-rec"); // “추천받기” 버튼
  const recModal = document.getElementById("rec-modal");
  const btnClose = recModal.querySelector(".modal-close");
  document.addEventListener("DOMContentLoaded", () => {
    function updateClockModal() {
      const d = new Date();
      document.getElementById("clock-modal").textContent = d
        .toTimeString()
        .slice(0, 5);
    }
    updateClockModal();
    setInterval(updateClockModal, 60000);
  });
  btnOpen.addEventListener("click", () => {
    recModal.classList.add("show");
    document.body.style.overflow = "hidden";
  });
  btnClose.addEventListener("click", closeModal);
  recModal.addEventListener("click", (e) => {
    if (e.target === recModal || e.target.classList.contains("modal-backdrop"))
      closeModal();
  });
  function closeModal() {
    recModal.classList.remove("show");
    document.body.style.overflow = "auto";
  }

  /* 상태바 시계 */
  setInterval(() => {
    const d = new Date();
    document.getElementById("clock-modal").textContent = d
      .toTimeString()
      .slice(0, 5);
  }, 1000 * 60);

  /* 체형 불러오기 버튼 색상 전환 */
  document.getElementById("btn-body").addEventListener("click", (e) => {
    e.currentTarget.classList.toggle("loaded");
  });

  /* ───────────────────── 1. 가격 슬라이더 로직 (원본 그대로) ───────────────────── */
  const MIN = 0,
    MAX = 500000,
    STEP = 1000,
    SLIDER_W = 330;

  const hMin = document.getElementById("handle-min");
  const hMax = document.getElementById("handle-max");
  const iMin = document.getElementById("price-min");
  const iMax = document.getElementById("price-max");
  const slider = document.getElementById("price-slider");

  let vMin = 0,
    vMax = 236000;

  const val2px = (v) => ((v - MIN) / (MAX - MIN)) * SLIDER_W;
  const px2val = (x) =>
    Math.round(((x / SLIDER_W) * (MAX - MIN)) / STEP) * STEP;

  function render() {
    hMin.style.left = val2px(vMin) + "px";
    hMax.style.left = val2px(vMax) + "px";
    iMin.value = vMin.toLocaleString();
    iMax.value = vMax.toLocaleString();
  }
  const onlyNum = (s) => s.replace(/[^\d]/g, "");

  function syncInput(isMin, raw) {
    const n = +onlyNum(raw) || 0;
    if (isMin) vMin = Math.min(Math.max(MIN, n), vMax - STEP);
    else vMax = Math.max(Math.min(MAX, n), vMin + STEP);
    render();
  }
  iMin.addEventListener("input", (e) => syncInput(true, e.target.value));
  iMax.addEventListener("input", (e) => syncInput(false, e.target.value));

  function bindDrag(handle, isMin) {
    const start = (e) => {
      e.preventDefault();
      const move = (m) => {
        const x =
          (m.touches ? m.touches[0].clientX : m.clientX) -
          slider.getBoundingClientRect().left;
        const clamped = Math.max(0, Math.min(SLIDER_W, x));
        const v = Math.min(MAX, Math.max(MIN, px2val(clamped)));
        if (isMin) vMin = Math.min(v, vMax - STEP);
        else vMax = Math.max(v, vMin + STEP);
        render();
      };
      const stop = () => {
        document.removeEventListener("mousemove", move);
        document.removeEventListener("touchmove", move);
      };
      document.addEventListener("mousemove", move);
      document.addEventListener("touchmove", move, { passive: false });
      document.addEventListener("mouseup", stop, { once: true });
      document.addEventListener("touchend", stop, { once: true });
    };
    handle.addEventListener("mousedown", start);
    handle.addEventListener("touchstart", start, { passive: false });
  }
  bindDrag(hMin, true);
  bindDrag(hMax, false);
  render();

  /* ───────────────────── 2. 칩 토글 & 선택 공통 함수 ───────────────────── */
  function bindChipToggle(btnId, wrapId, defaultTxt) {
    const btn = document.getElementById(btnId);
    const wrap = document.getElementById(wrapId);
    btn.addEventListener("click", () => {
      wrap.classList.toggle("open");
      btn.textContent = wrap.classList.contains("open") ? "접기" : defaultTxt;
    });
  }
  bindChipToggle("color-toggle", "color-wrap", "색상 전체보기");
  bindChipToggle("mat-toggle", "mat-wrap", "소재 전체보기");
  bindChipToggle("type-toggle", "type-wrap", "타입 전체보기");

  /* 칩 클릭(선택/해제) */
  document.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip, .color-item, .mat-chip");
    if (chip) chip.classList.toggle("selected");
  });

  /* ───────────────────── 3. 초기화 / 추천받기 버튼 UI 효과 ───────────────────── */
  document.getElementById("btn-reset").addEventListener("click", (e) => {
    e.currentTarget.classList.toggle("active");
    // TODO: reset 로직이 필요하면 여기에서 입력칸, 칩, 슬라이더 값 초기화
  });
  document.getElementById("btn-apply").addEventListener("click", (e) => {
    e.currentTarget.classList.toggle("active");
    // TODO: 추천 검색 실행 로직
  });
  function resetFilters() {
    /* 1. 칩 선택 해제 + 랩퍼 닫기 + 토글 글자 복원 */
    ["color", "mat", "type"].forEach((k) => {
      const wrap = document.getElementById(`${k}-wrap`);
      const toggle = document.getElementById(`${k}-toggle`);

      wrap
        .querySelectorAll(".selected")
        .forEach((el) => el.classList.remove("selected"));
      wrap.classList.remove("open");
      toggle.textContent =
        k === "color"
          ? "색상 전체보기"
          : k === "mat"
          ? "소재 전체보기"
          : "타입 전체보기";
    });

    /* 2. 가격 슬라이더 & 입력값 초기화 */
    vMin = MIN; // 0
    vMax = 236000; // 원하는 기본값
    render(); // 기존 슬라이더 함수 → 핸들·input 동기화

    /* 3. 체형 불러오기 버튼·칸 초기화(필요하면) */
    document.getElementById("btn-body").classList.remove("loaded");

    /* 4. 스크롤 맨 위로 (선택) */
    document
      .querySelector(".modal-sheet")
      .scrollTo({ top: 0, behavior: "smooth" });
  }
  document.getElementById("btn-reset").addEventListener("click", (e) => {
    e.currentTarget.classList.remove("active");
    resetFilters();
  });
})();
document.addEventListener("DOMContentLoaded", () => {
  const wearButtons = document.querySelectorAll(".wear");
  const container = document.getElementById("wear-modal-container");

  wearButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const pid = btn.dataset.id;
      const colors = btn.dataset.colors;
      const sizes = btn.dataset.sizes;

      fetch(`/products/wear-modal/${pid}/?colors=${colors}&sizes=${sizes}`)
        .then((response) => response.text())
        .then((html) => {
          container.innerHTML = html;

          // DOM에 삽입된 후에 select 해야 적용됨
          const phone = document.getElementById("phone");
          phone?.classList.add("show");

          document.body.style.overflow = "hidden";

          // 닫기 버튼도 여기서 등록해야 됨
          phone.querySelector(".wear-close")?.addEventListener("click", () => {
            phone.classList.remove("show");
            document.body.style.overflow = "auto";
          });
        });
    });
  });
});



