const loginCloseButton = document.getElementById("login-close-button");
const loginBlock = document.getElementById("login-modal");
const signupBlock = document.getElementById("signup-modal");
const forgetBlock = document.getElementById("forget-modal");
const active = "is-active"


function closeLoginBlock() { loginBlock.classList.remove(active); }

function openLoginBlock() { loginBlock.classList.add(active); }

function closeSignupBlock() { signupBlock.classList.remove(active); }

function openSignupBlock() { signupBlock.classList.add(active); }

function closeForgetBlock() { forgetBlock.classList.remove(active); }

function openForgetBlock() { forgetBlock.classList.add(active); }

function goToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}