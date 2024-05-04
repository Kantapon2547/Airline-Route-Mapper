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


if __name__ == "__main__":
    airline_dataset = AirlineRoutesDataset('routes.csv')
    airport_dataset = AirportDataset('airports.csv', 'runways.csv')

    airline_dataset.plot_airline_distribution()
    airport_dataset.classify_airport_size()

    plt.show()
