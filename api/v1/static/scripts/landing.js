document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.start-button').addEventListener('click', function() {
        console.log('Button clicked!'); // For debugging
        window.location.href = 'http://127.0.0.1:2000/gitlougui/homepage';
    });
});
