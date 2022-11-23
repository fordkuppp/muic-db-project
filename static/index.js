const loginCloseButton = document.getElementById("login-close-button");
const loginBlock = document.getElementById("login-modal");
const signupBlock = document.getElementById("signup-modal");
const forgetBlock = document.getElementById("forget-modal");
const masterBlock = document.getElementById("master-modal")
const active = "is-active"


function closeLoginBlock() { loginBlock.classList.remove(active); }

function openLoginBlock() { loginBlock.classList.add(active); }

function closeSignupBlock() { signupBlock.classList.remove(active); }

function openSignupBlock() { signupBlock.classList.add(active); }

function closeForgetBlock() { forgetBlock.classList.remove(active); }

function openForgetBlock() { forgetBlock.classList.add(active); }

function openMasterBlock() { masterBlock.classList.add(active); }

function closeMasterBlock() { masterBlock.classList.remove(active); }

function register() {
    var form = new FormData()
    form.append("username", document.getElementById("username").value);
    form.append("email", document.getElementById("email").value);
    form.append("password1", document.getElementById("password1").value);
    form.append("password2", document.getElementById("password2").value);
    form.append("key", bcryptHash(document.getElementById("key").value));
    form.append("hint", document.getElementById("hint").value);
    axios.post("/user/signup/", form)
        .then(res => {
            window.location.href = "/user/"
        })
        .catch(err => {
            console.log(err)
        })
    // console.log(compare(document.getElementById("key").value, form.get("key")))
}

function bcryptHash(pass) {
    return dcodeIO.bcrypt.hashSync(pass, 12)
}

function bcryptCompare(pass, hash) {
    return dcodeIO.bcrypt.compareSync(pass, hash);
}