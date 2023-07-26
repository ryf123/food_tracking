const loadHistoryData = () => {
  return fetch('/load_history?user_id=200')
    .then(response => response.json())
    .catch(error => {
      console.error('Error:', error);
    });
};

const loadHistory = async () => {
  console.log("loadHistory func");
  try {
    const data = await loadHistoryData();
    const tableBody = document.querySelector('#calorieTable tbody');
    data.forEach(item => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${item.date}</td>
        <td>${item.calorie}</td>
      `;
      tableBody.appendChild(row);
    });
    for (const child of tableBody.children) {
      console.log(child.innerHTML);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
// Call the loadHistory function to initiate the data loading
loadHistory();
