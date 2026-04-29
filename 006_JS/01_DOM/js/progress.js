let interval;
let timerid;
const timeInput = document.getElementById("timeInput");
const progress = document.getElementById("progress");
const progressText = document.getElementById("progressText");
const startButton = document.getElementById("startButton");
const clearButton = document.getElementById("clearButton");
startButton.addEventListener("click", startProgress);
clearButton.addEventListener("click", clearProgress);

function startProgress() {
  startButton.disabled = true;
  duration = parseInt(timeInput.value);
  console.log("입력 초: ", duration);
  progress.style.width = progressText.textContent = "0%";

  let elapsed = 0;
  timerId = setInterval(() => {
    console.log("반복호출");
    elapsed++;
    const ratio = (100 * elapsed) / duration;
    progress.style.width = `${ratio}%`;
    progressText.textContent = `${ratio}%`;
    console.log(progress);

    if (ratio >= 100) {
      clearInterval(timerId);
      startButton.disabled = false;
    }
  }, 1000);
}

function clearProgress() {
  if (timerId) clearInterval(timerId);
  progress.style.width = "2px";
  timeInput.value = "";
  progressText.textContent = `0%`;
  startButton.disabled = false;
}
