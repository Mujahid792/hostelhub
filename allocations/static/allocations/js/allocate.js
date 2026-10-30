// Real-time capacity warning on allocate page
document.addEventListener('DOMContentLoaded', () => {
    const roomSelect = document.querySelector('select[name="room"]');
    if (!roomSelect) return;
    roomSelect.addEventListener('change', () => {
        const opt = roomSelect.selectedOptions[0];
        if (opt && opt.textContent.includes('0 space')) {
            alert('Selected room has no available space!');
        }
    });
});