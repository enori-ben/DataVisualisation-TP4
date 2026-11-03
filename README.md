# TP04: Advanced Visualization, Comparative Analysis, and Interactivity

**Module:** Data Visualization  
**Academic Year:** 2026/2027  
**Level:** Second-Year Master's – Artificial Intelligence and Data Science

## 📚 Teacher's TP4 Reference

[View the Teacher's Original TP4 Instructions](https://github.com/ahmed3991/DataVisualisation-TP2025/blob/main/TP4/TP4.md)

---

## 1. Project Overview

This project analyzes global development indicators using Python. It explores the relationships between GDP per capita, life expectancy, internet usage, and population through statistical visualization, correlation analysis, interactive charts, geographical mapping, and network analysis.

The dataset covers 217 economies from 2000 to 2023.

## 2. Dataset

The project uses World Bank development indicators.

| Variable | Description |
|---|---|
| Country | Country or economy name |
| Year | Observation year |
| GDP_Per_Capita | GDP per capita in current US dollars |
| Life_Expectancy | Life expectancy at birth |
| Internet_Users_Pct | Individuals using the Internet (%) |
| Population | Total population |
| Region | Geographic region |
| Income_Group | World Bank income classification |

The original dataset contains 5,208 observations.

### Data preprocessing

- Standardized column values and data types.
- Removed duplicate country-year records.
- Kept observations from 2000 to 2023.
- Preserved missing indicator values instead of artificially imputing them.

## 3. Visualizations and Analysis

### 3.1 Comparative visualizations

- **Scatter Plot:** GDP per capita versus life expectancy, with a logarithmic GDP axis.
- **Bubble Chart:** Adds population size to the comparison.
- **2D Density Plot:** Shows the concentration of observations across the two indicators.

These visualizations help compare development indicators and examine differences between economies.

### 3.2 Correlation analysis

Pearson correlation is used to examine linear relationships between the four numerical indicators.

The strongest positive correlation is between Life Expectancy and Internet Users (r = 0.711).

Other notable correlations:

- GDP per capita and Internet Users: 0.604.
- GDP per capita and Life Expectancy: 0.577.
- Population and Life Expectancy: 0.009.

These correlations describe associations and do not establish causation.

### 3.3 Interactive GDP time series

A Plotly chart compares GDP per capita over time for Germany and Algeria. It supports hovering, zooming, and panning.

### 3.4 Geographical visualization

A Folium choropleth map displays life expectancy for the latest available year, with country information in its tooltip and popup.

**Geographical coverage limitation:** The supplied GeoJSON contains 179 geographic features, and 171 of the dataset's 217 country codes match the map boundaries. Some economies therefore cannot be displayed.

### 3.5 Network analysis

NetworkX represents a regional hierarchy:

**World → Regions → Countries**

The generated graph contains 225 nodes and 224 edges.

The hierarchical structure illustrates the organization of countries by geographic region. Additional external data would be required to represent economic relationships between countries.

## 4. Project Structure

```text
DataVisualisation-TP4/
├── data/
│   ├── world_bank_2000_2023.csv
│   ├── cleaned_world_bank.csv
│   └── countries.geo.json
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── visualizations.py
│   ├── interactive_visualizations.py
│   ├── network_analysis.py
│   └── main.py
├── results/
│   ├── 01_scatter.png
│   ├── 02_bubble.png
│   ├── 03_density.png
│   ├── 04_correlation_heatmap.png
│   ├── 05_interactive_gdp.html
│   ├── 06_life_expectancy_map.html
│   ├── 07_regional_hierarchy.png
│   └── correlation.csv
├── TP4.ipynb
├── requirements.txt
└── README.md
```

## 5. Installation and Execution

### Requirements

- Python 3.10 or later
- pip

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the complete project

From the project root directory:

```bash
python -m src.main
```

This command preprocesses the dataset and generates the visualizations in the `results/` directory.

### Run the Jupyter Notebook

```bash
jupyter notebook TP4.ipynb
```

Open the notebook and execute its cells in order.

## 6. Results

The project generates the following outputs:

1. GDP per capita vs Life expectancy scatter plot.
2. Population bubble chart.
3. Two-dimensional density plot.
4. Pearson correlation heatmap.
5. Interactive GDP time series.
6. Life expectancy geographical choropleth.
7. Regional hierarchy network graph.

The generated visualizations are available in the `results/` directory.

## 7. Limitations

- GDP per capita is measured in current US dollars and is not adjusted for inflation.
- Missing values are preserved and excluded from analyses that require complete observations.
- The geographical map depends on the coverage of the supplied GeoJSON file.
- Pearson correlation measures linear association, not causality.
- Combining observations across years may conceal country-specific and temporal differences.

## 8. Conclusion

This project demonstrates how statistical, interactive, geographical, and network visualizations can support the analysis of global development indicators. Combining these methods provides complementary perspectives on the relationships between economic conditions, life expectancy, internet usage, and population.
