var table = document.getElementById("table");
var carbs=0, proteins=0, fats=0, calories=0;

for(var i=1; i<table.rows.length-1; i++){
    carbs += parseFloat(table.rows[i].cells[1].innerHTML);
    proteins += parseFloat(table.rows[i].cells[2].innerHTML);
    fats += parseFloat(table.rows[i].cells[3].innerHTML);
    fats = Math.round(fats)
    calories += parseFloat(table.rows[i].cells[4].innerHTML);
}

document.getElementById("totalCarbs").innerHTML = '<b>' + carbs + '(gm)</b>';
document.getElementById("totalProteins").innerHTML = '<b>' + proteins + '(gm)</b>';
document.getElementById("totalFats").innerHTML = '<b>' + fats + '(gm)</b>';
document.getElementById("totalCalories").innerHTML = '<b>' + calories + '(kcal)</b>';


var ctxPie = document.getElementById('pieChart').getContext('2d');
var myPieChart = new Chart(ctxPie, {
    type: 'pie',
    data: {
        labels: ['Carbs ', 'Fats ', 'Proteins '],
        datasets: [{
            data: [carbs, fats, proteins],
            backgroundColor: [
                'rgba(255, 140, 35, 0.6)',
                'rgba(200, 50, 35, 0.6)',
                'rgba(40, 140, 35, 0.6)',
            ],
            borderColor: [
                'rgba(255, 140, 35, 0.9)',
                'rgba(200, 50, 35, 0.9)',
                'rgba(40, 140, 35, 0.9)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += new Intl.NumberFormat('en-US', { style: 'unit', unit: 'gram' }).format(context.parsed.y);
                        }
                        return label;
                    }
                }
            }
        }
    }
});

fetch('/nutrient-summary-data/')
    .then(response => response.json())
    .then(data => {
        // Sum consumed nutrients
        let totalCarbs = data.carbs;
        let totalProteins = data.proteins;
        let totalFats = data.fats;
        let totalCalories = data.calories;

        // Update pie chart data with percentages after fetching latest data
        let totalMacro = totalCarbs+totalFats+totalProteins;
        let carbsP = totalMacro > 0 ? Math.round((totalCarbs/totalMacro)*100) : 0;
        let fatsP = totalMacro > 0 ? Math.round((totalFats/totalMacro)*100) : 0;
        let proteinsP = totalMacro > 0 ? Math.round((totalProteins/totalMacro)*100) : 0;

        myPieChart.data.datasets[0].data = [totalCarbs, totalFats, totalProteins];
        myPieChart.data.labels = ['Carbs '+carbsP+'%', 'Fats '+fatsP+'%', 'Proteins '+proteinsP+'%'];
        myPieChart.update();


        // Goal values
        let goalCalories = data.goal_calories;
        let goalCarbs = data.goal_carbs;
        let goalFats = data.goal_fats;
        let goalProteins = data.goal_proteins;


        // Update calorie progress bar
        var calPer = (totalCalories / goalCalories)*100;
        document.getElementsByClassName("progress-bar")[0].setAttribute("style", "width:"+calPer+"%");
        var innerProgress = document.getElementById("innerProgress");
        innerProgress.innerHTML = ('~'+Math.round(calPer)+ "% out of daily goal: " + goalCalories + " kcal");


    });


fetch('/chart-data/')
    .then(response => response.json())
    .then(data => {
        // Create a bar chart for goal tracking
        new Chart(document.getElementById('goalBarChart'), {
            type: 'bar',
            data: {
                labels: ['Calories', 'Carbs', 'Proteins', 'Fats'],
                datasets: [
                    {
                        label: 'Consumed',
                        data: [data.calories.reduce((a, b) => a + b, 0) , data.carbs.reduce((a, b) => a + b, 0), data.proteins.reduce((a, b) => a + b, 0), data.fats.reduce((a, b) => a + b, 0)],
                        backgroundColor: 'rgba(54, 162, 235, 0.7)'
                    },
                    {
                        label: 'Goal',
                        data: [data.goal_calories, data.goal_carbs, data.goal_proteins, data.goal_fats],
                        backgroundColor: 'rgba(255, 99, 132, 0.7)'
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    if (context.label === 'Calories')
                                        label += new Intl.NumberFormat('en-US', { style: 'unit', unit: 'kilocalorie' }).format(context.parsed.y);
                                    else
                                        label += new Intl.NumberFormat('en-US', { style: 'unit', unit: 'gram' }).format(context.parsed.y);
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
    });

// --- Line Chart with Trend Line JavaScript ---
fetch('/line-chart-data/')
    .then(response => response.json())
    .then(data => {
        // Calculate moving average for trend line (simple 3-day moving average)
        const trendData = [];
        for (let i = 0; i < data.calories.length; i++) {
            let sum = 0;
            let count = 0;
            for (let j = Math.max(0, i - 2); j <= i; j++) { // 3-day window
                sum += data.calories[j];
                count++;
            }
            trendData.push(sum / count);
        }


        new Chart(document.getElementById('lineChart'), {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Calories Consumed',
                        data: data.calories,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.3
                    },
                    {
                        label: 'Trend (3-Day Avg)', // Label for trend line
                        data: trendData,          // Use moving average data
                        borderColor: 'rgba(255, 99, 132, 1)', // Different color for trend
                        borderWidth: 2,
                        borderDash: [5, 5], // Make it a dashed line
                        fill: false,
                        pointRadius: 0,      // Hide points on trend line for clarity
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false, // Title is already in HTML
                        text: 'Daily Calorie Trend (Last 7 Days)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Calories (kcal)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    });