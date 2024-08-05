document.addEventListener('DOMContentLoaded', function () {
    const themeSelect = document.getElementById('theme');
    themeSelect.addEventListener('change', function () {
        document.body.className = themeSelect.value;
    });
});
