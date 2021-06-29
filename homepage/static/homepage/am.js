// Global variables
var cellHoverTimeout

/**
 * Opens the popup that displays when hovering a cell in the adjacency matrix
 * 
 * @param {HTMLElement} matrixCell The cell that was hovered
 * @param {Array.<Object>} nodeData An array of node objects
 */
function enterCell(matrixCell, nodeData, edgeData) {
  cellHoverTimeout = setTimeout(() => {
    displayPopup(matrixCell, nodeData, edgeData)
  }, 400)
}


function displayPopup(matrixCell, nodeData, edgeData) {
  // Get the header & column id
  const rowId = matrixCell.dataset.columnIndex
  const colId = matrixCell.dataset.rowIndex
  const edgeInfoPopup = document.querySelector('.edge-info-popup')

  // Calculate average sentiment
  const relatedEdgeData = edgeData.filter(item => item[0] === nodeData[colId].id && item[1] === nodeData[rowId].id).map(item => item[2])
  const averageSentiment = relatedEdgeData.length === 0 ? 0 : roundTo(relatedEdgeData.reduce((a, b) => a + (b['sentiment'] || 0), 0) / relatedEdgeData.length, 3)

  // Fill the popup with data
  edgeInfoPopup.innerHTML = `
    <p><strong>Sender</strong></p>
    <p>ID: ${nodeData[colId].id}</p>
    <p>Email: ${nodeData[colId].email}</p>
    <p>Job title: ${nodeData[colId].job}</p>
    <br />
    <p><strong>Receiver</strong></p>
    <p>ID: ${nodeData[rowId].id}</p>
    <p>Email: ${nodeData[rowId].email}</p>
    <p>Job title: ${nodeData[rowId].job}</p>
    <br />
    <p><strong>Edge data</strong></p>
    <p>Average sentiment: ${averageSentiment}</p>
  `

  // Move the popup to the matrix cell
  const cellRect = matrixCell.getBoundingClientRect()
  edgeInfoPopup.style.left = cellRect.left + matrixCell.offsetWidth / 2 + 'px' // offsetWidth / 2 horizontally centers the popup

  // Change the top distance based on whether or not it's in the combined view
  // -80 is to account for the navbar, window.scrollY to prevent positioning issues
  const topDistance = cellRect.top - 80 + window.scrollY
  edgeInfoPopup.style.top = topDistance + 'px'
  
  // Set translate property to the :root element
  document.documentElement.style.setProperty('--translate-eip', `translate(-50%, calc(-100% - ${matrixCell.offsetHeight / 2 + 'px'} + 4px))`)

  // Display popup
  edgeInfoPopup.classList.add('show')
}


/**
 * Removes the popup that displays when hovering a cell in the adjacency matrix
 */
function exitCell() {
  // Remove the hover timeout
  clearTimeout(cellHoverTimeout)
  cellHoverTimeout = undefined

  // Hide the popup
  const edgeInfoPopup = document.querySelector('.edge-info-popup')
  edgeInfoPopup.classList.remove('show')
}


/**
 * Opens a modal that displays all of the emails in a list
 * 
 * @param {HTMLElement} matrixCell The cell that was hovered
 * @param {Array.<Object>} nodeData An array of node objects
 * @param {Array.<Array.<Number>>} edgeData An array of arrays, containing the edge data
 */
function clickCell(matrixCell, nodeData, edgeData) {
  // Get the header & column id
  const rowId = matrixCell.dataset.columnIndex
  const colId = matrixCell.dataset.rowIndex
  const relatedEdgeData = edgeData.filter(item => item[0] === nodeData[colId].id && item[1] === nodeData[rowId].id).map(item => item[2])

  let emailListHTML = []
  relatedEdgeData.forEach((el, index) => {
    emailListHTML.push(`
      <tr>
        <td>${index + 1}</td>
        <td class="${el.sentiment < 0 ? 'negative' : el.sentiment > 0 ? 'positive' : ''}">${roundTo(el.sentiment, 3)}</td>
        <td>${el.messageType}</td>
        <td>${el.date}</td>
      </tr>
    `)
  })

  let emailTableHTML = `
    <table class="email-list custom-scrollbar">
      <thead>
        <tr>
          <th style="width: 100%;" onclick="onColumnHeaderClicked(event)" >Email number</th>
          <th onclick="onColumnHeaderClicked(event)">Sentiment</th>
          <th onclick="onColumnHeaderClicked(event, 'string')">Type</th>
          <th onclick="onColumnHeaderClicked(event, 'date')">Date</th>
        </tr>
      </thead>
      <tbody>
        ${emailListHTML.join('')}
      </tbody>
    </table>
  `

  openModal(`
    <h1>Emails from ${nodeData[colId].id} to ${nodeData[rowId].id}</h1>
    <div class="modal-body">
      <div class="col-2">
        <div>
          <p><strong>Sender</strong></p>
          <p>ID: ${nodeData[colId].id}</p>
          <p>Email: ${nodeData[colId].email}</p>
          <p>Job title: ${nodeData[colId].job}</p>
        </div>
        <div>
          <p><strong>Receiver</strong></p>
          <p>ID: ${nodeData[rowId].id}</p>
          <p>Email: ${nodeData[rowId].email}</p>
          <p>Job title: ${nodeData[rowId].job}</p>
        </div>
      </div>
      ${emailListHTML.length > 0 ? emailTableHTML : '<p class="no-emphasis">No emails found!</p>'}
    </div>
  `, 'edge-info-modal')

  // Close the modal if someone clicks outside of it
  const overlay = document.querySelector('.overlay')
  overlay.addEventListener('click', () => closeModal(300))
}


function sortTableRowsByColumn(table, columnIndex, ascending, type) {

  const rows = Array.from(table.querySelectorAll(':scope > tbody > tr'))

  rows.sort((x, y) => {
    const xValue = x.cells[columnIndex].textContent
    const yValue = y.cells[columnIndex].textContent

    // Handle explicit data types
    if (type === 'date') {
      const xDate = new Date(xValue)
      const yDate = new Date(yValue)

      return ascending ? (xDate - yDate) : (yDate - xDate)
    } else if (type === 'string') {
      const xString = xValue
      const yString = yValue

      return ascending ? (xString > yString) ? 1 : -1 : (yString > xString) ? 1 : -1
    }

    // Assuming values are numeric (use parseInt or parseFloat):
    const xNum = parseFloat(xValue)
    const yNum = parseFloat(yValue)

    return ascending ? (xNum - yNum) : (yNum - xNum)
  });

  for (let row of rows) {
    table.tBodies[0].appendChild(row)
  }
}

function onColumnHeaderClicked(ev, type) {

  const th = ev.currentTarget
  const table = th.closest('table')
  const thIndex = Array.from(th.parentElement.children).indexOf(th)

  const ascending = (th.dataset).sort != 'asc'

  sortTableRowsByColumn(table, thIndex, ascending, type)

  const allTh = table.querySelectorAll(':scope > thead > tr > th')
  for (let th2 of allTh) {
    delete th2.dataset['sort']
  }

  th.dataset['sort'] = ascending ? 'asc' : 'desc'
}


/**
 * Toggles between displaying emails or IDs on the table headers
 * 
 * @param {Boolean} state Whether or not to display as emails
 * @param {Array.<Object>} nodeData An array of node objects
 */
function toggleEmails(state, nodeData) {
  // Select the header elements
  const topHeaderElements = document.querySelectorAll('.adjacency-matrix thead th:not(:first-child) span')
  const leftHeaderElements = document.querySelectorAll('.adjacency-matrix tbody th')
  
  // For every header element, set the innerText to either the email or the ID
  topHeaderElements.forEach((el, index) => {
    if (state) el.innerText = nodeData[index].email
    else el.innerText = nodeData[index].id
  })

  leftHeaderElements.forEach((el, index) => {
    if (state) el.innerText = nodeData[index].email
    else el.innerText = nodeData[index].id
  })
}


/**
 * Removes all empty rows from the HTML table
 * 
 * @param {Array.<Object>} nodeData An array of node objects
 * @param {Array.<Array>} edgeData An array of the form [senderId, receiverId, {data}]
 */
function removeEmptyRows(nodeData, edgeData) {
  nodeData.forEach(node => {
    // For each node, try to find if there are outgoing edges in the list
    const outgoingEdge = edgeData.find(edge => edge[0] === node.id)

    // If nothing has been found, the row has to be removed
    if (!outgoingEdge) {
      const elToRemove = document.getElementById(`node-${node.id}`)
      if (elToRemove) elToRemove.style.display = 'none'
    }
  })
}


/**
 * Recolors the given matrix cell by sentiment value. A negative value
 * will display like red and a positive value will display like green.
 * 
 * @param {HTMLElement} matrixCells All cells in the matrix
 */
function sentimentColoring(matrixCells) {
  console.log('Coloring by sentiment...')

  matrixCells.forEach(cell => cell.style.backgroundColor = cell.dataset.averageSentiment > 0 ? `rgba(101, 204, 169, ${cell.dataset.averageSentiment})` : `rgba(204, 102, 136, ${-cell.dataset.averageSentiment})`)

  console.log('Done! The data is now colored by sentiment.')
}


/**
 * Recolors the given matrix cell by edge count. This value is stored
 * in the dataset by the Django template. It's already normalized
 * between 0 and 1.
 * 
 * @param {HTMLElement} matrixCells All cells in the matrix
 */
function edgeCountColoring(matrixCells) {
  matrixCells.forEach(cell => cell.style.backgroundColor = `rgba(101, 204, 169, ${cell.dataset.edgeCountNorm})`)
}


// ------------------------------------------------------------
// Helper functions
//
// The helper functions below are meant to improve readability
// because of their more descriptive function names and make
// certain actions more easily repeatable.
// ------------------------------------------------------------
/**
 * Rounds a number to a certain amount of decimals
 * 
 * @param {Number} number The number to round
 * @param {Number} decimals The amount of decimals to round to
 */
function roundTo(number, decimals) {
  return Math.round((number + Number.EPSILON) * 10 ** decimals) / 10 ** decimals
}


/**
 * Displays a modal over the webpage to get the attention of the user
 *
 * @param {String} html The HTML to be displayed within the modal
 * @param {String} className The class name(s) to be given to the modal for styling purposes
 */
function openModal(html, className) {
  // Initialize variables
  const overlay = document.querySelector('.overlay')
  const modal = document.querySelector('.modal');
  const modalContent = modal.querySelector('.modal-content')

  // Render the provided HTML into the modal
  modalContent.innerHTML = html
  modal.classList.add(className)

  // Display the modal & overlay
  overlay.style.display = 'block'
  modal.style.display = 'flex'
  setTimeout(() => overlay.classList.add('show'), 100)
  setTimeout(() => modal.classList.add('show'), 100)
}


/**
 * Hides the displayed modal
 *
 * @param {Number} animDuration The duration of the fade-out animation
 */
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

    // Remove potential added classes
    modal.className = 'modal'
  }, animDuration)
}