import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class AirlineRoutesDataset:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def plot_airline_distribution(self):
        plt.figure(figsize=(12, 6))
        ax = sns.countplot(x='Airline', data=self.data, order=self.data['Airline'].value_counts().index[:20])
        ax.set_title('Distribution of Top 20 Airlines')
        ax.set_xlabel('Airline')
        ax.set_ylabel('Frequency')
        ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels
        plt.tight_layout()


class AirportDataset:
    def __init__(self, airports_file, runways_file):
        self.airports_data = pd.read_csv(airports_file)
        self.runways_data = pd.read_csv(runways_file)

    def classify_airport_size(self):
        # Merge datasets based on airport ID
        merged_data = pd.merge(self.airports_data, self.runways_data, left_on='id', right_on='airport_ref', how='inner')

        # Classify airport size based on runway area (length * width * elevation)
        def classify(row):
            area = row['length_ft'] * row['width_ft'] * row['elevation_ft']
            if area > 1000000000:  # Example threshold for Large
                return 'Large'
            elif area > 500000000:  # Example threshold for Medium
                return 'Medium'
            else:
                return 'Small'

        merged_data['type'] = merged_data.apply(classify, axis=1)

        # Count occurrences of each type
        size_counts = merged_data['type'].value_counts()

        # Extract data for plotting
        types = size_counts.index
        counts = size_counts.values
        sizes = {'Small': 100, 'Medium': 200, 'Large': 300}  # Define bubble sizes

        # Plot the bubble chart
        plt.figure(figsize=(10, 6))
        for i, airport_type in enumerate(types):
            plt.scatter(i, counts[i], s=sizes[airport_type], label=airport_type, alpha=0.7)

        plt.xticks(range(len(types)), types)
        plt.xlabel('Airport Size')
        plt.ylabel('Count')
        plt.title('Airport Size Classification Based on Area')
        plt.legend(title='Type')
        plt.grid(True)
        plt.tight_layout()
        plt.show()


class AirportDistributionPlotter:
    def __init__(self, airports_file):
        self.airports_df = pd.read_csv(airports_file)

    def plot_distribution_by_country(self):
        grouped = self.airports_df.groupby("iso_country").agg({
            "latitude_deg": "mean",
            "longitude_deg": "mean",
            "elevation_ft": "mean"
        })

        top_20_countries = grouped.index[:20]  # Select only the top 20 countries
        grouped_top_20 = grouped.loc[top_20_countries]

        fig, ax = plt.subplots(figsize=(10, 6))
        grouped_top_20.plot(kind="bar", ax=ax)
        plt.title("Top 20 Airport Distribution by Country with Runway Characteristics and Elevation")
        plt.xlabel("Country")
        plt.ylabel("Average Values")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


class RouteGraphPlotter:
    def __init__(self, route_data):
        self.route_data = pd.read_csv('data/routes.csv')

    def plot_source_airport_frequency(self):
        plt.figure(figsize=(14, 8))  # Adjust the figure size as needed
        source_counts = self.route_data['Source airport ID'].value_counts().head(20)  # Count the frequency of each source airport ID
        source_counts.plot(kind='bar')  # Plot as a bar graph
        plt.title('Frequency of Routes Departing from Source Airports (Top 20)')
        plt.xlabel('Source Airport ID')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.show()

    def plot_destination_airport_frequency(self):
        plt.figure(figsize=(10, 6))
        sns.countplot(x='Destination Airport', data=self.route_data.head(20))  # Select only the first 20 rows
        plt.title('Frequency of Routes Arriving at Destination Airports (Top 20)')
        plt.xlabel('Destination Airport')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_route_graph(self):
        plt.figure(figsize=(14, 8))
        sns.countplot(x='Source airport ID', data=self.route_data.head(20))  # Select only the first 20 rows
        plt.title('Distribution of Routes Among Different Airlines (Top 20)')
        plt.xlabel('Source Airport ID')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
