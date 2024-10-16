//mobile menu
document.addEventListener('DOMContentLoaded', () => {
    const burgerIcon = document.querySelector('#burger');
    const navBarMenu = document.querySelector('#nav-links');

    burgerIcon.addEventListener('click', () => {
        navBarMenu.classList.toggle('is-active')
    })
});