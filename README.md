# 🏏 Cricket Team Dashboard (IPL Analytics)

An interactive Streamlit dashboard for exploring IPL match data — overview statistics, visual analytics, and head-to-head team comparisons.

## Features

### Overview
- KPI metrics: total matches, total teams, venues, total rows.
- **Data Statistics** tab: toss decision distribution (bat vs field), win type distribution (runs vs wickets), and numerical summary statistics for the dataset.
- **Dataset Explorer** tab: column selector, adjustable row count, and global text search across selected columns.

### Visuals
- **Basic Charts**: matches played per team, wins per team, and top 10 most popular venues.
- **Advanced Charts**: win margin distribution (histogram with box plot), toss winner vs match winner pie chart, and matches-per-year trend (area chart).
- Global performance insights: average win margin by runs, average win margin by wickets, top-winning team, and most Player-of-the-Match awards.

### Analysis
- Select two teams to compare.
- Head-to-head win distribution between the selected teams.
- Individual team performance metrics: total matches, total wins, win percentage, and average win margin (runs).
- Toss strategy comparison (bat vs field) between the two teams.

## Requirements

```
streamlit
streamlit-option-menu
pandas
plotly
```

Install with:

```bash
pip install streamlit streamlit-option-menu pandas plotly
```

## Data

Place a file named **`IPL DATASET.csv`** in the same directory as the app script. Required columns include:

- `Match id`
- `Date`
- `Team1`, `Team2`
- `Venue`
- `Toss_Winner`, `Toss_Decision`
- `Match_Winner`
- `Win_Type` (e.g. `runs`, `wickets`)
- `Win_Margin`
- `Player_of_Match`

The `Date` column is parsed with mixed/day-first format support to derive a `Year` column for the yearly trend chart.

## Running the App

```bash
streamlit run app.py
```

(Replace `app.py` with the actual filename of the script.)

## Notes

- In the **Analysis** tab, click **"📊 Show Comparison Analysis"** after selecting two different teams to generate the comparison charts and metrics.
- If no historical matches exist between the selected teams, a notice is shown instead of the head-to-head chart.
- Team1 must be selected as a different team from Team2; otherwise a warning is displayed.
