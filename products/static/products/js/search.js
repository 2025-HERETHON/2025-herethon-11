let vMin = 0;
let vMax = 236000;
// 제일 위에 추가!
let isBodyDataLoaded = false;
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
      e.preventDefault(); // ⛔ 기본 <a href> 동작 막음
      const base = item.dataset.icon;
      const url = item.dataset.url;

      // 하단 네비 아이콘 바꾸는 부분
      document.querySelectorAll(".bottom-nav .nav-item").forEach((n) => {
        const b = n.dataset.icon;
        const active = n === item;
        n.classList.toggle("active", active);
        n.querySelector("img").src =
          STATIC_PATH + b + (active ? "_red.png" : ".png");
      });

      // 각 버튼별 페이지 이동 로직
      if (base === "home") {
        if (location.pathname !== url && location.pathname !== "/") {
          location.href = url;
        } else {
          window.scrollTo({ top: 0, behavior: "smooth" });
        }
      } else {
        location.href = url; // ⭐ 바로 이동 가능!!!!
      }
    });
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
  console.log("찜 누름 ✅", productId);
  fetch(`/products/${productId}/like/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
    })
    .then((data) => {
      if (data.status === "liked") {
        button.classList.add("liked");
      } else if (data.status === "unliked") {
        button.classList.remove("liked");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// CSRF 토큰 가져오는 함수
function getCookie(name) {
  const cookieValue = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="));
  return cookieValue ? decodeURIComponent(cookieValue.split("=")[1]) : null;
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
