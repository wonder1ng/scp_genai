function deleteContent(id) {
  fetch("/delete", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("알 수 없는 오류가 발생했습니다.");
      }
      return;
    })
    .catch((error) => {
      console.log("delete 처리 중 오류가 발생: ", error);
    });
}
function editContent(id) {
  const oldList = document.getElementById(`li_${id}`);
  oldList.outerHTML = `<li class='border w-25' id='li_${id}'>
                <div>글번호: ${id}</div>
                <input id='title_${id}' name='title_${id}' type='text' placeholder='새 제목'>
                <br />
                <input id='content_${id}' name='content_${id}' type='text' placeholder='새 내용'>
                <br />
                <button class='btn btn-primary' id='edit_${id}' onclick='editApi(${id})'>저장</button>
                <button class='btn btn-danger' id='edit_${id}' onclick='getList()'>취소</button>
                </li>`;
}
function editApi(id) {
  const newTitle = document.getElementById(`title_${id}`).value;
  const newContent = document.getElementById(`content_${id}`).value;
  fetch("/modify", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id,
      title: newTitle,
      content: newContent,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("알 수 없는 오류가 발생했습니다.");
      }
      getList();
      return;
    })
    .catch((error) => {
      console.log("modify 처리 중 오류가 발생: ", error);
    });
}
document.getElementsByTagName("button")[0].addEventListener("click", () => {
  const title = document.getElementById("input-title").value;
  const content = document.getElementById("input-text").value;
  fetch("/create", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title,
      content,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("알 수 없는 오류가 발생했습니다.");
      }
      getList();
      return;
    })
    .catch((error) => {
      console.log("create 처리 중 오류가 발생: ", error);
    });
});
const cards = document.getElementById("card-list");
function getList() {
  fetch("/list")
    .then((response) => {
      if (!response.ok) {
        throw new Error("알 수 없는 오류가 발생했습니다.");
      }
      return response.json();
    })
    .then((data) => {
      cards.innerHTML =
        "<ul class='row'>" +
        data.body
          .map(
            (v) =>
              `<li class='border w-25' id='li_${v[0]}'>
                <div id='title_${v[0]}'>${v[1]}</div>
                <div id='content_${v[0]}'>${v[2]}</div>
                <button class='btn btn-info text-white' id='edit_${v[0]}' onclick='editContent(${v[0]})'>수정</button>
                <button class='btn btn-warning id='delete_${v[0]}' onclick='deleteContent(${v[0]})'>삭제</button>
                </li>`,
          )
          .join("") +
        "</ul>";
    })
    .catch((error) => {
      console.log("getList 처리 중 오류가 발생: ", error);
    });
}
getList();
