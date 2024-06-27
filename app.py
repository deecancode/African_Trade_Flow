from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go
import pandas as pd
import json
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Load the data
df = pd.read_csv('trade.csv')

df= df[df["Partner"] != "World"]

# Load country coordinates from JSON file
with open('country_coordinates.json', 'r') as f:
    country_coords = json.load(f)

# List of African country codes (ISO alpha-3)
african_countries = [
    'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon',
    'Central African Rep.', 'Chad', 'Comoros', 'Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea',
    'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau',
    "Côte d'Ivoire", 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali',
    'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda',
    'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa',
    'South Sudan', 'Sudan', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
]
# List of partner countries
partner_countries = ['Afghanistan', 'Albania', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Bahamas', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bolivia (Plurinational State of)', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Rep.', 'Chad', 'Chile', 'China', 'China, Hong Kong SAR', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', "Côte d'Ivoire", "Dem. People's Rep. of Korea", 'Dem. Rep. of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Rep.', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Italy', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan', "Lao People's Dem. Rep.", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Mongolia', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Other Asia, nes', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Rep. of Korea', 'Rep. of Moldova', 'Romania', 'Russian Federation', 'Saint Kitts and Nevis', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovenia', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'State of Palestine', 'Sudan', 'Sweden', 'Switzerland', 'Syria', 'Tajikistan', 'Thailand', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkmenistan', 'Türkiye', 'USA', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United Rep. of Tanzania', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Viet Nam', 'World', 'Yemen', 'Zambia', 'Zimbabwe', 'Algeria', 'American Samoa', 'Anguilla', 'Areas, nes', 'Aruba', 'Azerbaijan', 'Barbados', 'Bhutan', 'Br. Indian Ocean Terr.', 'Br. Virgin Isds', 'Cayman Isds', 'China, Macao SAR', 'Cocos Isds', 'Curaçao', 'Faeroe Isds', 'French Polynesia', 'Gibraltar', 'Greenland', 'Holy See (Vatican City State)', 'Israel', 'Jamaica', 'Marshall Isds', 'Mayotte (Overseas France)', 'Montserrat', 'N. Mariana Isds', 'Nauru', 'North America and Central America, nes', 'Papua New Guinea', 'Pitcairn', 'Rwanda', 'Saint Helena', 'Slovakia', 'South Georgia and the South Sandwich Islands', 'Suriname', 'Timor-Leste', 'Tokelau', 'Tonga', 'United States Minor Outlying Islands', 'Wallis and Futuna Isds', 'Cook Isds', 'Falkland Isds (Malvinas)', 'Fr. South Antarctic Terr.', 'Heard Island and McDonald Islands', 'Kiribati', 'Norfolk Isds', 'Saint Lucia', 'Turks and Caicos Isds', 'Tuvalu', 'Antarctica', 'Burundi', 'Guam', 'Christmas Isds', 'Bouvet Island', 'Bunkers', 'Solomon Isds', 'Other Europe, nes', 'Vanuatu', 'LAIA, nes', 'Montenegro', 'Saint Pierre and Miquelon', 'Western Sahara', 'Free Zones', 'Niue', 'Palau', 'FS Micronesia', 'Special Categories', 'South Sudan', 'Sint Maarten', 'Oceania, nes', 'Saint Barthélemy']

# Create a dictionary to map country names to their coordinates
# Create a dictionary to map country names to their coordinates
country_to_coords = {entry['country']: (entry['latitude'], entry['longitude']) for entry in country_coords['ref_country_codes']}

def format_value(value):
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.1f}T"
    elif value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    else:
        return f"${value:.1f}"

@cache.memoize(timeout=86400)  # Cache for 24 hours
def create_trade_flow_graph(df):
    traces = []
    total_trade_value = 0
    intra_african_trade_value = 0

    max_trade_value = df['Trade Value (US$)'].max() if not df.empty else 1  # Avoid division by zero

    for _, row in df.iterrows():
        reporter_coords = country_to_coords.get(row['Reporter'])
        partner_coords = country_to_coords.get(row['Partner'])

        if reporter_coords and partner_coords:
            trade_value = float(row['Trade Value (US$)'])
            total_trade_value += trade_value

            # Calculate opacity based on trade value
            opacity = min((trade_value / max_trade_value) + 0.02, 0.9)

            if row['Reporter'] in african_countries and row['Partner'] in african_countries:
                line_color = 'green'
                line_width = 1
                intra_african_trade_value += trade_value
            else:
                line_color = 'orange'
                line_width = 1

            # Add line trace
            trace_line = go.Scattergeo(
                lon=[reporter_coords[1], partner_coords[1]],
                lat=[reporter_coords[0], partner_coords[0]],
                mode='lines',
                line=dict(width=line_width, color=line_color),
                text=f"{row['Reporter']} to {row['Partner']}",
                hoverinfo='text',
                opacity=opacity,
            )
            traces.append(trace_line)

            # Add dot traces for reporter and partner
            trace_reporter = go.Scattergeo(
                lon=[reporter_coords[1]],
                lat=[reporter_coords[0]],
                mode='markers',
                marker=dict(size=5, color=line_color),
                text=row['Reporter'],
                hoverinfo='text',
            )
            trace_partner = go.Scattergeo(
                lon=[partner_coords[1]],
                lat=[partner_coords[0]],
                mode='markers',
                marker=dict(size=3, color=line_color),
                text=row['Partner'],
                hoverinfo='text',
            )
            traces.extend([trace_reporter, trace_partner])

    intra_african_trade_percentage = (intra_african_trade_value / total_trade_value) * 100 if total_trade_value > 0 else 0
    extra_african_trade_value = total_trade_value - intra_african_trade_value
    extra_african_trade_percentage = 100 - intra_african_trade_percentage if total_trade_value > 0 else 0

    layout = go.Layout(
        title_text='Trade Flows',
        showlegend=False,
        geo=dict(
            scope='world',
            projection_type='equirectangular',
            showland=True,
            showcountries=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    fig = go.Figure(data=traces, layout=layout)
    graph_html = fig.to_html(full_html=False)

    return graph_html, format_value(intra_african_trade_value), int(intra_african_trade_percentage), format_value(extra_african_trade_value), int(extra_african_trade_percentage)

@app.route('/')
def index():
    # Filter the dataframe for the year 2023
    df_2023 = df[df['Period'] == 2023]
    graph_html, intra_african_trade_value, intra_african_trade_percentage, extra_african_trade_value, extra_african_trade_percentage = create_trade_flow_graph(df_2023)
    total_trade_value = df_2023['Trade Value (US$)'].sum()
    formatted_total_trade = format_value(total_trade_value)
    earliest_year = df['Period'].min()
    latest_year = df['Period'].max()
    reporting_countries_list = sorted(african_countries)
    partner_countries_list = sorted(partner_countries)
    return render_template('index.html', graph_html=graph_html, intra_african_trade_value=intra_african_trade_value,
                           intra_african_trade_percentage=intra_african_trade_percentage, extra_african_trade_value=extra_african_trade_value,
                           extra_african_trade_percentage=extra_african_trade_percentage, earliest_year=earliest_year,
                           latest_year=latest_year, reporting_countries=reporting_countries_list, partner_countries=partner_countries_list,
                           total_trade_value=formatted_total_trade, selected_year=2023)

@app.route('/filter', methods=['POST'])
@cache.cached(timeout=86400)  # Cache for 24 hours
def filter_data():
    # Get filter parameters from the form
    selected_year = int(request.form['selected_year'])
    reporting_countries = request.form.getlist('reporting_countries')
    partner_countries = request.form.getlist('partner_countries')

    # Start with the full dataset
    filtered_df = df[df['Period'] == selected_year]

    # Filter by reporting countries if specific countries are selected
    if reporting_countries and 'All' not in reporting_countries:
        filtered_df = filtered_df[filtered_df['Reporter'].isin(reporting_countries)]
        # Check for missing countries
        missing_countries = set(reporting_countries) - set(filtered_df['Reporter'].unique())
    else:
        missing_countries = set()

    # Filter by partner countries if specific countries are selected
    if partner_countries and 'All' not in partner_countries:
        filtered_df = filtered_df[filtered_df['Partner'].isin(partner_countries)]

    # Create the trade flow graph with the filtered data
    graph_html, intra_african_trade_value, intra_african_trade_percentage, extra_african_trade_value, extra_african_trade_percentage = create_trade_flow_graph(filtered_df)

    # Calculate total trade value
    total_trade_value = filtered_df['Trade Value (US$)'].sum()
    formatted_total_trade = format_value(total_trade_value)

    # Prepare the response data
    response_data = {
        'graph_html': graph_html,
        'intra_african_trade_value': intra_african_trade_value,
        'intra_african_trade_percentage': intra_african_trade_percentage,
        'extra_african_trade_value': extra_african_trade_value,
        'extra_african_trade_percentage': extra_african_trade_percentage,
        'missing_countries': list(missing_countries),
        'total_trade_value': formatted_total_trade
    }

    # Return the response as JSON
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5042)
