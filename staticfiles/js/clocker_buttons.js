document.addEventListener('htmx:afterSwap', function(event) {
    if (event.target.matches('.response-message')) {
        const responseMessage = event.target;
        responseMessage.classList.add('show');
        
        // Hide the response message after 5 seconds
        setTimeout(() => {
            responseMessage.classList.remove('show');
        }, 3000); // 5000ms = 5 seconds
    }
});



// document.addEventListener('DOMContentLoaded', function() {
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }

//     const csrftoken = getCookie('csrftoken');

//     function handleClockAction(buttonId, url, redirectUrl) {
//         $(buttonId).click(function(e) {
//             e.preventDefault();
//             $.ajax({
//                 url: url,
//                 type: "POST",
//                 headers: {
//                     'X-CSRFToken': csrftoken
//                 },
//                 success: function(response) {
//                     if (response.status === 'confirm') {
//                         if (confirm(response.message)) {
//                             $.ajax({
//                                 url: url,
//                                 type: "POST",
//                                 data: { confirm: 'yes' },
//                                 headers: {
//                                     'X-CSRFToken': csrftoken
//                                 },
//                                 success: function(response) {
//                                     if (response.status === 'success') {
//                                         alert(response.message);
//                                         window.location.href = redirectUrl;
//                                     } else if (response.status === 'failure') {
//                                         alert(response.message);
//                                     } else if (response.status === 'warning') {
//                                         alert(response.message);    
//                                     } 
//                                 }
//                             });
//                         } else {
//                             window.location.href = redirectUrl;
//                         }
//                     } else if (response.status === 'success') {
//                         alert(response.message);
//                         window.location.href = redirectUrl;
//                     } else if (response.status === 'failure') {
//                         alert(response.message);
//                     } else if (response.status === 'warning') {
//                         alert(response.message);   
//                     }
//                 }
//             });
//         });
//     }

//     handleClockAction('#clockOutButton', clockOutUrl, redirectUrl);
//     handleClockAction('#clockInButton', clockInUrl, redirectUrl);
// });



