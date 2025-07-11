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

document.addEventListener('DOMContentLoaded', function () {
  const heartEl = document.getElementById('wish');
  const heartCountEl = document.querySelector('.heart-count');

  if (!heartEl) return;

  heartEl.addEventListener('click', function () {
    fetch('/products/review/' + productId + '/like/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.liked) {
          heartEl.classList.add('on');
        } else {
          heartEl.classList.remove('on');
        }
        heartCountEl.textContent = data.like_count;
      })
      .catch((err) => console.error('찜 오류:', err));
  });

  // CSRF 토큰 가져오기 함수
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
