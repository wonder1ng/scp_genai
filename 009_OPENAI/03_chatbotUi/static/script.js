document.addEventListener("DOMContentLoaded", () => {
  const chatInput = document.getElementById("user-input");
  const formInput = document.getElementById("user-input-form");
  const resultDiv = document.getElementById("result");
  const chatContainer = document.getElementById("chat-container");

  formInput.addEventListener("submit", async (e) => {
    e.preventDefault();
    const chatMessage = chatInput.value.trim();
    if (!chatMessage) return;

    appendMessage("user", chatMessage);
    chatInput.value = "";

    try {
      const replyText = await fetchChatbotReply(chatMessage);
      appendMessage("bot", replyText);
    } catch (error) {
      console.error("에러 발생:", error);
      appendMessage("bot", "서버 연결 불량");
    }
  });
  /**
   * API 통신 담당
   */
  async function fetchChatbotReply(message) {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ chatMessage: message }),
    });

    if (!response.ok) {
      throw new Error("네트워크 응답에 문제가 있습니다.");
    }
    const data = await response.json();
    return data.reply;
  }

  /**
   * 화면에 말풍선 DOM을 그리는 함수 (그리기 분리)
   * @param {string} sender - 'user' 또는 'bot'
   * @param {string} text - 메시지 내용
   */
  function appendMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);

    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("bubble");
    bubbleDiv.innerText = text;

    messageDiv.appendChild(bubbleDiv);
    resultDiv.appendChild(messageDiv);

    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
});
