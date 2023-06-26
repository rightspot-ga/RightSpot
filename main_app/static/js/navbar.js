// * Sidebar toggle function
// * This script is used to toggle the sidebar when the sidebar toggle button is clicked
// * It also stores the state of the sidebar in the localstorage so that the sidebar state is maintained when the page is refreshed

// Constants
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const content = document.getElementById('content');
const footer = document.querySelector('footer');
const navTexts = document.querySelectorAll('.nav-text');
const navIcons = document.querySelectorAll('.nav-icon');
const navLinks = document.querySelectorAll('.nav-link');
const logoTitle = document.getElementById('logo-title');
const userTitle = document.getElementById('user-title');

// Initialise tooltips, overriding the default
$(sidebarToggle).tooltip(); // initialise sidebartoggle button tooltip
navLinks.forEach((navLink) => {
    $(navLink).tooltip(); // initialise jQuery tooltip
});

// Check if there isn't already a localstorage item sidebarExpanded, if not, create one
if (localStorage.getItem('sidebarExpanded') === null) {
    localStorage.setItem('sidebarExpanded', true); // set the default value to true
}

// Run the function on page load, once the page is loaded, the sidebar will be in the correct state
handleOnLoad();

// Check if the sidebar is collapsed or not within the same session, on page load/reload
if (localStorage.getItem('sidebarExpanded') === 'true') {
    sidebarExpand();
} else{
    sidebarCollapse();
}

// Add event listener to the sidebar toggle button
sidebarToggle.addEventListener('click', handleOnClick);

// * Functions
function handleOnLoad() {
    // Remove transition, so sidebar is in the right state when the page is loaded instantly
    sidebar.style.transition = 'none';
    sidebarToggle.style.transition = 'none';
    content.style.transition = 'none';
    footer.style.transition = 'none';

    // If expanded, add active class for instant load with no transition
    if (localStorage.getItem('sidebarExpanded') === 'true') {
        addActive();
        addActiveText();
    }

    // Restore transition after the sidebar is in place, so that the transition works when the sidebar is toggled
    setTimeout(() => {
        sidebar.style.transition = '';
        sidebarToggle.style.transition = '';
        content.style.transition = '';
        footer.style.transition = '';
        navIcons.forEach((navIcon) => {
            navIcon.style.transition = '';
        });
    }, 250);

}

function handleOnClick(){
    $(sidebarToggle).tooltip('hide'); // hide the tooltip when button clicked

    if (localStorage.getItem('sidebarExpanded') === 'true') {
        sidebarCollapse();
        localStorage.setItem('sidebarExpanded', false);
    } else{
        sidebarExpand();
        localStorage.setItem('sidebarExpanded', true);
    }
}

function removeActive(){
    sidebar.classList.remove('active');
    sidebarToggle.classList.remove('active');
    content.classList.remove('active');
    footer.classList.remove('active');
    navIcons.forEach((navIcon) => {
        navIcon.classList.remove('active');
    });
}

function removeActiveText(){
    logoTitle.classList.remove('active');
    userTitle.classList.remove('active');
    navTexts.forEach((navText) => {
        navText.classList.remove('active');
    });
}

function addActive(){
    sidebar.classList.add('active');
    sidebarToggle.classList.add('active');
    content.classList.add('active');
    footer.classList.add('active');
    navIcons.forEach((navIcon) => {
        navIcon.classList.add('active');
    });
}

function addActiveText(){
    logoTitle.classList.add('active');
    userTitle.classList.add('active');
    navTexts.forEach((navText) => {
        navText.classList.add('active');
    });
}

// * Sidebar toggle functions

function sidebarCollapse() {
    sidebarToggle.setAttribute('data-original-title', 'Expand Menu');
    removeActive();
    removeActiveText();

    // Add menu tooltips and load them
    navLinks.forEach((navLink) => {
        $(navLink).tooltip();
    }); 

}

function sidebarExpand() {
    sidebarToggle.setAttribute('data-original-title', 'Collapse Menu');
    addActive();

    // Remove menu tooltips and destroy them
    navLinks.forEach((navLink) => {
        $(navLink).tooltip('dispose');
    });    

    // Delay the transition of the logo title and nav text until the sidebar is expanded
    setTimeout(() => {
        addActiveText();
    }, 250);           
}