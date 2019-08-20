function checkTaskSubmit(event) {
  event.preventDefault();
  let taskId = event.target.getAttribute("task_id");
  let taskAnswer = document.getElementById(taskId).value;
  let payload = {"task_id": taskId, "task_answer": taskAnswer};
  fetch({{ url_for('check')|tojson }}, {
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
let submitButtonsArray = document.getElementsByName("check-task");
submitButtonsArray.forEach(function(element) {
    element.addEventListener('click', checkTaskSubmit)
})
