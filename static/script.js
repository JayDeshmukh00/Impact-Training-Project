window.onload = function() {
    fetch('/api/transactions')
        .then(response => response.json())
        .then(data => {
            let categories = {};
            data.forEach(transaction => {
                if (transaction.type === 'expense') {
                    categories[transaction.category] = (categories[transaction.category] || 0) + transaction.amount;
                }
            });

            const ctx = document.getElementById('categoryChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(categories),
                    datasets: [{
                        label: 'Expenses by Category',
                        data: Object.values(categories),
                        backgroundColor: ['#FF5733', '#33FF57', '#3357FF', '#FF33A1'],
                        borderWidth: 1
                    }]
                }
            });
        });
};
