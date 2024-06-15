function fetchData() {
    const rankSelect = document.getElementById('rankSelect').value;
    const branchSelect = document.getElementById('branchSelect').value;

    if (rankSelect === 'Select' || branchSelect === 'Select') {
        alert('Please select both rank range and branch.');
        return;
    }

    fetch(`/fetch-data/?rank=${rankSelect}&branch=${branchSelect}`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('myChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Closing Rank',
                        data: data.values,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}






