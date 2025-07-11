// 시계
      function updateClock() {
        const d = new Date();
        document.getElementById("clock").textContent = d.toTimeString().slice(0, 5);
      }
      updateClock();
      setInterval(updateClock, 60000);