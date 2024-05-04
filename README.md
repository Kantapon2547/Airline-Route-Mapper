# Airline Route Mapper

Airline Route Mapper is a Python-based application designed to find the shortest path between two airports based on the distances between them, utilizing Dijkstra's algorithm for efficient route calculation.

## Description

Airline Route Mapper leverages Dijkstra's algorithm to calculate the shortest path between two airports using the provided airline routes dataset and airport information dataset. This project provides users with the ability to determine the shortest route considering the distances between airports. The interface offers a visualization of the route on a map, along with detailed information about the airports involved and the calculated distance.

## Main Features

- Utilizes Dijkstra's algorithm for finding the shortest path between airports.
- Input interface for users to specify origin and destination airports.
- Visualizes the shortest route on a map.
- Displays detailed information about airports involved in the route.
- Calculates and displays the total distance of the route.

## How to Use

1. **Install Dependencies**: Make sure you have Python installed on your system. You will need to install the following Python packages:
    ```bash
    pip install pandas folium
    ```

2. **Download the Repository**: Clone or download the repository to your local machine.

3. **Prepare Data**: Ensure you have the following CSV files in the project directory:
   - `airports.csv`: Contains information about airports, including their IDs, names, cities, countries, and coordinates.
   - `routes.csv`: Contains information about airline routes, including the origin and destination airport IDs.

4. **Run the Application**: Open a terminal or command prompt, navigate to the project directory, and run the following command:
    ```bash
    python mapper_gui.py
    ```

5. **Input Origin and Destination**: Enter the IDs of the origin and destination airports in the respective entry fields.

6. **Calculate Route**: Click on the "Calculate Route" button to find the shortest path between the specified airports.

7. **View Route Details**: The application will display detailed information about the origin and destination airports, including their IDs, cities, and countries.

8. **Display Route on Map**: Click on the "Show Map" button to visualize the calculated route on a map.

9. **Interact with Map**: You can interact with the map to zoom in/out and pan around to explore the route.

10. **Exit the Application**: Close the application window when done.

