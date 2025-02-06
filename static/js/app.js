document.addEventListener("DOMContentLoaded", function () {
    // Fetch the category data from Django template
    const categoryLabels = JSON.parse(document.getElementById("categoryLabels").textContent);
    const categoryCounts = JSON.parse(document.getElementById("categoryCounts").textContent);

    const ctx = document.getElementById("productsByCategoryChart").getContext("2d");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: categoryLabels,
            datasets: [{
                label: "Number of Products",
                data: categoryCounts,
                backgroundColor: [
                    "rgba(99, 102, 241, 0.8)",
                    "rgba(79, 70, 229, 0.8)",
                    "rgba(59, 130, 246, 0.8)",
                    "rgba(16, 185, 129, 0.8)",
                    "rgba(245, 158, 11, 0.8)",
                    "rgba(220, 38, 38, 0.8)"
                ],
                borderColor: "rgba(99, 102, 241, 1)",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: "rgba(0, 0, 0, 0.1)" }
                },
                x: {
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
});
