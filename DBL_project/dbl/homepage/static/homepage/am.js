/**
 * Opens the popup that displays when hovering a cell in the adjacency matrix
 * @param {HTMLElement} matrixCell The cell that was hovered
 * @param {Array.<Object>} nodeInfo An array of node objects
 */
function enterCell(matrixCell, nodeInfo) {
  // Get the header & column id
  const headerId = getNodeIndex(matrixCell) - 1
  const columnId = getNodeIndex(matrixCell.closest("tr"))
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
    <br />
    <p><strong>Edge data</strong></p>
    <p>Average sentiment: -</p>
  `

  // Move the popup to the matrix cell
  const cellRect = matrixCell.getBoundingClientRect()
  edgeInfoPopup.style.left = cellRect.left + matrixCell.offsetWidth / 2 + 'px' // offsetWidth / 2 horizontally centers the popup
  edgeInfoPopup.style.top = cellRect.top - 80 + window.scrollY + 'px' // -80 is to account for the navbar, window.scrollY to prevent positioning issues
  edgeInfoPopup.style.transform = `translate(-50%, calc(-100% - ${matrixCell.offsetHeight / 2 + 'px'} + 4px))`

  // Display popup
  edgeInfoPopup.classList.add('show')
}


/**
 * Removes the popup that displays when hovering a cell in the adjacency matrix
 */
function exitCell() {
  // Hide the popup
  const edgeInfoPopup = document.querySelector('.edge-info-popup')
  edgeInfoPopup.classList.remove('show')
}


/**
 * Opens a modal that displays all of the emails in a list
 * @param {HTMLElement} matrixCell The cell that was hovered
 * @param {Array.<Object>} nodeInfo An array of node objects
 * @param {Array.<Array.<Number>>} edgeData An array of arrays, containing the edge data
 */
function clickCell(matrixCell, nodeInfo, edgeData) {
  // Get the header & column id
  const headerId = getNodeIndex(matrixCell) - 1
  const columnId = getNodeIndex(matrixCell.closest("tr"))

  console.log(edgeData[0])

  const edgesHTML = [`<tr>
            <td>Email #1</td>
            <td>0.918</td>
            <td>2000-08-13</td>
          </tr>`]

  openModal(`
    <h1>Emails from ${nodeInfo[columnId].id} to ${nodeInfo[headerId].id}</h1>
    <div class="modal-body">
      <p><strong>Sender</strong></p>
      <p>ID: ${nodeInfo[columnId].id}</p>
      <p>Email: ${nodeInfo[columnId].email}</p>
      <p>Job title: ${nodeInfo[columnId].job}</p>
      <br />
      <p><strong>Receiver</strong></p>
      <p>ID: ${nodeInfo[headerId].id}</p>
      <p>Email: ${nodeInfo[headerId].email}</p>
      <p>Job title: ${nodeInfo[headerId].job}</p>
      <br />
      <table class="email-list">
        <thead>
          <tr>
            <th>Email number</th>
            <th>Sentiment</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          ${edgesHTML.join('')}
        </tbody>
      </table>
    </div>
  `)

  // Close the modal if someone clicks outside of it
  const overlay = document.querySelector('.overlay')
  overlay.addEventListener('click', () => closeModal(300))
}


/**
 * Toggles between displaying emails or IDs on the table headers
 * @param {Boolean} state Whether or not to display as emails
 * @param {Array.<Object>} nodeInfo An array of node objects
 */
function toggleEmails(state, nodeInfo) {
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
const getNodeIndex = el => [...el.parentNode.children].indexOf(el)



function openModal(html) {
  // Initialize variables
  const overlay = document.querySelector('.overlay')
  const modal = document.querySelector('.modal');
  const modalContent = modal.querySelector('.modal-content')

  // Render the provided HTML into the modal
  modalContent.innerHTML = html

  // Display the modal & overlay
  overlay.style.display = 'block'
  modal.style.display = 'flex'
  setTimeout(() => overlay.classList.add('show'), 100)
  setTimeout(() => modal.classList.add('show'), 100)
}

function closeModal(animDuration) {
  // Initialize variables
  const overlay = document.querySelector('.overlay')
  const modal = document.querySelector('.modal')

  // Close the modal & overlay
  overlay.classList.remove('show')
  modal.classList.remove('show')

  setTimeout(() => {
    overlay.style.display = 'none'
    modal.style.display = 'none'
  }, animDuration)
}