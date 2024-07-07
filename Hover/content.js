// ==UserScript==
// @name         Amazon Hover Popup with Stable Blur
// @namespace    http://tampermonkey.net/
// @version      1.9
// @description  Show popup on Amazon product hover and blur background with stable effect
// @author       Your Name
// @match        *://www.amazon.com/*
// @match        *://www.amazon.in/*
// @grant        none
// ==/UserScript==

(function () {
  "use strict";

  // Add styles for the blurred background and popup
  const style = document.createElement("style");
  style.innerHTML = `
      .blurred-background *:not(#hover-popup) {
          filter: blur(5px) !important;
          pointer-events: none; /* Prevents interaction with the blurred background */
      }
      #hover-popup {
          display: none;
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          background-color: white;
          padding: 20px;
          border: 1px solid black;
          z-index: 10000;
          width: 50%;
          height: 50%;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
          overflow: auto; /* Allows content overflow to be scrollable */
      }
  `;
  document.head.appendChild(style);

  // Create the popup element
  const popup = document.createElement("div");
  popup.id = "hover-popup";
  popup.innerText = ""; // Placeholder content
  document.body.appendChild(popup);

  let hoverTimeout;
  let isHovered = false;

  // Function to show the popup and blur the background
  function showPopup() {
    if (!isHovered) {
      document.body.classList.add("blurred-background");
      popup.style.display = "block";
      isHovered = true;
    }
  }

  // Function to hide the popup and remove the blur from the background
  function hidePopup() {
    if (isHovered) {
      document.body.classList.remove("blurred-background");
      popup.style.display = "none";
      isHovered = false;
    }
  }

  // Event listener to handle hover over product links
  document.addEventListener("mouseover", function (e) {
    const link = e.target.closest('a[href*="/dp/"], a[href*="/sspa/"]');
    if (link && (link.href.includes("/dp/") || link.href.includes("/sspa/"))) {
      clearTimeout(hoverTimeout);
      hoverTimeout = setTimeout(() => {
        showPopup();
        sendLinkToServer(link.href);
      }, 2000); // 2000 milliseconds = 2 seconds
    }
  });

  // Event listener to handle moving cursor away from product links
  document.addEventListener("mouseout", function (e) {
    const link = e.target.closest('a[href*="/dp/"], a[href*="/sspa/"]');
    if (link && (link.href.includes("/dp/") || link.href.includes("/sspa/"))) {
      clearTimeout(hoverTimeout);
      hoverTimeout = setTimeout(hidePopup, 300);
    }
  });

  // Keep the popup visible if the cursor is over it
  popup.addEventListener("mouseover", function () {
    clearTimeout(hoverTimeout);
  });

  popup.addEventListener("mouseout", function () {
    hoverTimeout = setTimeout(hidePopup, 300);
  });

  function sendLinkToServer(link) {
    fetch("http://127.0.0.1:5000/store_link", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ link: link }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => console.log("Link sent to server:", data))
      .catch((error) => console.error("Error sending link:", error));
  }
})();
