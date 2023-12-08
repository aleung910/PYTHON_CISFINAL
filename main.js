document.addEventListener('DOMContentLoaded', function () {
    fetch('stations.json')
        .then(response => response.json())
        .then(stationData => {

            const startSelect = document.querySelector('select[name="StartStation"]');
            const endSelect = document.querySelector('select[name="EndStation"]');

            // Filter stations for 1-6 train lines
            const lines16 = ['1', '2', '3', '4', '5', '6'];
            const filteredStations = stationData.filter(station => {
                const daytimeRoutes = Array.isArray(station['Daytime Routes'])
                    ? station['Daytime Routes']
                    : [station['Daytime Routes'].toString()];

                return lines16.some(line => daytimeRoutes.includes(line));
            });

            // Populate the select elements with options
            filteredStations.forEach(station => {
                const option = document.createElement('option');
                option.value = station['Stop Name'];
                option.textContent = station['Stop Name'];
                startSelect.appendChild(option.cloneNode(true));
                endSelect.appendChild(option);
            });

            // Add event listener to the button
            const button = document.querySelector('button[name="button"]');
            button.addEventListener('click', function () {
                // Retrieve the selected stations
                const startStation = startSelect.value;
                const endStation = endSelect.value;

                // Do something with the selected stations, e.g., fetch additional information
                console.log('Selected Start Station:', startStation);
                console.log('Selected End Station:', endStation);
            });
        })
        .catch(error => console.error('Error fetching stations:', error));

   // Fetch stopsGraph.json
   fetch('stopsGraph.json')
   .then(response => response.json())
   .then(stopGraph => {
       // Assuming stopGraph is an object or an array
       const jsonString = JSON.stringify(stopGraph, null, 2);

       // Display JSON content in a pre element (you can customize this based on your HTML structure)
       const jsonContainer = document.getElementById('json-container');
       jsonContainer.textContent = jsonString;
   })
   .catch(error => console.error('Error fetching stopsGraph.json:', error));


});

// main.js
// main.js
// document.addEventListener("DOMContentLoaded", function () {
//     const jsonContainer = document.getElementById('json-container');
//     const createGraphButton = document.querySelector('button[name="button"]');

//     createGraphButton.addEventListener('click', function () {
//         fetch('http://localhost:8000/get_data')
//             .then(response => response.json())
//             .then(data => {
//                 // Update only the specific element with the JSON data
//                 jsonContainer.innerText = JSON.stringify(data, null, 2);
                
//             })
//             .catch(error => console.error('Error fetching data:', error));
//     });
// });
// main.js
