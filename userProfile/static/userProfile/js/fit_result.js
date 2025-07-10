// 시계
      function updateClock() {
        const d = new Date();
        document.getElementById("clock").textContent = d
          .toTimeString()
          .slice(0, 5);
      }
      updateClock();
      setInterval(updateClock, 60000);

      // 더미 데이터
      const wornProducts = Array(6).fill({
        img: "products/productimg/sample1.jpg",
        brand: "더잠",
        title: "이지핏 스퀘어 브라탑 · 팬티 세트",
        color: "블랙",
        size: "M",
        price: 23000,
      });

      const makeCard = (p) => `
        <div class="review-item">
          <img src="${p.img}" alt="${p.title}" />
          <div class="item-info">
            <div class="title">[${p.brand}] ${p.title}</div>
            <div class="opt">${p.color} · ${p.size}</div>
            <div class="price">${p.price.toLocaleString()}원</div>
          </div>
          <a href="#" class="btn-write">내 리뷰 보기</a>
        </div>`;
      document.getElementById("review-wrap").innerHTML = wornProducts
        .map(makeCard)
        .join("");

      function showLogout() {
        document.getElementById("logoutModal").style.display = "flex";
      }
      function hideLogout() {
        document.getElementById("logoutModal").style.display = "none";
      }
      function showProfileEdit() {
        document.getElementById("profileModal").style.display = "flex";
      }
      function hideProfileEdit() {
        document.getElementById("profileModal").style.display = "none";
      }
      function updateProfileImg(event) {
        const reader = new FileReader();
        reader.onload = function (e) {
          const previewImg = document.getElementById("previewImg");
          const currentProfile = document.getElementById("currentProfile");

          if (previewImg) previewImg.src = e.target.result;
          if (currentProfile) currentProfile.src = e.target.result; // ← 핵심
        };

        if (event.target.files[0]) {
          reader.readAsDataURL(event.target.files[0]);
        }
      }

      function saveProfile() {
        const previewImg = document.getElementById("previewImg");
        const currentProfile = document.getElementById("currentProfile");
        if (previewImg && currentProfile) {
          currentProfile.src = previewImg.src;
        }
        hideProfileEdit();
      }