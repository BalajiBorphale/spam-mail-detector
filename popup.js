document.getElementById('checkSpam').addEventListener('click', function() {
    const emailText = document.getElementById('emailText').value;

    fetch('https://smdetector-e9lm.onrender.com/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: emailText })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.prediction;
        // Add class based on spam/not spam
        if (data.prediction === 'Spam') {
            document.getElementById('result').classList.add('spam');
            document.getElementById('result').classList.remove('not-spam');
        } else {
            document.getElementById('result').classList.add('not-spam');
            document.getElementById('result').classList.remove('spam');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
