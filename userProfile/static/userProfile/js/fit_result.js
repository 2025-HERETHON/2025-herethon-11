// window.addEventListener("DOMContentLoaded", function () {
//         const savedImage = localStorage.getItem("profileImage");
//         const currentProfile = document.getElementById("currentProfile");
//         const previewImg = document.getElementById("previewImg");
//         const mainProfile = document.getElementById("mainProfile");

//         if (savedImage) {
//             if (currentProfile) currentProfile.src = savedImage;
//             if (previewImg) previewImg.src = savedImage;
//             if (mainProfile) mainProfile.src = savedImage;
//         }
//         });
      // 시계
      function updateClock() {
        const d = new Date();
        document.getElementById("clock").textContent = d.toTimeString().slice(0, 5);
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

      // const makeCard = (p) => `
      //   <div class="review-item">
      //     <img src="${p.img}" alt="${p.title}" />
      //     <div class="item-info">
      //       <div class="title">[${p.brand}] ${p.title}</div>
      //       <div class="opt">${p.color} · ${p.size}</div>
      //       <div class="price">${p.price.toLocaleString()}원</div>
      //     </div>
      //     <a href="#" class="btn-write">내 리뷰 보기</a>
      //   </div>`;
      // document.getElementById("review-wrap").innerHTML = wornProducts.map(makeCard).join("");

      function showLogout() {
        document.getElementById("logoutModal").style.display = "flex";
      }
      function hideLogout() {
        document.getElementById("logoutModal").style.display = "none";
      }
      function showProfileEdit() {
        // const savedImage = localStorage.getItem("profileImage");
        // const previewImg = document.getElementById("previewImg");
        // if (savedImage) {
        // previewImg.src = savedImage;
        // } else {
        // previewImg.src = "/static/account/img/profile.png";
        // }
        document.getElementById("profileModal").style.display = "flex";
    }

      function hideProfileEdit() {
        document.getElementById("profileModal").style.display = "none";
      }
      function updateProfileImg(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (e) {
            const dataUrl = e.target.result;
            document.getElementById("previewImg").src = dataUrl;
        };
        reader.readAsDataURL(file);
        }

        function saveProfile() {
        const previewImg = document.getElementById("previewImg");
        const currentProfile = document.getElementById("currentProfile");
        const mainProfile = document.getElementById("mainProfile");

        const newSrc = previewImg.src;
        if (currentProfile) currentProfile.src = newSrc;
        if (mainProfile) mainProfile.src = newSrc;

        // localStorage.setItem("profileImage", newSrc);

        hideProfileEdit();
        }

        //닉네임 수정시 글자수 세기
        function updateCharCount() {
          const input = document.getElementById("nicknameInput");
          const count = document.getElementById("charCount");
          count.textContent = input.value.length;
        }

        // 페이지 로드 시 초기값도 계산해줌
        document.addEventListener("DOMContentLoaded", () => {
          updateCharCount();
        });