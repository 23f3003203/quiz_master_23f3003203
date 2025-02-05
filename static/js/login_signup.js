function showAlert(message){
    alert(message)
}

function formvalidation(){
    var email = document.getElementById("s-username").value;
    var password = document.getElementById("s-password").value;
    var confirmPassword = document.getElementById("cpassword").value;
    var alertElement = document.getElementById("alert");

    console.log(email, password, confirmPassword)

    // Regular expressions for validation
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    alertElement.classList.add("hide");
    alertElement.textContent = "";


    // Validate email
    if (!emailPattern.test(email)) {
        alertElement.textContent = "Invalid email address";
        alertElement.classList.remove("hide");
        return false;
    }

    // Validate password
    if (password.length < 6) {
        alertElement.textContent = "Password must be at least 6 characters long";
        alertElement.classList.remove("hide");
        return false;
    }

    // Validate confirm password
    if (password !== confirmPassword) {
        alertElement.textContent = "Passwords do not match";
        alertElement.classList.remove("hide");
        return false;
    }

    // If all validations pass
    return true;
}