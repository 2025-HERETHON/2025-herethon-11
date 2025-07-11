document.cookie = "csrftoken={{ csrf_token }}; path=/";

      function getCSRFToken() {
        const tokenMeta = document.querySelector('meta[name="csrf-token"]');
        return tokenMeta ? tokenMeta.getAttribute("content") : "";
      }

      function calculateCup(btn) {
        const bust = getSelectedValue(document.getElementById("topBust"));
        const underbust = getSelectedValue(
          document.getElementById("underBust")
        );
        const isPublic = document.getElementById("privacyToggle").checked;

        const manualCup = document.getElementById("manualCupInput");
        if (manualCup.style.display === "block") return; //사이즈 직접 입력 시 버튼 실행 안되도록

        if (!isPublic) {
          document.getElementById("cupResult").innerText = "";
          btn.classList.remove("active");
          return; //사이즈 측정 요청 막음
        }

        const csrfToken = getCSRFToken();

        //가슴 사이즈 측정 요청
        fetch("/user/size-check-cup/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ bust, underbust }),
        })
          .then((res) => res.json())
          .then((data) => {
            // cup_size 결과 처리
            document.getElementById("cupResult").innerText = data.cup_size;
            btn.classList.add("active");
          });
      }

      function calculateHip(btn) {
        const waist = parseInt(document.getElementById("waistInput").value);
        const hip = parseInt(document.getElementById("hipInput").value);
        const isPublic = document.getElementById("privacyToggle").checked;

        const manualHip = document.getElementById("manualHipInput");
        if (manualHip.style.display === "block") return; //사이즈 직접 입력 시 버튼 실행 안되도록

        if (!isPublic) {
          document.getElementById("hipResult").innerText = "";
          btn.classList.remove("active");
          return;
        }

        if (isNaN(waist) || isNaN(hip)) {
          alert("허리와 힙 둘레를 모두 입력해주세요.");
          return;
        }
        if (hip < 82 || hip > 117) {
          document.getElementById("hipAlertOverlay").style.display = "flex";
          setTimeout(() => {
            document.getElementById("hipAlertOverlay").style.display = "none";
          }, 2000); // 2초 후 자동 닫힘
          return;
        }

        const csrfToken = getCSRFToken();

        //골반 사이즈 측정 요청
        fetch("/user/size-check-pelvis/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ waist, hip }),
        })
          .then((res) => res.json())
          .then((data) => {
            // pelvis_size 결과 처리
            document.getElementById("hipResult").innerText = data.pelvis_size;
            btn.classList.add("active");
          });
      }

      function getSelectedValue(el) {
        if (!el) return null;
        // 선택된 항목을 select-item 클래스에 selected 클래스가 둘 다 붙은 요소로 찾기
        const selected = el.querySelector(".select-item.selected");
        if (!selected) return null;

        // innerText가 숫자가 아닐 수도 있으니 숫자로 변환 시도
        const val = parseInt(selected.innerText, 10);
        return isNaN(val) ? null : val;
      }

      function createScrollList(id, from, to) {
        const el = document.getElementById(id);
        const liHeight = 30;

        for (let i = from; i <= to; i += 5) {
          const li = document.createElement("li");
          li.className = "select-item";
          li.innerText = i;
          el.appendChild(li);

          li.addEventListener("click", () => {
            const index = [...el.children].indexOf(li);
            const scrollTop = index * liHeight - liHeight; // 중앙 위치로
            el.scrollTo({ top: scrollTop, behavior: "smooth" });

            // 클래스 갱신
            el.querySelectorAll("li").forEach((item) =>
              item.classList.remove("selected")
            );
            li.classList.add("selected");
          });
        }

        el.addEventListener("scroll", () => {
          const items = el.querySelectorAll("li");
          items.forEach((item) => item.classList.remove("selected"));
          const index = Math.round(el.scrollTop / liHeight) + 1;
          if (items[index]) items[index].classList.add("selected");
        });

        // 초기 강조 위치 설정 (중간 숫자)
        setTimeout(() => {
          el.scrollTop = liHeight * 1; // 두 번째 항목이 중앙에 오게
          el.querySelectorAll("li")[2]?.classList.add("selected");
        }, 100);
      }

      createScrollList("topBust", 55, 110);
      createScrollList("underBust", 55, 110);

      function toggleManualInput(type) {
        const inputBox = document.getElementById(
          type === "cup" ? "manualCupInput" : "manualHipInput"
        );
        const arrow = document.getElementById(
          type === "cup" ? "cupArrow" : "hipArrow"
        );

        const isVisible = inputBox.style.display === "block";
        inputBox.style.display = isVisible ? "none" : "block";

        if (arrow) {
         arrow.src = isVisible
          ? STATIC_IMG_URL + "toggle1.png"
          : STATIC_IMG_URL + "toggle.png";
        }
      }

      document
        .getElementById("privacyToggle")
        .addEventListener("change", function () {
          const label = document.getElementById("privacyLabel");
          const tcontainer = document.querySelector(".toggle-container");
          if (this.checked) {
            label.textContent = "공개";
            tcontainer.classList.add("public");
          } else {
            label.textContent = "비공개";
            tcontainer.classList.remove("public");
          }
        });

      function resetAll() {
        document
          .querySelectorAll("input[type=number]")
          .forEach((input) => (input.value = ""));
        document
          .querySelectorAll(".result-box")
          .forEach((box) => (box.innerText = ""));
        document
          .querySelectorAll(".measure-btn")
          .forEach((btn) => btn.classList.remove("active"));
      }

      function saveData() {
        const cup_size_self = document.querySelector("#manualCupInput input").value.trim();
        const cup_size_auto = document.getElementById("cupResult").innerText.trim();
        const cup_size = cup_size_self !== "" ? cup_size_self : cup_size_auto;

        const pelvis_size_self = document.querySelector("#manualHipInput input").value.trim();
        const pelvis_size_auto = document.getElementById("hipResult").innerText.trim();
        const pelvis_size = pelvis_size_self !== "" ? pelvis_size_self : pelvis_size_auto;

        const isManualCup = cup_size_self !== "";
        const isManualPelvis = pelvis_size_self !== "";

        const bust = isManualCup ? null : getSelectedValue(document.getElementById("topBust"));
        const underbust = isManualCup ? null : getSelectedValue(document.getElementById("underBust"));

        const waist = isManualPelvis ? null : parseInt(document.getElementById("waistInput").value);
        const hip = isManualPelvis ? null : parseInt(document.getElementById("hipInput").value);

        const height = parseInt(document.getElementById("height").value);
        const weight = parseInt(document.getElementById("weight").value);

        const csrfToken = getCSRFToken();

        console.log({
          bust,
          underbust,
          cup_size,
          waist,
          hip,
          pelvis_size,
          height,
          weight,
        });

        //유효성 체크
        if (!cup_size) {
          alert("컵 사이즈를 입력하거나 측정해 주세요.");
          return;
        }
        if (!isManualCup && (!bust || !underbust)) {
          alert("윗가슴/밑가슴 둘레를 입력해 주세요.");
          return;
        }

        if (!pelvis_size) {
          alert("골반 사이즈를 입력하거나 측정해 주세요.");
          return;
        }
        if (!isManualPelvis && (isNaN(waist) || isNaN(hip))) {
          alert("허리/힙 둘레를 입력해 주세요.");
          return;
        }

        if (isNaN(height) || isNaN(weight)) {
          alert("키와 몸무게를 입력해 주세요.");
          return;
        }

        //최종 입력 사이즈 저장
        fetch("/user/save-body-info/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({
            bust,
            underbust,
            cup_size,
            pelvis_size,
            waist,
            hip,
            height,
            weight,
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.message) alert("저장 완료!");
            else alert("오류 발생: " + data.error);
          });
      }
