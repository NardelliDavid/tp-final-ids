//Scrip de js para hacer el menú desplegable
const menuToggle = document.getElementById('menuToggle');
const sidebarContainer = document.getElementById('sidebarContainer');

    if (menuToggle && sidebarContainer) {
        menuToggle.addEventListener('click', () => {
            sidebarContainer.classList.toggle('show');
        });
}