



document.addEventListener("htmx:beforeSwap", function (event) {
    var xhr = event.detail.xhr;

    // Check if the response is JSON
    if (xhr.getResponseHeader("Content-Type").includes("application/json")) {
        // Prevent HTMX from swapping the JSON response
        event.preventDefault();
        console.log("JSON response ignored.");
    }
});


document.addEventListener('DOMContentLoaded', function () {
    // Get the event section and announcement section
    var eventSection = document.getElementById('event-section');
    var clockerSection = document.getElementById('clocker-section')
    var announcementSection = document.getElementById('announcement-section');

    // Function to adjust the max-height of the announcement section
    function adjustAnnouncementMaxHeight() {
        // Get the height of the event section
        var eventHeight = eventSection.offsetHeight;
        var clockerHeight = clockerSection.offsetHeight;
        var calculateHeight = eventHeight - clockerHeight;
        // Set the max-height of the announcement section based on the event height
        // You can adjust the calculation as needed (e.g., subtract a margin)
        announcementSection.style.maxHeight = eventHeight - clockerHeight + 'px';
    }

    // Adjust the max-height on page load
    adjustAnnouncementMaxHeight();

    // Optional: If you plan to change the event section dynamically (e.g., adding/removing events),
    // you can call this function whenever the event section changes:
    // window.addEventListener('resize', adjustAnnouncementMaxHeight); // If window resizing matters
});
