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

document.addEventListener('DOMContentLoaded', () => {
    // Functions to open and close a modal
    function openModal($el) {
        $el.classList.add('is-active');
    }

    function closeModal($el) {
        $el.classList.remove('is-active');
    }

    function closeAllModals() {
        (document.querySelectorAll('.modal') || []).forEach(($modal) => {
            closeModal($modal);
        });
    }

    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
        const modal = $trigger.dataset.target;
        const $target = document.getElementById(modal);

        $trigger.addEventListener('click', () => {
            openModal($target);
        });
    });

    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
        const $target = $close.closest('.modal');

        $close.addEventListener('click', () => {
            closeModal($target);
        });
    });

    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
        const e = event || window.event;

        if (e.keyCode === 27) { // Escape key
            closeAllModals();
        }
    });
});