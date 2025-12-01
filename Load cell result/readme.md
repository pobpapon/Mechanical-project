# 📊 Recoil Force Measurement System

<p align="center">
  <img src="https://img.shields.io/badge/MATLAB-R2020+-orange.svg" alt="MATLAB">
  <img src="https://img.shields.io/badge/Excel-Analysis-green.svg" alt="Excel">
  <img src="https://img.shields.io/badge/Load%20Cell-Data-blue.svg" alt="Load Cell">
  <img src="https://img.shields.io/badge/Data%20Analysis-Force%20Measurement-red.svg" alt="Analysis">
</p>

<p align="center">
  <strong>A comprehensive system for measuring and analyzing recoil forces using load cell sensors</strong>
</p>

---

## 📋 Overview

This project provides a complete workflow for measuring, collecting, and analyzing recoil forces using load cell sensors. The system captures raw force data, processes it through Excel for statistical analysis, and uses MATLAB for advanced graphical analysis and force pattern recognition.

## 🔄 Data Flow
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Load Cell  │─────►│  .TXT File  │─────►│    Excel    │
│   Sensor    │ Raw  │  Raw Data   │ Copy │  Analysis   │
│             │ Data │ (Unmodified)│      │             │
└─────────────┘      └─────────────┘      └──────┬──────┘
                                                  │
                                                  │ Export
                                                  ▼
                                           ┌─────────────┐
                                           │   MATLAB    │
                                           │  Analysis   │
                                           │ (.m files)  │
                                           └─────────────┘
```

## ✨ Features

- 📈 **Real-time Data Acquisition** - Direct load cell sensor readings
- 📄 **Raw Data Preservation** - Unmodified .TXT files for data integrity
- 📊 **Excel Analysis** - Statistical analysis and peak force detection
- 🔬 **MATLAB Processing** - Advanced graphical analysis and visualization
- 🎯 **Peak Force Detection** - Automatic identification of maximum forces
- 📉 **Force-Time Graphs** - Detailed visualization of recoil patterns

---

## 📁 Project Structure
```
Recoil-Force-Measurement/
│
├── raw-data/
│   ├── test_001.txt          # Raw load cell data (unmodified)
│   ├── test_002.txt
│   └── test_003.txt
│
├── analysis/
│   ├── force_analysis.xlsx   # Excel analysis workbook
│   │   ├── Sheet1: Original Data
│   │   └── Sheet2: Summary & Peak Forces
│   │
│   └── force_analysis_v2.xlsx
│
├── matlab-scripts/
│   ├── force_graph_analysis.m      # Main analysis script
│   ├── peak_detection.m            # Peak force detection
│   ├── plot_recoil_force.m        # Visualization
│   └── batch_analysis.m            # Multiple file processing
│
└── README.md
```

---

## 📄 File Descriptions

### 📝 .TXT Files (Raw Data)
**Purpose:** Store unmodified raw data received directly from load cell sensor

**Characteristics:**
- ✅ **Read-only** - Never modified or edited
- ✅ **Original measurements** - Direct sensor output
- ✅ **Timestamped data** - Force readings with time intervals
- ✅ **Archive quality** - Preserved for data integrity

**Format Example:**
```
Time(s)    Force(N)
0.000      0.125
0.001      0.248
0.002      15.634
0.003      125.847
...
```

### 📊 Excel Files (Data Analysis)

#### Sheet 1: Original Data
**Purpose:** Import and display raw data from .TXT files

**Contents:**
- Direct copy of .TXT file data
- Time series data
- Force measurements
- No modifications or calculations

**Columns:**
| Time (s) | Force (N) | Comments |
|----------|-----------|----------|
| 0.000    | 0.125     | -        |
| 0.001    | 0.248     | -        |

#### Sheet 2: Summary & Peak Forces
**Purpose:** Statistical analysis and peak force identification

**Contains:**
- 📈 Maximum peak force
- 📉 Minimum force
- 📊 Average force
- 🎯 Peak detection results
- ⏱️ Time to peak force
- 📉 Recoil duration
- 📋 Test summary statistics

**Analysis Metrics:**
| Metric | Value | Unit |
|--------|-------|------|
| Peak Force | XXX.XX | N |
| Average Force | XX.XX | N |
| Duration | X.XXX | s |
| Impulse | XXX.XX | N·s |

### 🔬 .M Files (MATLAB Analysis)
**Purpose:** Advanced graphical analysis and force pattern visualization

**Features:**
- 📈 Force-time graph plotting
- 🎯 Peak detection algorithms
- 📊 Statistical analysis
- 🔄 Batch processing capabilities
- 💾 Export results to images/data files

**Main Functions:**
```matlab
% Load and analyze recoil force data
% Plot force vs time graphs
% Detect peak forces automatically
% Calculate impulse and momentum
% Export analysis results
```

---

## 🚀 Usage

### 1️⃣ Data Collection
```bash
# Connect load cell to data acquisition system
# Start recording
# Save output as .TXT file in raw-data/ folder
# Do NOT modify the .TXT file
```

### 2️⃣ Excel Analysis
```excel
1. Open force_analysis.xlsx
2. Go to Sheet1 "Original Data"
3. Import data from .TXT file (Copy & Paste)
4. Go to Sheet2 "Summary & Peak Forces"
5. Review automatic calculations
6. Check peak force detection
7. Export summary if needed
```

### 3️⃣ MATLAB Analysis
```matlab
% Open MATLAB
cd('matlab-scripts')

% For single file analysis
force_graph_analysis('test_001.txt')

% For batch processing
batch_analysis('raw-data/')

% Plot results
plot_recoil_force('test_001.txt')
```

---

## 📊 Analysis Workflow

<details>
<summary><b>Step-by-Step Analysis Process</b></summary>

### Phase 1: Data Collection
1. Mount load cell in test fixture
2. Connect to data acquisition system
3. Configure sampling rate
4. Conduct test and record data
5. Save as .TXT file (raw, unmodified)

### Phase 2: Excel Processing
1. Import .TXT data to Sheet1
2. Verify data integrity
3. Sheet2 auto-calculates:
   - Peak forces
   - Average forces
   - Time metrics
   - Statistical summary

### Phase 3: MATLAB Analysis
1. Load data from .TXT or Excel
2. Apply filtering if needed
3. Generate force-time plots
4. Detect and mark peak forces
5. Calculate derived metrics
6. Export visualizations

</details>

---

## 📈 Sample Analysis Output

### Force-Time Graph
```
Force (N)
    │
200 │         ╱╲
    │        ╱  ╲
150 │       ╱    ╲
    │      ╱      ╲
100 │     ╱        ╲
    │    ╱          ╲___
 50 │   ╱                ╲___
    │  ╱                     ╲___
  0 │_╱___________________________╲___
    └─────────────────────────────────► Time (s)
    0    0.1   0.2   0.3   0.4   0.5
```

### Typical Results
| Test | Peak Force (N) | Time to Peak (ms) | Duration (ms) | Impulse (N·s) |
|------|----------------|-------------------|---------------|---------------|
| 001  | 185.4          | 45                | 250           | 15.6          |
| 002  | 192.1          | 42                | 245           | 16.2          |
| 003  | 178.9          | 48                | 260           | 14.8          |

---

## 🔧 Requirements

### Hardware
- ⚙️ Load cell sensor (appropriate capacity)
- 🔌 Data acquisition system
- 💻 Computer for analysis

### Software
- 📊 Microsoft Excel 2016 or later
- 🔬 MATLAB R2020a or later
- 📦 MATLAB Signal Processing Toolbox (recommended)

---

## 📦 MATLAB Dependencies
```matlab
% Required Toolboxes
- Signal Processing Toolbox
- Statistics and Machine Learning Toolbox (optional)

% Installation check
ver
```

---

## ⚙️ Configuration

<details>
<summary><b>Load Cell Settings</b></summary>

- **Sampling Rate:** 1000 Hz (1 ms intervals)
- **Measurement Range:** 0-500 N
- **Sensitivity:** 2 mV/V
- **Excitation Voltage:** 10V

</details>

<details>
<summary><b>Excel Settings</b></summary>

- **Decimal Places:** 3
- **Auto-calculation:** Enabled
- **Graph Type:** XY Scatter with lines

</details>

<details>
<summary><b>MATLAB Settings</b></summary>
```matlab
% Configuration parameters
sampling_rate = 1000;  % Hz
filter_cutoff = 100;   % Hz
plot_style = 'line';
export_format = 'png';
```

</details>

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| .TXT file won't open in Excel | Use "Import Data" → "From Text" |
| MATLAB can't find file | Check file path and working directory |
| Peak detection not working | Adjust threshold in MATLAB script |
| Excel formulas showing errors | Verify data range in Sheet2 |
| Graph looks noisy | Apply low-pass filter in MATLAB |

---

## 📸 Screenshots

> Add your screenshots here
```markdown
### Raw Data View
![Raw Data](path/to/raw-data-screenshot.png)

### Excel Analysis
![Excel Analysis](path/to/excel-screenshot.png)

### MATLAB Graph Output
![MATLAB Output](path/to/matlab-graph.png)
```

---

## 📝 Best Practices

1. **Data Integrity**
   - ⚠️ Never modify .TXT files
   - 📁 Keep backups of raw data
   - 📋 Document test conditions

2. **Analysis Workflow**
   - 🔄 Process data systematically
   - ✅ Verify results across tools
   - 📊 Compare Excel and MATLAB outputs

3. **Documentation**
   - 📝 Record test parameters
   - 🏷️ Use clear file naming
   - 📅 Include date/time stamps

---

## 🤝 Contributing

Improvements to analysis scripts are welcome!

1. Fork the repository
2. Create analysis branch (`git checkout -b feature/ImprovedAnalysis`)
3. Commit your changes
4. Push and create Pull Request

---

## 📚 References

- Load cell calibration standards
- Signal processing techniques
- Peak detection algorithms
- Recoil force analysis methods

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@pobpapon](https://github.com/pobpapon)
- Email: papon99@gmail.com

---

## 🙏 Acknowledgments

- Load cell manufacturer documentation
- MATLAB community
- Excel data analysis resources

---

<p align="center">
  📊 Accurate measurements for better analysis
</p>

<p align="center">
  ⭐ Star this repo if you find it useful!
</p>
