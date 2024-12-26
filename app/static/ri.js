document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const resetBtn = document.getElementById('reset-btn');
    const productNameInput = document.getElementById('product-name');
    const resultsContainer = document.getElementById('results-container');
    const resultProductName = document.getElementById('result-product-name');
    const resultTrending = document.getElementById('result-trending');
    const resultProfitMargin = document.getElementById('result-profit-margin');
    const resultWarehouseSpace = document.getElementById('result-warehouse-space');
    const vendorList = document.getElementById('vendor-list');

    // Simulated data
    const sampleData = {
        Headphones: {
            trending: true,
            profitMargin: "$25.00",
            warehouseSpace: "500 units",
            vendors: [
                { name: "Vendor A", rating: "4.5", location: "New York" },
                { name: "Vendor B", rating: "4.2", location: "San Francisco" },
            ],
        },
    };

    analyzeBtn.addEventListener('click', () => {
        const productName = productNameInput.value.trim();
        if (!productName) {
            alert("Please enter a product name.");
            return;
        }

        const data = sampleData[productName];
        if (!data) {
            alert("No data found for this product.");
            return;
        }

        resultProductName.textContent = productName;
        resultTrending.textContent = data.trending ? "Yes" : "No";
        resultProfitMargin.textContent = data.profitMargin;
        resultWarehouseSpace.textContent = data.warehouseSpace;

        vendorList.innerHTML = "";
        data.vendors.forEach((vendor) => {
            const row = `<tr>
                <td>${vendor.name}</td>
                <td>${vendor.rating}</td>
                <td>${vendor.location}</td>
            </tr>`;
            vendorList.innerHTML += row;
        });

        resultsContainer.classList.remove('hidden');
    });

    resetBtn.addEventListener('click', () => {
        productNameInput.value = "";
        resultsContainer.classList.add('hidden');
    });
});