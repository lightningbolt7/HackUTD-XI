async function getPredictions() {
    try {
        // URL of the backend endpoint
        const response = await fetch('http://127.0.0.1:5000/prediction', {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.text(); // Receive response from backend
        console.log(result); // e.g., "Predictions saved to PredictionResults.csv"

        // Display a message to the user
        alert('Predictions completed! Check the CSV file on the server.');
    } catch (error) {
        console.error('Error fetching predictions:', error);
        alert('Error fetching predictions. Check the console for details.');
    }
}

// Example button click to trigger prediction
document.getElementById('predictButton').addEventListener('click', getPredictions);
