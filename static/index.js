const loginCloseButton = document.getElementById("login-close-button");
const loginBlock = document.getElementById("login-modal");
const signupBlock = document.getElementById("signup-modal");
const resetBlock = document.getElementById("reset-modal");
const active = "is-active"


function closeLoginBlock() { loginBlock.classList.remove(active); }

function openLoginBlock() { loginBlock.classList.add(active); }

function closeSignupBlock() { signupBlock.classList.remove(active); }

function openSignupBlock() { signupBlock.classList.add(active); }

function closeResetBlock() { resetBlock.classList.remove(active); }

function openResetBlock() { resetBlock.classList.add(active); }