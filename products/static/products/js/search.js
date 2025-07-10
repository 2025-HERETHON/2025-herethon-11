document.addEventListener("DOMContentLoaded", () => {
  /* 시계 */
  function updateClock() {
    const d = new Date();
    const c1 = document.getElementById("clock");
    const c2 = document.getElementById("clock-modal");
    if (c1) c1.textContent = d.toTimeString().slice(0, 5);
    if (c2) c2.textContent = d.toTimeString().slice(0, 5);
  }
  updateClock();
  setInterval(updateClock, 60000);

  /* 네비 */
  const STATIC_PATH = "{% static 'products/productimg/' %}";
  const HOME_URL = "{% url 'home' %}";
  document.querySelectorAll(".bottom-nav .nav-item").forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const base = item.dataset.icon;
      document.querySelectorAll(".bottom-nav .nav-item").forEach((n) => {
        const b = n.dataset.icon;
        const active = n === item;
        n.classList.toggle("active", active);
        n.querySelector("img").src =
          STATIC_PATH + b + (active ? "_red.png" : ".png");
      });
      if (base === "home") {
        if (location.pathname !== HOME_URL && location.pathname !== "/") {
          location.href = HOME_URL;
        } else {
          window.scrollTo({ top: 0, behavior: "smooth" });
        }
      } else {
        alert("준비 중인 페이지입니다 🛠️");
      }
    });
  });

  /* 모달 열기/닫기 */
  const recModal = document.getElementById("rec-modal");
  document.querySelector(".btn-rec").addEventListener("click", () => {
    recModal.classList.add("show");
    document.body.style.overflow = "hidden";
  });
  recModal.querySelector(".modal-close").addEventListener("click", closeModal);
  recModal.addEventListener("click", (e) => {
    if (e.target === recModal || e.target.classList.contains("modal-backdrop"))
      closeModal();
  });
  function closeModal() {
    recModal.classList.remove("show");
    document.body.style.overflow = "auto";
  }

  /* 체형 버튼 */
  document.getElementById("btn-body").addEventListener("click", (e) => {
    e.currentTarget.classList.toggle("loaded");
  });

  /* 가격 슬라이더 */
  const MIN = 0,
    MAX = 500000,
    STEP = 1000,
    SLIDER_W = 330;
  let vMin = 0,
    vMax = 236000;
  const hMin = document.getElementById("handle-min"),
    hMax = document.getElementById("handle-max"),
    iMin = document.getElementById("price-min"),
    iMax = document.getElementById("price-max"),
    slider = document.getElementById("price-slider");
  const val2px = (v) => ((v - MIN) / (MAX - MIN)) * SLIDER_W;
  const px2val = (x) =>
    Math.round(((x / SLIDER_W) * (MAX - MIN)) / STEP) * STEP;
  const render = () => {
    hMin.style.left = val2px(vMin) + "px";
    hMax.style.left = val2px(vMax) + "px";
    iMin.value = vMin.toLocaleString();
    iMax.value = vMax.toLocaleString();
  };
  render();
  const onlyNum = (s) => s.replace(/[^\d]/g, "");
  const sync = (isMin, raw) => {
    const n = +onlyNum(raw) || 0;
    if (isMin) vMin = Math.min(Math.max(MIN, n), vMax - STEP);
    else vMax = Math.max(Math.min(MAX, n), vMin + STEP);
    render();
  };
  iMin.addEventListener("input", (e) => sync(true, e.target.value));
  iMax.addEventListener("input", (e) => sync(false, e.target.value));
  const drag = (handle, isMin) => {
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
  };
  drag(hMin, true);
  drag(hMax, false);

  /* 칩 토글 */
  const toggleWrap = (btnId, wrapId, txt) => {
    const btn = document.getElementById(btnId),
      wrap = document.getElementById(wrapId);
    btn.addEventListener("click", () => {
      wrap.classList.toggle("open");
      btn.textContent = wrap.classList.contains("open") ? "접기" : txt;
    });
  };
  toggleWrap("color-toggle", "color-wrap", "색상 전체보기");
  toggleWrap("mat-toggle", "mat-wrap", "소재 전체보기");
  toggleWrap("type-toggle", "type-wrap", "타입 전체보기");
  document.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip");
    if (chip) chip.classList.toggle("selected");
  });

  /* 초기화/추천 */
  const reset = () => {
    ["color", "mat", "type"].forEach((k) => {
      const wrap = document.getElementById(`${k}-wrap`);
      wrap
        .querySelectorAll(".selected")
        .forEach((el) => el.classList.remove("selected"));
      wrap.classList.remove("open");
      document.getElementById(`${k}-toggle`).textContent =
        k === "color"
          ? "색상 전체보기"
          : k === "mat"
          ? "소재 전체보기"
          : "타입 전체보기";
    });
    vMin = MIN;
    vMax = 236000;
    render();
    document.getElementById("btn-body").classList.remove("loaded");
    document
      .querySelector(".modal-sheet")
      .scrollTo({ top: 0, behavior: "smooth" });
  };
  document.getElementById("btn-reset").addEventListener("click", reset);
  document
    .getElementById("btn-apply")
    .addEventListener("click", () => alert("추천 검색 실행!"));
});

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

          const phone = document.getElementById("phone");
          phone?.classList.add("show");

          document.body.style.overflow = "hidden";

          phone.querySelector(".wear-close")?.addEventListener("click", () => {
            phone.classList.remove("show");
            document.body.style.overflow = "auto";
          });
        });
    });
  });
});

function toggleLike(event) {
  event.stopPropagation();

  const button = event.currentTarget;
  const productId = button.dataset.productId;

  fetch(`/products/${productId}/like/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      if (data.status === 'liked') {
        button.classList.add('liked');
      } else if (data.status === 'unliked') {
        button.classList.remove('liked');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// CSRF 토큰 가져오는 함수
function getCookie(name) {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith(name + '='));
  return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".wear").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.stopPropagation(); // 다시 한 번 안전하게
      const productId = btn.dataset.id;
      const colors = btn.dataset.colors;
      const sizes = btn.dataset.sizes;

      // 모달 여는 함수 호출
      openWearModal(productId, colors, sizes);
    });
  });
});

function openWearModal(productId, colors, sizes) {
  // 여기에 모달 열기 로직 작성
  const modal = document.getElementById("wear-modal-container");
  modal.innerHTML = `
    <div class="modal">
      <h2>착용 옵션 선택</h2>
      <p>상품 ID: ${productId}</p>
      <p>컬러: ${colors}</p>
      <p>사이즈: ${sizes}</p>
      <button onclick="closeWearModal()">닫기</button>
    </div>
  `;
  modal.style.display = "block";
}

function closeWearModal() {
  document.getElementById("wear-modal-container").style.display = "none";
}


