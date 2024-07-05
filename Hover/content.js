let hoverTimer;
let currentLink;

// Event listener for mouseover event
document.body.addEventListener('mouseover', function(event) {
  let element = event.target;
  while (element) {
    if (element.tagName === 'A' && element.href) {
      currentLink = element.href;
      hoverTimer = setTimeout(fetchAndShowProductInfo, 2000); // 2000 milliseconds = 2 seconds
      break;
    }
    element = element.parentElement;
  }
});

// Event listener for mouseout event
document.body.addEventListener('mouseout', function(event) {
  clearTimeout(hoverTimer);
  // Check if the mouse has moved to the overlay itself
  let relatedTarget = event.relatedTarget;
  if (!relatedTarget || relatedTarget.id !== 'product-overlay') {
    hideProductOverlay();
  }
});

// Function to fetch and show product information
function fetchAndShowProductInfo() {
  fetch('http://127.0.0.1:5000/store_link', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ link: currentLink })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(productInfo => {
    showProductOverlay(productInfo);
  })
  .catch(error => {
    console.error('Error fetching product information:', error);
  });
}

// Function to show product overlay
function showProductOverlay(productInfo) {
  // Blur background
  document.body.style.filter = 'blur(5px)';

  // Check if overlay already exists
  let overlay = document.getElementById('product-overlay');
  
  if (!overlay) {
    // Create overlay div if it doesn't exist
    overlay = document.createElement('div');
    overlay.id = 'product-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '50%';
    overlay.style.left = '50%';
    overlay.style.transform = 'translate(-50%, -50%)';
    overlay.style.background = 'white';
    overlay.style.padding = '20px';
    overlay.style.zIndex = '9999';
    document.body.appendChild(overlay);

    // Prevent the overlay from hiding when hovering over it
    overlay.addEventListener('mouseover', function() {
      clearTimeout(hoverTimer);
    });
    overlay.addEventListener('mouseout', function() {
      hideProductOverlay();
    });
  }

  // Update overlay content
  overlay.innerHTML = `
    <h2>${productInfo.title}</h2>
    <p>${productInfo.description}</p>
    <p>Price: ${productInfo.price}</p>
    <p>Rating: ${productInfo.rating}</p>
  `;

  // Display overlay
  overlay.style.display = 'block';
}

// Function to hide product overlay
function hideProductOverlay() {
  // Hide overlay if it exists
  let overlay = document.getElementById('product-overlay');
  if (overlay) {
    overlay.style.display = 'none';
  }

  // Unblur background
  document.body.style.filter = 'none';
}

// Function for periodic updates of links
function periodicallySendLinks() {
  let links = []; // Placeholder for actual logic to collect links

  // Send links to Flask server
  fetch('http://127.0.0.1:5000/store_link', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ links: links })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => console.log('Links updated on server:', data))
  .catch(error => console.error('Error updating links:', error));
}

// Call periodicallySendLinks every 3 seconds (3000 milliseconds)
setInterval(periodicallySendLinks, 3000);
