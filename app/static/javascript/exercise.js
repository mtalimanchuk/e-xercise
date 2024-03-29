function checkTaskSubmit(url, event) {
  event.preventDefault();
  let taskId = event.target.getAttribute("task_id");
  let taskAnswer = document.getElementById(taskId).value;
  let payload = {"task_id": taskId, "task_answer": taskAnswer};
  
  fetch(url, {
    method: 'POST',
    body: JSON.stringify(payload)
  })
    .then(parseJSON)
    .then(showTaskSubmitResult);
}

function parseJSON(response) {
  return response.json();
}

function showTaskSubmitResult(data) {
  let input = document.getElementById(data.id);
  if (data.result === true){
    input.style.backgroundColor = '#14ff8f';
  } else {
    input.style.backgroundColor = '#ff939c';
  }
}

function resizeInput(event) {
  let element = event.target;
  let inputLength = element.value.length;
  console.log(element.offsetWidth + "/" + inputLength)
  if (inputLength >= 10) {
    element.style.width = inputLength + "ch";
  }
  else {
    element.style.width = "10ch";
  }
}
