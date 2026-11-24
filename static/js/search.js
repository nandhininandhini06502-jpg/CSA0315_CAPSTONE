// ==========================================================
// Evidence Search and Algorithm Visualizer JS
// ==========================================================

document.addEventListener('DOMContentLoaded', function () {
    const algoSelect = document.getElementById('id_algorithm');
    const algoBadge = document.getElementById('algoTypeBadge');

    const algoDescriptions = {
        'c_binary': 'C Binary Search: Sorted logarithmic lookup O(log n)',
        'c_hash': 'C Hash Table: Direct bucket lookup with O(1) average access',
        'c_bst': 'C Binary Search Tree: Hierarchical branching and search',
        'c_linear': 'C Linear Search: Sequential string matching O(n)'
    };

    if (algoSelect && algoBadge) {
        algoSelect.addEventListener('change', function () {
            algoBadge.textContent = algoDescriptions[this.value] || this.value;
        });
    }

    // Instant table live filtering
    const tableSearch = document.getElementById('tableQuickSearch');
    const tableBody = document.getElementById('evidenceTableBody');
    if (tableSearch && tableBody) {
        tableSearch.addEventListener('input', function () {
            const query = this.value.toLowerCase();
            const rows = tableBody.querySelectorAll('tr');
            rows.forEach(function (row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }
});
