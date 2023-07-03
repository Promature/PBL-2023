document.getElementById('submitBtn').addEventListener('click', function(event) {
  event.preventDefault(); // Prevent the default form submission

  var form = document.querySelector('.needs-validation');
  if (!form.checkValidity()) {
    // If the form is invalid, display the validation messages
    form.classList.add('was-validated');
    return;
  }
  //gather data
  var firstName = document.getElementById('firstName').value;
  var lastName = document.getElementById('lastName').value;
  var email = document.getElementById('email').value;
  var address = document.getElementById('address').value;
  var city = document.getElementById('city').value;
  var state = document.getElementById('state').value;
  var zip = document.getElementById('zip').value;


  var data = {
    firstName: firstName,
    lastName: lastName,
    email: email,
    address: address,
    city: city,
    state: state,
    zip: zip
  };

  // Get the CSRF token from the cookie
  var csrftoken = getCookie('csrftoken');

  // Send an AJAX request to your Django backend
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'save-shipping-address/', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.setRequestHeader('X-CSRFToken', csrftoken); // Include the CSRF token in the request headers
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      // Handle the response here if needed
      var response = JSON.parse(xhr.responseText);
      console.log(response);
    }
  };
  xhr.send(JSON.stringify(data));
});

// Function to get the CSRF token from the cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
