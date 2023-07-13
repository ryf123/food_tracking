let mediaRecorder;
let recordedChunks = [];
let transcribed_texts = [{'text':'今天我吃了一个包子', 'total_calorie': 200}, {'text':'今天我吃了一个饺子', 'total_calorie': 100}];

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.addEventListener('dataavailable', handleDataAvailable);
    mediaRecorder.start();
    recordedChunks = []; // Clear the previous recording chunks
    document.getElementById('startButton').disabled = true;
    document.getElementById('stopButton').disabled = false;
    document.getElementById('saveButton').disabled = true;
    document.getElementById('audioPreview').src = '';
  } catch (error) {
    console.error('Error accessing microphone:', error);
  }
};

const stopRecording = () => {
  mediaRecorder.stop();
  mediaRecorder.stream.getTracks().forEach(track => track.stop());
  document.getElementById('startButton').disabled = false;
  document.getElementById('stopButton').disabled = true;
  document.getElementById('saveButton').disabled = false;
};

const handleDataAvailable = (event) => {
  recordedChunks.push(event.data);
};

const transcribe = () => {
  if(recordedChunks.length == 0){
    return;
  }

  const blob = new Blob(recordedChunks, { type: 'audio/webm' });
  const formData = new FormData();
  formData.append('audio', blob, 'recorded_audio.webm');

  fetch('/transcribe', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Handle the data returned by the API
    console.log(data);
    transcribed_texts.push(JSON.parse(JSON.stringify(data)));
    // Update the content of the transcribedText element
    updateTable(transcribed_texts);
  })
  .catch(error => {
    // Handle any errors that occurred during the request
    console.error('Error:', error);
  });
};

const saveLog = () => {
  const queryParams = new URLSearchParams();
  queryParams.append("text", JSON.stringify(transcribed_text));

  fetch('/db_save'+ "?" + queryParams.toString())
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
  })
  .catch(error => {
    // Handle any errors that occurred during the request
    console.error('Error:', error);
  });
};

const saveRecording = () => {
  const blob = new Blob(recordedChunks, { type: 'audio/webm' });
  const url = URL.createObjectURL(blob);
  document.getElementById('audioPreview').src = url;
  document.getElementById('audioPreview').controls = true;
  const link = document.createElement('a');
  link.href = url;
  link.download = 'recorded_audio.webm';
  link.click();
};

const updateTable = (arrayData) => {
    // Convert the array to a table
    var tableHtml = '<table id="selectableTable">';
    tableHtml += '<thead><tr><th>#</th><th>Transcribed Text</th><th>Calories</th></thead>';
    tableHtml += '<tbody>';
    var total_calorie = 0;
    for (var i = 0; i < arrayData.length; i++) {
        tableHtml += '<tr>';
        tableHtml += '<td>' + (i+1) + '</td>';
        tableHtml += '<td contentEditable="true">' + arrayData[i]['text'] + '</td>';
        tableHtml += '<td>' + arrayData[i]['total_calorie'] + '</td>';
        tableHtml += '</tr>';
        total_calorie += arrayData[i]['total_calorie'];
    }
    tableHtml += '<tr><td>#</td><td>Total Calorie</td><td>' + total_calorie + '</td></tr>';
    tableHtml += '</tbody>';
    tableHtml += '</table>';

    // Display the table on the page
    var tableContainer = document.getElementById('table-container');
    tableContainer.innerHTML = tableHtml;

    var table = document.getElementById('selectableTable');
    var rows = table.getElementsByTagName('tr');

    for (var i = 0; i < rows.length - 1; i++) {
        rows[i].addEventListener('click', function() {
            // Deselect all other rows
            for (var j = 0; j < rows.length; j++) {
                rows[j].classList.remove('selected');
            }

            // Select the clicked row
            this.classList.add('selected');
        });
    }
}
updateTable(transcribed_texts);
var removeButton = document.getElementById('RemoveButton');
removeButton.addEventListener('click', function() {
    var table = document.getElementById('selectableTable');
    var selectedRow = table.querySelector('tr.selected');
    if (selectedRow) {
        selectedRow.remove();
        var rowData = Array.from(selectedRow.cells).map(cell => cell.textContent);
        var index = rowData[0];
        transcribed_texts.splice(index - 1, index);
    } else {
        console.log('No row selected.');
    }
});
var calculateButtonButton = document.getElementById('CalculateButton');
calculateButtonButton.addEventListener('click', function() {
    var table = document.getElementById('selectableTable');
    var selectedRow = table.querySelector('tr.selected');
    if (selectedRow) {
        var rowData = Array.from(selectedRow.cells).map(cell => cell.textContent);

        var requestOptions = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json' // Set the appropriate content type
          },
          body: JSON.stringify({'transcribed_text': rowData[1]}) // Convert the parameters to a JSON string
        };
        fetch('/calculate_calorie', requestOptions)
        .then(response => response.json())
        .then(data => {
          // Handle the response data
          console.log(data);
          const cells = selectedRow.cells;
          cells[1].innerHTML = JSON.parse(JSON.stringify(data))['total_calorie'];
        })
        .catch(error => {
          // Handle any errors
          console.error('Error:', error);
        });
    } else {
        console.log('No row selected.');
    }
});

document.getElementById('startButton').addEventListener('click', startRecording);
document.getElementById('stopButton').addEventListener('click', stopRecording);
document.getElementById('saveButton').addEventListener('click', saveRecording);
document.getElementById('transcribe').addEventListener('click', transcribe);
document.getElementById('saveLog').addEventListener('click', saveLog);