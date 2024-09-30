console.log("its Working!");


function returnSimpleContent() {
    fetch('/simple/get_content')
        .then(response => response.json())
        .then(data => {
            document.getElementById('simple-content-container').innerHTML = `
                <h2>${data.message}</h2>
                <p>Status: ${data.status}</p>
            `;
        })
        .catch(error => console.error('Error:', error));
}

function headSimpleContent() {
    fetch('/simple/head_content', { method: 'HEAD' })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            console.log('HEAD request successful');
        })
        .catch(error => console.error('Error:', error));
}
