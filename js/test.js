document.querySelector('.check-btn').addEventListener('click', function(e) {
  e.preventDefault(); // Prevent the form from submitting

  var inputText = document.getElementById('ai-check-input').value;
  var results = document.getElementById('results');
  var notification = document.getElementById('notification');

  if (inputText.trim().length === 0) {
    // Show notification if input is empty
    results.classList.add('hidden');
    notification.classList.remove('hidden');
  } else {
    // Show results if input is not empty
    notification.classList.add('hidden');
    results.classList.remove('hidden');
  }
});