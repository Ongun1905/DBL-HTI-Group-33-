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
  edgeInfoPopup.style.left = matrixCell.offsetLeft + matrixCell.offsetWidth / 2 + 'px' // offsetWidth is to put it in the horizontal middle
  edgeInfoPopup.style.top = matrixCell.offsetTop - 80 + 'px' // -80 is to account for the navbar
  edgeInfoPopup.style.transform = `translate(-50%, calc(-50% - ${matrixCell.offsetHeight / 2 + 'px'} - 16px))`

  // Display popup
  edgeInfoPopup.classList.add('show')

  // Console log for debugging
  console.log(`You hovered the cell at (x, y) = (${columnId}, ${headerId})`)
  console.log(`This cell represents all emails from ${nodeInfo[columnId].id} (${nodeInfo[columnId].email}) to ${nodeInfo[headerId].id} (${nodeInfo[headerId].email})`)
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