document.cookie = "csrftoken={{ csrf_token }}; path=/";
      // 시계
      function updateClock() {
        const d = new Date();
        document.getElementById("clock").textContent = d.toTimeString().slice(0, 5);
      }
      updateClock();
      setInterval(updateClock, 60000);

      /*작성한 체형 사이즈 불러오기 */
      document.addEventListener('DOMContentLoaded', () => {
      fetch("/user/body-size/")  // GET
          .then(res => res.json()) 
          .then(data => {
              console.log(data);  // 콘솔로 받은 데이터를 확인
              console.log(data.is_public);
              if (data) {
                  //사이즈 공개 여부
                  // 1. 공개 여부 (is_public) 반영
                  const privacyToggle = document.getElementById("privacyToggle");
                  const label = document.getElementById("privacyLabel");
                  const tcontainer = document.querySelector(".toggle-container");

                  // is_public 값에 따라 체크박스 상태 설정
                  privacyToggle.checked = data.is_public !== undefined ? data.is_public : false;
                  
                  // 체크박스 상태에 따른 label 텍스트 변경
                  if (privacyToggle.checked) {
                    label.textContent = "공개";
                    tcontainer.classList.add("public");  // 공개 상태인 경우
                  } else {
                    label.textContent = "비공개";
                    tcontainer.classList.remove("public");  // 비공개 상태인 경우
                  }
                  
                  // 1. 컵 사이즈: 자동/직접 입력인지 판단
                  if (data.is_manual_cup) {
                      document.getElementById("manualCupInput").style.display = "block";  // 수동 입력란 보이기
                      document.getElementById("manualCupInput").querySelector("input").value = data.cup_size || '';
                      document.getElementById("cupResult").style.display = "block";  // 자동 계산 결과 숨기기
                  } else {
                      //자동 계산
                      const cupSize = data.cup_size || '';
                      const bust = data.bust || '';
                      const underbust = data.underbust || '';
                      setDialValue(cupSize, bust, underbust); 
                      document.getElementById("cupResult").innerText = cupSize;  // 자동 계산된 값 표시
                      document.getElementById("manualCupInput").style.display = "none";  // 수동 입력란 숨기기
                  }

                  // 2. 골반 둘레: 자동/수동 입력인지 판단
                  if (data.is_manual_pelvis) {
                      //수동 계산
                      document.getElementById("manualHipInput").style.display = "block";
                      document.getElementById("manualHipInput").querySelector("input").value = data.pelvis_size || '';
                      document.getElementById("hipResult").style.display = "block";  // 자동 계산 결과 숨기기
                  } else {
                      //자동 계산
                      document.getElementById("hipResult").innerText = data.pelvis_size || '';  // 자동 계산된 값 표시
                      document.getElementById("manualHipInput").style.display = "none";  // 수동 입력란 숨기기
                  }

                  // 나머지 데이터 입력
                  document.getElementById("waistInput").value = data.waist || '';
                  document.getElementById("hipInput").value = data.hip || '';
                  document.getElementById("height").value = data.height || '';
                  document.getElementById("weight").value = data.weight || '';
              }
          })
          .catch(error => console.error('Error fetching data:', error));
      });


      //다이얼 초기화 함수: 받아온 cup_size에  맞는 다이얼 값 설정
      function setDialValue(cupSize, bust, underbust) {
      const dial = document.getElementById('topBust');  // 윗가슴 다이얼을 나타내는 `ul` 요소
      const allItems = dial.querySelectorAll('li');  // 다이얼 항목들
      
      const bustStr = String(bust).trim(); 
      const targetItem = Array.from(allItems).find(item => item.textContent.trim() === bustStr);

      // 해당 항목이 있으면 선택 상태로 만들어서 중앙으로 스크롤
      if (targetItem) {
          targetItem.classList.add('selected');
          const scrollTop = targetItem.offsetTop - (dial.offsetHeight / 2) + (targetItem.offsetHeight / 2); // 중앙으로 조정
          dial.scrollTo({ top: scrollTop, behavior: "smooth" });
      }

      const underDial = document.getElementById('underBust');  // 밑가슴 다이얼을 나타내는 `ul` 요소
      const underItems = underDial.querySelectorAll('li');  // 다이얼 항목들

      const underbustStr = String(underbust).trim(); 
      const underTargetItem = Array.from(underItems).find(item => item.textContent.trim() === underbustStr);

      // 해당 항목이 있으면 선택 상태로 만들어서 중앙으로 스크롤
      if (underTargetItem) {
          underTargetItem.classList.add('selected');
          const scrollTop = underTargetItem.offsetTop - (underDial.offsetHeight / 2) + (underTargetItem.offsetHeight / 2); // 중앙으로 조정
          underDial.scrollTo({ top: scrollTop, behavior: "smooth" });
      }
      }


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
        if (!isPublic) {
          document.getElementById("cupResult").innerText = "";
          btn.classList.remove("active");
          return;  // 사이즈 측정 요청 막음
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
        // setTimeout(() => {
        //   el.scrollTop = liHeight * 1; // 두 번째 항목이 중앙에 오게
        //   el.querySelectorAll("li")[2]?.classList.add("selected");
        // }, 100);
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

         // 자동 계산이 활성화되었을 때 다이얼에 맞는 값을 세팅
         if (type === "cup" && !isVisible) {
            const cupResultElement = document.getElementById("cupResult");
            if (cupResultElement) {
                const cupSize = cupResultElement.innerText;
                setDialValue(cupSize); // 다이얼에 선택된 값으로 업데이트
            }
        }

        if (type === "hip" && !isVisible) {
            const pelvisResultElement = document.getElementById("pelvisResult");
            if (pelvisResultElement) {
                const pelvisSize = pelvisResultElement.innerText.trim();
                document.getElementById("manualHipInput").querySelector("input").value = pelvisSize; // 자동 계산된 값 설정
            }
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

        const isPublic = document.getElementById("privacyToggle").checked; //공개 여부

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
          isPublic,
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
            is_manual_cup: isManualCup,  // 자동 계산이면 false, 수동이면 true
            is_manual_pelvis: isManualPelvis,  // 자동 계산이면 false, 수동이면 true
            is_public: isPublic,
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.message) alert("저장 완료!");
            else alert("오류 발생: " + data.error);
          });
      }
