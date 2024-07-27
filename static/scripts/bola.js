function Sendding(parameterToSend){
    // Perform a POST request to the specified URL ('http://localhost:8888/idor/BOLA')
    fetch('http://localhost:8888/idor/bola', {
        // Specify that the request method is POST
        method: 'POST', headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify({ param: parameterToSend })
    }).then(response => response.json())
        .then(data => {
            resulteResponse = "Clients of user-1 \n" + data.message;
            document.getElementById('responseContainer').innerText = resulteResponse;
        })
        // Catch any errors that occur during the fetch operation
        .catch(error => console.error('Error:', error));
}



// Wait for the DOM to fully load before executing the enclosed code
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('viewqrDB').addEventListener('click', function () {
        Sendding(["bola1"])
    });
});