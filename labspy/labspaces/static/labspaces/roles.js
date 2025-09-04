document.addEventListener('DOMContentLoaded', function () {
  function getMainTableWrapper() {
    return document.querySelector('.table-responsive');
  }

  function showRowById(rowId) {
    var row = document.getElementById(rowId);
    if (!row) return;
    row.classList.remove('d-none');

    // Allow dropdowns to overflow fully when role table is expanded
    var wrapper = getMainTableWrapper();
    if (wrapper) {
      wrapper.dataset.prevOverflowY = wrapper.style.overflowY || '';
      wrapper.style.overflowY = 'visible';
      // Optionally lift max-height to ensure full visibility
      wrapper.dataset.prevMaxHeight = wrapper.style.maxHeight || '';
      wrapper.style.maxHeight = 'none';
    }
  }

  function hideRowById(rowId) {
    var row = document.getElementById(rowId);
    if (!row) return;
    row.classList.add('d-none');

    // Restore scrolling behavior on main wrapper when no role tables are open
    var anyOpen = document.querySelector('tr[id^="role-table-"]:not(.d-none)');
    if (!anyOpen) {
      var wrapper = getMainTableWrapper();
      if (wrapper) {
        wrapper.style.overflowY = wrapper.dataset.prevOverflowY || 'auto';
        wrapper.style.maxHeight = wrapper.dataset.prevMaxHeight || '610px';
      }
    }
  }

  // Attach handlers to "View" buttons
  document.querySelectorAll('.view-role-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var targetId = btn.getAttribute('data-target');
      if (!targetId) return;
      // Hide any other open role tables
      document.querySelectorAll('tr[id^="role-table-"]').forEach(function (row) {
        if (row.id !== targetId) {
          row.classList.add('d-none');
        }
      });
      showRowById(targetId);
      // Scroll into view for better UX
      var targetRow = document.getElementById(targetId);
      if (targetRow) {
        targetRow.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  });

  // Attach handlers to "Hide" buttons inside expanded rows
  document.querySelectorAll('.hide-role-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var targetId = btn.getAttribute('data-target');
      if (!targetId) return;
      hideRowById(targetId);
    });
  });
}); 