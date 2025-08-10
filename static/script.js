async function loadPerfumes() {
    const res = await fetch("/get");
    const perfumes = await res.json();

    const tablesContainer = document.getElementById("tablesContainer");
    tablesContainer.innerHTML = "";

    const categories = [
        "Premium Perfume",
        "Premium Medium Perfume",
        "Regular Perfume",
        "Car Perfume"
    ];

    categories.forEach(category => {
        const filtered = perfumes.filter(p => p.category === category);
        if (filtered.length > 0) {
            let totalQty = filtered.reduce((sum, p) => sum + p.quantity, 0);

            let tableHTML = `
                <div class="card shadow mb-4 p-3">
                    <h4 class="mb-3">${category}</h4>
                    <table class="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Price</th>
                                <th>Quantity</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${filtered.map(p => `
                                <tr>
                                    <td>${p.name}</td>
                                    <td>₹${p.price.toFixed(2)}</td>
                                    <td>${p.quantity}</td>
                                    <td>
                                        <button class="btn btn-warning btn-sm" onclick="editPerfume(${p.id}, '${p.name}', '${p.category}', ${p.price}, ${p.quantity})">Edit</button>
                                        <button class="btn btn-danger btn-sm" onclick="deletePerfume(${p.id})">Delete</button>
                                    </td>
                                </tr>
                            `).join("")}
                            <tr class="table-info">
                                <td colspan="2" class="fw-bold">Total Quantity</td>
                                <td colspan="2" class="fw-bold">${totalQty}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            `;
            tablesContainer.innerHTML += tableHTML;
        }
    });
}

async function addPerfume() {
    const name = document.getElementById("name").value;
    const category = document.getElementById("category").value;
    const price = document.getElementById("price").value;
    const quantity = document.getElementById("quantity").value;

    if (!name || !price || !quantity) {
        alert("Please fill all fields!");
        return;
    }

    await fetch("/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, category, price, quantity })
    });

    document.getElementById("name").value = "";
    document.getElementById("price").value = "";
    document.getElementById("quantity").value = "";

    loadPerfumes();
}

async function editPerfume(id, name, category, price, quantity) {
    const newName = prompt("Enter new name:", name);
    const newCategory = prompt("Enter new category:", category);
    const newPrice = parseFloat(prompt("Enter new price:", price));
    const newQuantity = parseInt(prompt("Enter new quantity:", quantity));

    if (!newName || !newCategory || isNaN(newPrice) || isNaN(newQuantity)) return;

    await fetch("/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, name: newName, category: newCategory, price: newPrice, quantity: newQuantity })
    });

    loadPerfumes();
}

async function deletePerfume(id) {
    if (!confirm("Are you sure you want to delete this perfume?")) return;

    await fetch("/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });

    loadPerfumes();
}

async function getTotal() {
    const res = await fetch("/total");
    const data = await res.json();
    document.getElementById("totalValue").textContent = `Total Stock Value: ₹${data.total.toFixed(2)}`;
}

loadPerfumes();
