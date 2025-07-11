document.addEventListener("DOMContentLoaded", () => {
  // STATIC_PATH는 HTML <head>에서 선언된 전역 변수여야 합니다
  if (!window.STATIC_PATH) {
    console.warn("⚠️ STATIC_PATH is not defined.");
    return;
  }

  const path = window.location.pathname.replace(/\/$/, ""); // 맨 끝 슬래시 제거

  // 현재 페이지별로 활성화될 아이콘 이름 지정
  const routes = {
    "": "home",                     // /
    "/products": "home",            // products.html
    "/products/search": "home",     // products_search.html
    "/reviews": "review",            // review.html
    "/reviews/form": "review",       // review_form.html
    "/user/mypage": "user",              // fit_result.html, mypage.html
  };

  // routes 키에서 현재 path 매칭 시도
  const activeIcon = routes[path];

  if (activeIcon) {
    document.querySelectorAll(".bottom-nav .nav-item").forEach((item) => {
      const icon = item.dataset.icon;
      const img = item.querySelector("img");
      const isActive = icon === activeIcon;

      item.classList.toggle("active", isActive);
      img.src = `${window.STATIC_PATH}${icon}${isActive ? "_red" : ""}.png`;
    });
  } else {
    console.warn("❌ 해당 경로에 매칭되는 nav 아이콘 없음:", path);
  }
});
