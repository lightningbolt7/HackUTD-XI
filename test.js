async function getPredictions() {
    try {
        const response = await fetch('http://127.0.0.1:5000/prediction', {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.text();
        console.log(result);

        alert('Predictions completed! Check the CSV file on the server.');
    } catch (error) {
        console.error('Error fetching predictions:', error);
        alert('Error fetching predictions. Check the console for details.');
    }
}

document.getElementById('predictButton').addEventListener('click', getPredictions);
