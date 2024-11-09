function login_page() {
    // Get the input values
    var user = document.getElementById('username').value;
    var pass = document.getElementById('password').value;
    var captcha = document.getElementById('captcha').value;

    // Validate the user credentials and captcha
    if (user === 'yuvaraja' && pass === '1234' && captcha.toUpperCase() === 'W68HP') {
        alert('Your login was successful');
        // Redirect to the dashboard page
        window.location.href = 'dashboard.html';
         
    } else {
        alert('Invalid username, password, or captcha');
    }
}
