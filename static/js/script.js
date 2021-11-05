$(document).ready(function() {
    $(".sidenav").sidenav({edge: "right"})
})


function openForm() {
    document.getElementById("form").style.display = "block";
}

// Close button of the feedback
function closeForm() {
    document.getElementById("form").style.display = "none";
}