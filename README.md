# PSL 2026 Auction Statistics

An interactive dashboard for exploring the Pakistan Super League 2026 player auction: player roles, team squads and recorded sold prices, with written insights under every chart.

**Live app:** [psl2026auctionsstatistics-2026-umerhayatkhan.streamlit.app](https://psl2026auctionsstatistics-2026-umerhayatkhan.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50%2B-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-interactive%20charts-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-data%20analysis-150458?logo=pandas&logoColor=white)

---

## Overview

The 2026 PSL auction produced 135 player records across eight franchises. This project turns that cleaned dataset into a dashboard where you can filter by team and role and see how prices, roles and squads compare.

Every chart is followed by a short list of insights that is calculated from the current filters, so the commentary always matches what is on screen.

## Features

- **Filters:** narrow the data by team and player role from the sidebar.
- **Key metrics:** player records, average sold price, highest sold price and total recorded spend.
- **Top buys:** the highest-priced players, shown in their team's color.
- **Player Records by Role:** how the squads are split between batsmen, bowlers, all-rounders and wicketkeeper-batsmen.
- **Average Sold Price by Role:** which roles the franchises paid the most for.
- **Base Price vs Sold Price:** an interactive scatter plot colored by team, with player names on hover and a "sold = base" reference line.
- **Squad snapshot:** player count, total spend and average price for each franchise.
- **Dynamic insights:** bullet-point findings under each chart that update with the filters.
- **Data access:** browse the filtered records in a table and download them as CSV.

## Dataset

`psl2026_auction_clean.csv` contains one row per player record.

| Column | Description |
| --- | --- |
| `player_name` | Player name |
| `nationality` | Player's country |
| `role` | Batsman, Bowler, All-rounder or Wicketkeeper-Batsman |
| `acquisition_type` | Auction, Retention or Direct Signing |
| `category` | Player category (Platinum, Diamond, Gold, Silver, Emerging, Unknown) |
| `base_price_pkr_lakh` | Base price in PKR lakh (missing for direct signings) |
| `sold_price_pkr_lakh` | Recorded sold price in PKR lakh |
| `team` | Franchise that acquired the player |
| `overseas` | Whether the player is an overseas player |
| `retained_or_new` | Retained or New |

**Notes**
- All prices are in PKR lakh.
- Seven records have no base price, so they are left out of the base-vs-sold chart.
- The dashboard describes the recorded data and does not independently verify auction outcomes.

## Key Findings

Full-dataset highlights (the complete list is in [`INSIGHTS.md`](INSIGHTS.md)):

- Bowlers are the largest group with 54 records, ahead of batsmen with 40.
- All-rounders have the highest average sold price at about 324 lakh.
- Steve Smith has the highest recorded price at 1,400 lakh, followed by Saim Ayub at 1,260 lakh.
- Base and sold prices are strongly related (correlation about 0.88). 64% of players sold above their base price.

## Tech Stack

| Purpose | Tool |
| --- | --- |
| Web app | Streamlit |
| Data handling | Pandas |
| Charts | Plotly |
| Language | Python |

## Project Structure

```
.
├── app.py                        # Streamlit dashboard
├── psl2026_auction_clean.csv     # Cleaned auction dataset
├── INSIGHTS.md                   # Chart insights for the full dataset
├── requirements.txt              # Python dependencies
├── assets/                       # Optional images (see below)
│   ├── players/
│   └── teams/
└── README.md
```

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

The app opens at `http://localhost:8501`.

## Adding Player and Team Images

The dashboard shows colored initials for players by default. To use real images, add files named after the player or team in lowercase with underscores:

```
assets/players/saim_ayub.png
assets/teams/karachi_kings.png
```

PNG, JPG, JPEG and WEBP files are supported. Only add images you have the right to use.

Code Link:
https://colab.research.google.com/drive/1UxGWAG2UFyeW2cM_xLPSPsoebTw4GDHz?usp=sharing

## Customization

- **Team colors:** edit the `TEAM_COLORS` dictionary in `app.py`.
- **Role colors:** edit the `ROLE_COLORS` dictionary in `app.py`.
- **Theme:** the brand colors (`NAVY`, `GREEN`, `GOLD`) are defined at the top of `app.py`.

## Deployment

The app is deployed on [Streamlit Community Cloud](https://streamlit.io/cloud). To deploy your own copy, push the repository to GitHub, create a new app on Streamlit Community Cloud, select the repository and set `app.py` as the main file.

## Disclaimer

This is an independent educational project. It is not affiliated with or endorsed by the Pakistan Super League or any of its franchises. Team names and colors are used for identification only.

## Author

**Umer Hayat Khan**
Computer Systems Engineer (UET Peshawar), working on AI systems.

- GitHub: [@your-github-username](https://github.com/your-github-username)
- LinkedIn: [your-linkedin-profile](https://www.linkedin.com/in/your-linkedin-profile)

## Feedback

Found a bug or have a suggestion? Please open an issue on the repository.
