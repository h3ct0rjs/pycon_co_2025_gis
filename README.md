# PyCon CO 2025 - Geospatial Analysis with Marimo

This repository contains a Marimo notebook demonstrating geospatial analysis techniques using DuckDB, GeoPandas, Folium, and other Python libraries.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- macOS, Linux, or Windows with WSL

### Running the Notebook

1. **Clone or download this repository**
2. **Navigate to the project directory**:
   ```bash
   cd pycon_co_2025_gis
   ```

3. **Run the launch script**:
   ```bash
   ./run_notebook.sh
   ```

That's it! The script will:
- Create a Python virtual environment (if `.venv` doesn't exist)
- Install all required dependencies
- Launch the Marimo notebook in your browser

## 📁 Project Structure

```
pycon_co_2025_gis/
├── pycon_co.py                                    # Main Marimo notebook
├── requirements.txt                               # Python dependencies
├── run_notebook.sh                                # Launch script
├── README.md                                      # This file
├── col_relative_wealth_index.csv                  # Colombia wealth data (optional)
└── col_ppp_2020_1km_Aggregated_UNadj.tif         # Population raster data (optional)
```

## 📊 Data Files

The notebook references two local data files:

1. **`col_relative_wealth_index.csv`** - Colombia Relative Wealth Index data
2. **`col_ppp_2020_1km_Aggregated_UNadj.tif`** - Population raster from WorldPop

### Data Sources

- **Wealth Index Data**: Available from [HDX - Colombia Relative Wealth Index](https://data.humdata.org/dataset/76f2a2ea-ba50-40f5-b79c-db95d668b843)
- **Population Raster**: Available from [WorldPop](https://hub.worldpop.org/geodata/summary?id=25805)

**Note**: If these files are missing, the notebook will still work partially as it also uses remote data sources for boundaries and some demonstrations.

## 🔧 Manual Setup (Alternative)

If you prefer to set up manually:

1. **Create virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the notebook**:
   ```bash
   marimo run pycon_co.py
   ```

## 📚 What's in the Notebook

This notebook demonstrates:

- **DuckDB Spatial**: Setting up spatial databases and extensions
- **Vector Data Operations**: Working with points, lines, and polygons
- **Geospatial Formats**: Reading GeoJSON, Shapefiles, and other formats
- **Spatial Queries**: Finding spatial relationships (within, intersects, etc.)
- **Data Visualization**: Creating interactive maps with Folium
- **Coordinate Projections**: Working with different coordinate systems
- **Zonal Statistics**: Combining raster and vector data analysis

## 🛠 Dependencies

The main libraries used are:

- **marimo**: Interactive notebook environment
- **duckdb**: In-memory analytical database with spatial extensions
- **geopandas**: Geospatial data manipulation
- **folium**: Interactive web maps
- **rasterstats**: Raster-vector analysis

## 🌐 Browser Support

The notebook runs in your web browser. Supported browsers:
- Chrome/Chromium
- Firefox
- Safari
- Edge

## 🐛 Troubleshooting

### Virtual Environment Issues
If you encounter permission issues, try:
```bash
python3 -m venv .venv --clear
```

### Missing System Dependencies
On some systems, you might need to install additional packages:

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install python3-dev gdal-bin libgdal-dev
```

**macOS** (with Homebrew):
```bash
brew install gdal
```

### Port Already in Use
If Marimo can't start because the port is in use, you can specify a different port:
```bash
marimo run pycon_co.py --port 8081
```

### Data Download Issues
If you need to download the data files manually:

1. **Wealth Index CSV**:
   - Visit: https://data.humdata.org/dataset/76f2a2ea-ba50-40f5-b79c-db95d668b843
   - Download the CSV file and rename it to `col_relative_wealth_index.csv`

2. **Population Raster**:
   - Visit: https://hub.worldpop.org/geodata/summary?id=25805
   - Download the TIF file for Colombia 2020

## 📄 License

This project is intended for educational purposes as part of PyCon Colombia 2025.

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the notebook or documentation.

---

**Happy Mapping! 🗺️**
