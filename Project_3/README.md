This project was purposely made more complex in order to learn Arduino API communications with another device (in this case the Raspberry PI 400). The Raspberry Pi also sends its data to the Arduino Cloud.

![image](https://github.com/user-attachments/assets/8fdd72d3-aa2f-4843-bd67-06246a0840d7)

In the above image you can see how the devices in projects 1, 2, and 3 fit together. 

<h3>Raspberry Pi:</h3>

The Python code for this project uses Flask to provide a server for the Arduino to query against. It first gets a new authentication code from Ardunio Cloud, and then it queries for the last temperature and humidity values provided by Project 1. While it has these values, it saves them to a CSV file on the SD drive. Finally, it returns the values and a timestamp as JSON.

<h3>Arduino R4 WIFI:</h3>

The C++ code for this project makes a GET call to the Raspberry Pi (using its IP address), parses the JSON it returns, and displays the results on a connected LCD panel.

The project is displayed as-is on a wall in kind of a "retro" manner.
<ul>

![image](https://github.com/user-attachments/assets/7d942504-c8f0-4636-9e05-6bdba7d1163b)
 
</ul>
