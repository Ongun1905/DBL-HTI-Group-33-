/**
 * File selection handling
 * 
 * Files can be selected by pressing the "pick file" button,
 * which changes a bunch of text and sets up the upload button
 * for submission.
 */
const body = document.querySelector('body')
const upload = document.querySelector('.upload')
const uploadButtonText = document.querySelector('.upload-button-text')
const uploadFilename = document.querySelector('.upload-filename')
const fileInput = document.getElementById('upload-file')
const submitButton = document.getElementById('submit-upload-file')

fileInput.onchange = () => uploadFile(fileInput.files[0], false)


function uploadFile(file, programmatically, dtFiles) {
  if (file) {
    uploadFilename.classList.remove('inactive')

    uploadFilename.innerText = file.name
    uploadButtonText.innerText = 'Upload'

    fileInput.style.display = 'none'
    uploadButtonText.setAttribute('for', '')

    uploadButtonText.addEventListener("click", async () => {
      upload.classList.add("uploading")
      if (programmatically) {
        fileInput.files = dtFiles
      }
      submitButton.click()
    })
  }
}


/**
 * Drop handling
 * 
 * Files can also be selected by dragging and dropping them over the
 * file selection/file upload element. This part of the JS code
 * handles all of that.
 */
const dropArea = document.querySelector('.drop-area')

// Remove bubbling for all drag events (unnecessary and slows down the webpage)
;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => dropArea.addEventListener(eventName, preventDefaults, false))

function preventDefaults(e) {
  e.preventDefault()
  e.stopPropagation()
}

// Add dashed borders to the droparea when dragging a file over the webpage
;['dragenter', 'dragover'].forEach(eventName => body.addEventListener(eventName, displayDropArea, false))
;['dragleave', 'drop'].forEach(eventName => body.addEventListener(eventName, hideDropArea, false))

// Change the color of the dashed border of the dropArea when dragging a file over the dropArea itself
;['dragenter', 'dragover'].forEach(eventName => dropArea.addEventListener(eventName, highlight, false))
;['dragleave', 'drop'].forEach(eventName => dropArea.addEventListener(eventName, unhighlight, false))


function highlight(e) {
  dropArea.classList.add('highlight')
}

function unhighlight(e) {
  dropArea.classList.remove('highlight')
}

function displayDropArea() {
  if (!dropArea.classList.contains('highlight')) dropArea.classList.add('droppable')
}

function hideDropArea() {
  dropArea.classList.remove('droppable')
}

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false)

function handleDrop(e) {
  let dt = e.dataTransfer
  let file = dt.files[0]

  uploadFile(file, true, dt.files)
}