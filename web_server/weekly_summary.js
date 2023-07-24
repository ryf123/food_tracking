const loadWeeklySummaryData = () => {
  return fetch('/load_weekly_summary?user_id=200')
    .then(response => response.json())
    .catch(error => {
      console.error('Error:', error);
    });
};

const loadWeeklySummary = async () => {
  try {
    const data = await loadWeeklySummaryData();
    const tableBody = document.querySelector('#weeklySummaryTable tbody');
    data.forEach(item => {
      const row = document.createElement('tr');
      const calorie = Math.round(item.calorie);
      row.innerHTML = `
        <td>${item.week}</td>
        <td>${calorie}</td>
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
const loadAnalysisData = () => {
  return fetch('/load_nutrition_analysis?user_id=200')
    .then(response => response.json())
    .catch(error => {
      console.error('Error:', error);
    });
};

const loadAnalysis = async () => {
  try {
    const data = await loadAnalysisData();
    var divElement = document.getElementById("analysisResult");
    divElement.textContent = JSON.parse(JSON.stringify(data))['analysis'];
  } catch (error) {
    console.error('Error:', error);
  }
};
loadAnalysis();
loadWeeklySummary();
