/**
 * Opens the popup that displays when hovering a cell in the adjacency matrix
 * @param {Event} e The hover event
 * @param {Array.<Object>} nodeInfo An array of node objects
 */
function enterCell(e, matrixCell, nodeInfo) {
  // Get the header & column id
  const headerId = getNodeindex(matrixCell) - 1
  const columnId = getNodeindex(e.target.closest("tr"))
  const edgeInfoPopup = document.querySelector('.edge-info-popup')

  // Fill the popup with data
  edgeInfoPopup.innerHTML = `
    <p><strong>Sender</strong></p>
    <p>ID: ${nodeInfo[columnId].id}</p>
    <p>Email: ${nodeInfo[columnId].email}</p>
    <p>Job title: ${nodeInfo[columnId].job}</p>
    <br />
    <p><strong>Receiver</strong></p>
    <p>ID: ${nodeInfo[headerId].id}</p>
    <p>Email: ${nodeInfo[headerId].email}</p>
    <p>Job title: ${nodeInfo[headerId].job}</p>
  `

  // Move the popup to the matrix cell
  const cellRect = matrixCell.getBoundingClientRect()
  edgeInfoPopup.style.left = cellRect.left + matrixCell.offsetWidth / 2 + 'px' // offsetWidth / 2 horizontally centers the popup
  edgeInfoPopup.style.top = cellRect.top - 80 + window.scrollY + 'px' // -80 is to account for the navbar, window.scrollY to prevent positioning issues
  edgeInfoPopup.style.transform = `translate(-50%, calc(-100% - ${matrixCell.offsetHeight / 2 + 'px'}))`

  // Display popup
  edgeInfoPopup.classList.add('show')
}


/**
 * Removes the popup that displays when hovering a cell in the adjacency matrix
 * @param {Event} e The hover event
 */
function exitCell(e) {
  // Hide the popup
  const edgeInfoPopup = document.querySelector('.edge-info-popup')
  edgeInfoPopup.classList.remove('show')
}


/**
 * Toggles between displaying emails or IDs on the table headers
 * @param {Boolean} state Whether or not to display as emails
 * @param {Array.<Object>} nodeInfo An array of node objects
 */
function toggleEmails(state, nodeInfo) {
  const topHeader = document.querySelector('.adjacency-matrix thead')
  const topHeaderElements = document.querySelectorAll('.adjacency-matrix thead th:not(:first-child) span')
  const leftHeaderElements = document.querySelectorAll('.adjacency-matrix tbody th')

  
  topHeaderElements.forEach((el, index) => {
    if (state) el.innerText = nodeInfo[index].email
    else el.innerText = nodeInfo[index].id
  })

  leftHeaderElements.forEach((el, index) => {
    if (state) el.innerText = nodeInfo[index].email
    else el.innerText = nodeInfo[index].id
  })
}

// A function to find a node's index within its parent element
const getNodeindex = elm => [...elm.parentNode.children].findIndex(c => c == elm)