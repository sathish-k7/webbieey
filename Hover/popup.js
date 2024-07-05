document.addEventListener('DOMContentLoaded', function() {
  let linksList = document.getElementById('links');


  chrome.storage.local.get('links', function(data) {
    let links = data.links || [];
    links.forEach(function(link) {
      let listItem = document.createElement('li');
      let linkElement = document.createElement('a');
      linkElement.href = link;
      linkElement.textContent = link;
      linkElement.target = '_blank';
      listItem.appendChild(linkElement);
      linksList.appendChild(listItem);
    });
  });


});