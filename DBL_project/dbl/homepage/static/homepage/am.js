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
  edgeInfoPopup.style.top = cellRect.top - 80 + window.scrollY + 'px' // -80 is to account for the navbar, window.scrollY to prevent positioning issues
  
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
        <td>Email #${index + 1}</td>
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
          <th style="width: 100%;">Email number</th>
          <th>Sentiment</th>
          <th>Type</th>
          <th>Date</th>
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
 * @param {Array.<Object>} nodeData An array of node objects
 * @param {Array.<Array>} edgeData An array of the form [senderId, receiverId, {data}]
 */
function sentimentColoring(matrixCells, nodeData, edgeData) {
  console.log('Coloring by sentiment...')

  // Fetch sentiment values
  let sentimentValues = []
  let sentimentValuesAbs = []
  matrixCells.forEach(cell => {
    // Get the header & column id
    const rowId = cell.dataset.columnIndex
    const colId = cell.dataset.rowIndex

    // Fetch the average sentiment of the cell
    const relatedEdgeData = edgeData.filter(item => item[0] === nodeData[colId].id && item[1] === nodeData[rowId].id).map(item => item[2])
    const averageSentiment = relatedEdgeData.length === 0 ? 0 : relatedEdgeData.reduce((a, b) => a + (b['sentiment'] || 0), 0) / relatedEdgeData.length
    const maxSentiment = 1

    // Push sentiment to the global array
    sentimentValues.push(averageSentiment)
    sentimentValuesAbs.push(Math.abs(averageSentiment))

    // Normalize to 1 instead of max
    const normalizedVal = 0.25 * logb(15 * Math.abs(averageSentiment) + 1, maxSentiment + 1)

    if (averageSentiment < 0) cell.style.backgroundColor = `rgba(204, 102, 136, ${normalizedVal})`
    else cell.style.backgroundColor = `rgba(101, 204, 169, ${normalizedVal})`
  })

  // Find the maximum sentiment value
  const maxSentimentValue = 1 /*arrayMax(sentimentValuesAbs)*/

  // Normalizing the sentiment value logarithmically and setting the background color of cells
  matrixCells.forEach((cell, index) => {
    const averageSentiment = sentimentValues[index]
    const normalizedVal = 0.25 * logb(15 * Math.abs(averageSentiment) + 1, maxSentimentValue + 1)

    if (averageSentiment < 0) cell.style.backgroundColor = `rgba(204, 102, 136, ${normalizedVal})`
    else cell.style.backgroundColor = `rgba(101, 204, 169, ${normalizedVal})`
  })
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
// NX graph manipulation functions
//
// These functions are used to manipulate the NX graph
// from JS. It's not meant to replace the Dash controls,
// only used to interact with the AM on the vis2 page
// ------------------------------------------------------------


/**
 * Dual input sliders
 */
const sliders = document.querySelectorAll('.dual-range-slider')

// Support for multiple sliders
sliders.forEach(slider => {
  const minRange = slider.querySelector('.min-range')
  const maxRange = slider.querySelector('.max-range')
  const children = slider.childNodes[1].childNodes

  minRange.addEventListener('input', () => {
    // Make sure the sliders don't cross eachother
    const minValue = Math.min(minRange.value, maxRange.value)
    minRange.value = minValue

    // Set width of slider elements
    const value = minValue / parseInt(minRange.max) * 100
    children[1].style.width = value + '%'
    children[5].style.left = value + '%'
    children[7].style.left = value + '%'
    // children[11].style.left = value + '%'
    // children[11].childNodes[1].innerHTML = minValue // Set bubble text


    // If the thumb handles are on top of eachother,
    // give the most recently changed thumb handle height priority
    if (Math.abs(minRange.value - maxRange.value) === 0) {
      children[7].style.zIndex = 1
      children[9].style.zIndex = 0
      minRange.style.zIndex = 1
      maxRange.style.zIndex = 0
    } else {
      children[7].style.zIndex = 3
      children[9].style.zIndex = 3
      minRange.style.zIndex = 3
      maxRange.style.zIndex = 3
    }
  })

  maxRange.addEventListener('input', () => {
    // Make sure the sliders don't cross eachother
    const maxValue = Math.max(minRange.value, maxRange.value)
    maxRange.value = maxValue

    // Set width of slider elements
    let value = maxValue / parseInt(maxRange.max) * 100
    children[3].style.width = 100 - value + '%'
    children[5].style.right = 100 - value + '%'
    children[9].style.left = value + '%'
    // children[13].style.left = value + '%'
    // children[13].childNodes[1].innerHTML = maxValue // Set bubble text

    // If the thumb handles are on top of eachother,
    // give the most recently changed thumb handle height priority
    if (Math.abs(minRange.value - maxRange.value) === 0) {
      children[9].style.zIndex = 1
      children[7].style.zIndex = 0
      maxRange.style.zIndex = 1
      minRange.style.zIndex = 0
    } else {
      children[9].style.zIndex = 3
      children[7].style.zIndex = 3
      maxRange.style.zIndex = 3
      minRange.style.zIndex = 3
    }
  })

  minRange.addEventListener('input', () => console.log(`(${normalizeToSentiment(minRange.value)}, ${normalizeToSentiment(maxRange.value)})`))
  maxRange.addEventListener('input', () => console.log(`(${normalizeToSentiment(minRange.value)}, ${normalizeToSentiment(maxRange.value)})`))
})


const normalizeToSentiment = (value) => {
  // Value is between 0 and 100
  return roundTo(value / 50 - 1, 1)
}


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
 * 
 * @param {Number} x Number to apply the logarithm to
 * @param {Number} y The base of the logarithm
 * @returns
 */
const logb = (x, y) => Math.log(x) / Math.log(y)

/**
 * Find and return the maximal value of the array
 * 
 * @param {Array.<Number>} array Array of numbers
 * @returns Maximal element of the given array
 */
function arrayMax(array) {
  return array.reduce(function (p, v) {
    return (p > v ? p : v);
  });
}


// A function to find a node's index within its parent element
// Watch out when using this in the matrix table, since it's a
// huge HTML element and is therefore pretty slow
/**
 * 
 * @param {Array.<HTMLElement>} el 
 * @returns 
 */
const getNodeIndex = el => [...el.parentNode.children].indexOf(el)



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