# African Trade Flow Visualization

This project provides an interactive web application to visualize trade flows between African countries and their global partners. It uses Flask, Plotly, and Pandas to process and display trade data.

## Features

- Interactive world map showing trade flows
- Filters for year, reporting countries, and partner countries
- Display of intra-African and extra-African trade statistics
- Responsive design for various screen sizes

## Installation

1. Clone the repository
git clone https://github.com/deecancode/African_Trade_Flow.git
cd African_Trade_Flow

## Usage

1. Ensure you have the required data files:
   - `trade.csv`: Contains the trade data
   - `country_coordinates.json`: Contains geographical coordinates for countries

2. Run the Flask application:


3. Open a web browser and navigate to `http://localhost:5042`

## Data Format

The `trade.csv` file contains the following columns:
- Period: Year of the trade data
- Reporter: The reporting country
- Partner: The partner country
- Trade Value (US$): The value of trade in US dollars

The `country_coordinates.json` file contains a list of countries with their latitude and longitude coordinates.

## Customization

You can customize the list of African countries and partner countries in the `app.py` file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Nabelou Ouologuem
