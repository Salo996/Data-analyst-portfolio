# Tableau Dashboard Creation Guide
**Market Intelligence Dashboard - Salomón Santiago Esquivel**

## 🎯 Dashboard Overview
Create a professional 4-page Tableau dashboard showcasing advanced data visualization skills for your portfolio.

---

## 📊 Dashboard 1: Executive Summary
**Purpose**: High-level KPIs for C-suite decision makers

### Data Source: `executive_summary.csv`

### Key Visualizations:
1. **KPI Cards** (Top row)
   - Total Market Cap: SUM(market_cap_billions)
   - Average Daily Return: AVG(daily_return_pct) 
   - Portfolio Companies: COUNTD(symbol)
   - Trading Days: COUNTD(date)

2. **Market Cap Treemap** (Left)
   - Size: market_cap_billions
   - Color: daily_return_pct (red-green gradient)
   - Labels: company names

3. **Performance Scatter Plot** (Right)
   - X-axis: volatility_pct
   - Y-axis: daily_return_pct
   - Size: market_cap_billions
   - Color: sector
   - Tooltip: company, all metrics

4. **Sector Performance Bar Chart** (Bottom)
   - X-axis: sector
   - Y-axis: AVG(daily_return_pct)
   - Color: risk_category

### Filters:
- Date Range Slider
- Sector (multi-select)
- Performance Category

---

## 📈 Dashboard 2: Competitive Analysis
**Purpose**: Lenovo vs competitors deep-dive

### Data Source: `competitive_analysis.csv`

### Key Visualizations:
1. **Competitive Ranking Table** (Top)
   - Columns: company, performance_rank, avg_daily_return_pct, volatility_pct, market_cap_billions
   - Highlight Lenovo row in blue
   - Sort by performance_rank

2. **Performance vs Risk Quadrant** (Left)
   - X-axis: volatility_pct
   - Y-axis: avg_daily_return_pct
   - Shape: company_type (circle for competitors, square for Lenovo)
   - Size: market_cap_billions
   - Add reference lines at averages

3. **Market Share Pie Chart** (Top Right)
   - Angle: market_cap_billions
   - Color: company
   - Highlight Lenovo slice

4. **Positive Days Comparison** (Bottom Right)
   - X-axis: company
   - Y-axis: positive_days_pct
   - Color: company_type
   - Add average reference line

### Calculated Fields:
```
// Market Leader Indicator
IF [Symbol] = 'AAPL' THEN 'Market Leader'
ELSEIF [Symbol] = 'LNVGY' THEN 'Lenovo (Focus)'
ELSE 'Competitor'
END
```

---

## ⚠️ Dashboard 3: Risk Analysis
**Purpose**: Portfolio risk assessment and monitoring

### Data Source: `risk_analysis.csv`

### Key Visualizations:
1. **Risk Heatmap** (Top)
   - Rows: company
   - Columns: date (weekly aggregation)
   - Color: volatility_pct (red intensity scale)
   - Size: volume_millions

2. **VaR Distribution** (Left)
   - X-axis: var_95_pct
   - Y-axis: COUNT(records)
   - Color: risk_level
   - Histogram/distribution chart

3. **Portfolio Concentration** (Right)
   - Angle: portfolio_weight_pct
   - Color: risk_level
   - Donut chart with risk warning zones

4. **Risk Timeline** (Bottom)
   - X-axis: date
   - Y-axis: AVG(volatility_pct) by sector
   - Color: sector
   - Line chart with trend analysis

### Risk Alerts:
- Text box showing companies with >4% volatility
- Color-coded risk levels throughout

---

## 📊 Dashboard 4: Time Series & Trends
**Purpose**: Historical performance and trend analysis

### Data Source: `timeseries_data.csv`

### Key Visualizations:
1. **Cumulative Returns** (Top)
   - X-axis: date
   - Y-axis: cumulative_return_pct
   - Color: company
   - Multiple line chart
   - Highlight Lenovo line

2. **Volume vs Performance** (Left)
   - X-axis: date
   - Y-axis: daily_return_pct (bars)
   - Y-axis (secondary): volume_millions (line)
   - Dual-axis chart

3. **Moving Average Convergence** (Right)
   - X-axis: date
   - Y-axis: close_price, ma_7_days, ma_30_days
   - Multiple lines per company
   - Filter for specific company

4. **Sector Rotation Heatmap** (Bottom)
   - Rows: sector
   - Columns: date (monthly)
   - Color: AVG(daily_return_pct)
   - Show sector momentum over time

---

## 🎨 Design Guidelines

### Color Scheme:
- **Primary**: #1f77b4 (Professional Blue)
- **Secondary**: #ff7f0e (Attention Orange)  
- **Success**: #2ca02c (Performance Green)
- **Warning**: #d62728 (Risk Red)
- **Neutral**: #7f7f7f (Gray)

### Typography:
- **Title**: Tableau Book, 16pt
- **Headers**: Tableau Medium, 12pt
- **Body**: Tableau Book, 10pt

### Layout:
- Clean white backgrounds
- Consistent spacing (10px margins)
- Professional grid alignment
- Responsive design for different screens

---

## 📋 Creation Steps

1. **Prepare Data**:
   ```bash
   cd C:\Users\salos\market-intelligence-dashboard\scripts
   python tableau_data_prep.py
   ```

2. **Open Tableau Public**:
   - File → Open → Browse to tableau/ folder
   - Connect to CSV files

3. **Create Worksheets**:
   - Build each visualization separately
   - Apply consistent formatting
   - Test interactivity

4. **Assemble Dashboards**:
   - Drag worksheets to dashboard canvas
   - Add filters and actions
   - Configure responsive layout

5. **Publish to Tableau Public**:
   - File → Save to Tableau Public
   - Title: "Market Intelligence Dashboard - Salomón Santiago"
   - Add description with portfolio link

---

## 🚀 Portfolio Integration

### Add to your portfolio website:
```html
<div class="col-4 col-12-medium">
    <article class="box style2">
        <a href="https://public.tableau.com/views/your-dashboard" class="image featured">
            <img src="images/tableau-dashboard.png" alt="Market Intelligence Dashboard" />
        </a>
        <h3><a href="#">Market Intelligence Dashboard</a></h3>
        <p>Advanced Tableau visualization analyzing $2.8 trillion in market cap across 15 technology companies. 
        Features competitive analysis, risk assessment, and executive KPIs with real-time API integration.</p>
    </article>
</div>
```

### Key Metrics to Highlight:
- **15 companies analyzed** (100% data collection success)
- **90 days** of market data
- **1,350+ data points** processed
- **4 interactive dashboards** created
- **Advanced SQL analytics** with 200+ lines of queries

This dashboard will demonstrate your ability to create executive-level business intelligence tools that drive strategic decisions!