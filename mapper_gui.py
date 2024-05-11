import tkinter as tk
from tkinter import ttk, scrolledtext
import csv
import webbrowser
import folium
from data_graph import AirlineRoutesDataset, AirportDataset, AirportDistributionPlotter, RouteGraphPlotter


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

        # Clear Button
        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_data)
        self.clear_button.grid(row=2, column=1, padx=10, pady=5)

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

        self.insert_data_from_csv("data/airports.csv", encoding='utf-8')

        # Graph selection
        self.graph_selection = tk.StringVar(value="Airport Distribution")
        ttk.Label(self.root, text="Graph Selection:", background='light blue').grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        self.graph_options = ttk.Combobox(self.root, textvariable=self.graph_selection, state='readonly')
        self.graph_options['values'] = ["Airport Distribution", "Airport Size Classification", "Airline Distribution", "Route Graph"]
        self.graph_options.grid(row=6, column=1, padx=10, pady=5)
        self.graph_options.bind("<<ComboboxSelected>>", self.update_graph)

    def insert_data_from_csv(self, filename, encoding='utf-8'):
        with open(filename, "r", encoding=encoding) as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                airport_id, _, _, name, latitude_deg, longitude_deg, _, _, iso_country, _, city, *_ = row
                display_data = f"{airport_id}, {name}", city, iso_country, latitude_deg, longitude_deg
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
        self.display_route_on_map(origin_data, destination_data)  # Call this method to display the route on the map

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
        m = folium.Map(location=[0, 0], zoom_start=2)  # Initial map with a default location

        # Add origin pin
        origin_latitude, origin_longitude = float(origin_data[3]), float(origin_data[4])
        origin_name = origin_data[0].split(", ")[1]
        origin_popup = f"<a href='https://www.google.com/maps/search/?api=1&query={origin_latitude},{origin_longitude}'>Origin: {origin_name}</a>"
        folium.Marker(location=[origin_latitude, origin_longitude], popup=origin_popup, parse_html=True).add_to(m)

        # Add destination pin
        destination_latitude, destination_longitude = float(destination_data[3]), float(destination_data[4])
        destination_name = destination_data[0].split(", ")[1]
        destination_popup = f"<a href='https://www.google.com/maps/search/?api=1&query={destination_latitude},{destination_longitude}'>Destination: {destination_name}</a>"
        folium.Marker(location=[destination_latitude, destination_longitude], popup=destination_popup,
                      parse_html=True).add_to(m)

        m.save("airport_map.html")

    def get_coordinates(self, city_name):
        for item in self.airport_tree.get_children():
            airport_id = self.airport_tree.item(item, "text")
            airport_data = self.airport_tree.item(item, "values")
            if airport_data[1] == city_name:
                latitude = float(airport_data[3])
                longitude = float(airport_data[4])
                return latitude, longitude
        return 0, 0

    def show_map(self):
        webbrowser.open_new_tab("airport_map.html")

    def update_graph(self, event=None):
        graph_type = self.graph_selection.get()
        if graph_type == "Airport Distribution":
            AirportDistributionPlotter("data/airports.csv").plot_distribution_by_country()
        elif graph_type == "Airport Size Classification":
            AirportDataset('data/airports.csv', 'data/runways.csv').classify_airport_size()
        elif graph_type == "Airline Distribution":
            AirlineRoutesDataset('data/routes.csv').plot_airline_distribution()
        elif graph_type == "Route Graph":
            RouteGraphPlotter('routes.csv').plot_route_graph()

    def show_graph(self):
        self.update_graph()

    def clear_data(self):
        self.origin_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.airport_details_text.delete(1.0, tk.END)


root = tk.Tk()
app = AirlineRouteMapperApp(root)
root.mainloop()
