import tkinter as tk
from tkinter import ttk, scrolledtext
import csv
import webbrowser
import folium
import data_graph


class AirlineRouteMapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Route Mapper")
        self.root.configure(background='light blue')  # Set background color
        self.create_widgets()

    def create_widgets(self):
        # Origin Airport ID
        ttk.Label(self.root, text="Origin Airport ID:", background='light blue').grid(row=0, column=0, padx=10, pady=5)
        self.origin_entry = ttk.Entry(self.root)
        self.origin_entry.grid(row=0, column=1, padx=10, pady=5)

        # Destination Airport ID
        ttk.Label(self.root, text="Destination Airport ID:", background='light blue').grid(row=1, column=0, padx=10, pady=5)
        self.destination_entry = ttk.Entry(self.root)
        self.destination_entry.grid(row=1, column=1, padx=10, pady=5)

        # Calculate Route Button
        self.calculate_button = ttk.Button(self.root, text="Calculate Route", command=self.calculate_route)
        self.calculate_button.grid(row=2, columnspan=2, padx=10, pady=5)

        # Text widget to display airport details
        self.airport_details_text = scrolledtext.ScrolledText(self.root, width=60, height=10, wrap=tk.WORD)
        self.airport_details_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Show Map Button
        self.show_map_button = ttk.Button(self.root, text="Show Map", command=self.show_map)
        self.show_map_button.grid(row=4, column=0, sticky=tk.E, padx=10, pady=5)

        # Show Graph Button
        self.show_graph_button = ttk.Button(self.root, text="Show Graph", command=self.show_graph)
        self.show_graph_button.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)

        # Airport Table with Scrollbar
        self.airport_tree = ttk.Treeview(self.root, columns=("Airport Name", "City", "Country"))
        self.airport_tree.heading("#0", text="ID")
        self.airport_tree.heading("Airport Name", text="Airport Name")
        self.airport_tree.heading("City", text="City")
        self.airport_tree.heading("Country", text="Country")

        # Add scrollbars
        tree_scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.airport_tree.yview)
        tree_scroll.grid(row=5, column=2, sticky="ns")
        self.airport_tree.configure(yscrollcommand=tree_scroll.set)

        self.airport_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.insert_data_from_csv("airports.csv", encoding='utf-8')

    def insert_data_from_csv(self, filename, encoding='utf-8'):
        with open(filename, "r", encoding=encoding) as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                airport_id, _, _, name, _, _, _, _, iso_country, _, city, *_ = row
                display_data = f"{airport_id}, {name}", city, iso_country
                self.airport_tree.insert("", tk.END, text=airport_id, values=display_data)

    def calculate_route(self):
        origin_id = self.origin_entry.get()
        destination_id = self.destination_entry.get()

        origin_data = self.get_airport_details(origin_id)
        destination_data = self.get_airport_details(destination_id)

        if origin_data is None:
            print(f"Origin airport with ID {origin_id} not found.")
            return
        if destination_data is None:
            print(f"Destination airport with ID {destination_id} not found.")
            return

        self.display_airport_details(origin_data, destination_data)

    def get_airport_details(self, airport_id):
        for item in self.airport_tree.get_children():
            if self.airport_tree.item(item, "text") == airport_id:
                return self.airport_tree.item(item, "values")
        return None

    def display_airport_details(self, origin_data, destination_data):
        self.airport_details_text.delete(1.0, tk.END)
        self.airport_details_text.insert(tk.END, "Origin Airport Details:\n")
        self.airport_details_text.insert(tk.END, f"Airport ID: {origin_data[0]}\n")
        self.airport_details_text.insert(tk.END, f"City: {origin_data[1]}\n")
        self.airport_details_text.insert(tk.END, f"Country: {origin_data[2]}\n\n")

        self.airport_details_text.insert(tk.END, "Destination Airport Details:\n")
        self.airport_details_text.insert(tk.END, f"Airport ID: {destination_data[0]}\n")
        self.airport_details_text.insert(tk.END, f"City: {destination_data[1]}\n")
        self.airport_details_text.insert(tk.END, f"Country: {destination_data[2]}\n")

    def display_route_on_map(self, origin_data, destination_data):
        origin_city = origin_data[1]
        m = folium.Map(location=self.get_coordinates(origin_city), zoom_start=8)

        origin_name = origin_data[0].split(", ")[1]
        destination_name = destination_data[0].split(", ")[1]
        folium.Marker(location=self.get_coordinates(origin_city), popup=f"Origin: {origin_name}").add_to(m)
        destination_city = destination_data[1]
        folium.Marker(location=self.get_coordinates(destination_city), popup=f"Destination: {destination_name}").add_to(m)

        m.save("airport_map.html")

    def get_coordinates(self, city_name):
        for item in self.airport_tree.get_children():
            airport_id = self.airport_tree.item(item, "text")
            airport_data = self.airport_tree.item(item, "values")
            if airport_data[1] == city_name:
                latitude = float(airport_data[4])
                longitude = float(airport_data[5])
                return latitude, longitude
        return 0, 0

    def show_map(self):
        webbrowser.open_new_tab("airport_map.html")

    def show_graph(self):
        data_graph.AirportDataset('airports.csv', 'runways.csv').display_graph()


# Create the Tkinter application
root = tk.Tk()
app = AirlineRouteMapperApp(root)
root.mainloop()
