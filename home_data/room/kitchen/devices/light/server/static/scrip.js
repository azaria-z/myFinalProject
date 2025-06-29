function toggleLight() {
    const lightBulb = document.getElementById('light-bulb');
    const state = lightBulb.classList.contains('off') ? true : false;

    fetch('http://127.0.0.1:5000/light/state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ state: state })
    })
    .then(response => response.json())
    .then(data => updateLightDisplay(data))
    .catch(error => console.error('Error:', error));
}

function changeBrightness(value) {
    fetch('http://127.0.0.1:5000/light/brightness', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ brightness: parseInt(value) })
    })
    .then(response => response.json())
    .then(data => updateLightDisplay(data))
    .catch(error => console.error('Error:', error));
}

function changeLightColor() {
    const color = document.getElementById('color').value;
    fetch('http://127.0.0.1:5000/light/color', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ color: color })
    })
    .then(response => response.json())
    .then(data => updateLightDisplay(data))
    .catch(error => console.error('Error:', error));
}

// פונקציה לעדכון התצוגה
function updateLightDisplay(data) {
    const lightBulb = document.getElementById('light-bulb');
    
    // עדכון מצב המנורה
    if (data.state === "on") {
        lightBulb.classList.remove('off');
        lightBulb.classList.add('on');
    } else {
        lightBulb.classList.remove('on');
        lightBulb.classList.add('off');
    }

    // עדכון צבע המנורה
    if (data.color) {
        lightBulb.style.backgroundColor = data.color;
    }

    // עדכון בהירות המנורה
    const brightness = data.brightness;
    if (brightness >= 75) {
        lightBulb.style.filter = 'brightness(100%)';
    } else if (brightness >= 50) {
        lightBulb.style.filter = 'brightness(75%)';
    } else if (brightness >= 25) {
        lightBulb.style.filter = 'brightness(50%)';
    } else {
        lightBulb.style.filter = 'brightness(25%)';
    }
}
