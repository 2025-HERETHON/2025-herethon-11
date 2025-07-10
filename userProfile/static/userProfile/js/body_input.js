document.cookie = "csrftoken={{ csrf_token }}; path=/";

      function getCSRFToken() {
        //POST요청 보내기 위해 필요
        const cookieValue = document.cookie
          .split("; ")
          .find((row) => row.startsWith("csrftoken="));
        return cookieValue ? cookieValue.split("=")[1] : "";
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
            ? "{% static 'account/img/toggle1.png' %}"
            : "{% static 'account/img/toggle.png' %}"; // ▲ ▼ 토글
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
        const bust = getSelectedValue(document.getElementById("topBust"));
        const underbust = getSelectedValue(
          document.getElementById("underBust")
        );
        const cup_size = document.getElementById("cupResult").innerText;
        const waist = parseInt(document.getElementById("waistInput").value);
        const hip = parseInt(document.getElementById("hipInput").value);
        const pelvis_size = document.getElementById("hipResult").innerText;
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

        if (
          !bust ||
          !underbust ||
          !cup_size ||
          !waist ||
          !hip ||
          !pelvis_size ||
          !height ||
          !weight
        ) {
          alert("사이즈를 모두 측정한 후 저장하세요.");
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
            waist,
            hip,
            height,
            weight,
            pelvis_size,
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.message) alert("저장 완료!");
            else alert("오류 발생: " + data.error);
          });
      }
