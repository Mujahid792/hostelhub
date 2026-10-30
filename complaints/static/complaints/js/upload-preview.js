document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('input[type="file"]');
    const container = document.getElementById('preview-container');
    const img = document.getElementById('image-preview');
    if (!input || !container || !img) return;
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (ev) => {
                img.src = ev.target.result;
                container.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            container.style.display = 'none';
        }
    });
});