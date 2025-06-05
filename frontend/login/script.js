let isLogin = true;

function toggleForm() {
    isLogin = !isLogin;

    document.getElementById("formTitle").textContent = isLogin ? "Login" : "Sign Up";
    document.getElementById("submitBtn").textContent = isLogin ? "Login" : "Sign Up";
    document.getElementById("repeatPassword").style.display = isLogin ? "none" : "block";
    document.getElementById("toggleBtn").textContent = isLogin ? "Don't have an account? Sign Up" : "Already have an account? Login";
}

document.getElementById("authForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const repeatPassword = document.getElementById("repeatPassword").value;

    if (!isLogin && password !== repeatPassword) {
        alert("Passwords do not match!");
        return;
    }

    if (isLogin) {
        // Handle login logic here
        alert(`Logging in as ${username}`);
    } else {
        // Handle signup logic here
        alert(`Signing up as ${username}`);
    }
});
