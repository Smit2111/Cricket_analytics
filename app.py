import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

st.set_page_config(page_title="Cricket Team", layout="wide")

with st.sidebar:
    select = option_menu("Menu", ["Overview", "Visuals", "Analysis"],
                         icons=["table", "bar-chart", "person"],
                         menu_icon="cast",
                         default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#000000"},
                             "icon": {"color": "orange", "font-size": "20px"},
                             "nav-link": {
                                 "font-size": "16px",
                                 "text-align": "left",
                                 "margin": "0px",
                                 "--hover-color": "#eee",
                             },
                             "nav-link-selected": {"background-color": "#02ab21"},
                         }
                         )



df = pd.read_csv("IPL DATASET.csv")

if select == "Overview":
    st.title("🏏 Cricket Dashboard Overview")


    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Matches", df.shape[0])
    m2.metric("Total Teams", df["Team1"].nunique())
    m3.metric("Venues", df["Venue"].nunique())
    m4.metric("Total Rows", df.shape[0])

    st.divider()

    tab_stats, tab_explorer = st.tabs(["Data Statistics", "Dataset Explorer"])

    with tab_stats:
        st.subheader("Match Summary Insights")

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Toss Decision Distribution")
            toss_counts = df["Toss_Decision"].value_counts().reset_index()
            toss_counts.columns = ["Decision", "Count"]
            fig_toss = px.pie(
                toss_counts,
                values="Count",
                names="Decision",
                title="Bat vs Field Decisions",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_toss, use_container_width=True)

        with col_right:
            st.subheader("Win Type Distribution")
            win_counts = df["Win_Type"].value_counts().reset_index()
            win_counts.columns = ["Win Type", "Count"]
            fig_win = px.bar(
                win_counts,
                x="Win Type",
                y="Count",
                title="Wins by Runs vs Wickets",
                color="Win Type",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig_win, use_container_width=True)

        st.divider()
        st.subheader("Numerical Summary Statistics")
        num_stats = df.describe().T
        st.dataframe(num_stats, use_container_width=True)

    with tab_explorer:
        st.subheader("Dataset Preview & Filter")

        selected_columns = st.multiselect("Select Columns to Display", df.columns,
                                          default=["Match id", "Date", "Team1", "Team2", "Venue", "Match_Winner"])


        num_rows = st.slider("Number of rows to display", 5, 100, 20)


        search_query = st.text_input("Global Search (Team, Venue, etc.)")

        filtered_df = df[selected_columns]
        if search_query:
            mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            filtered_df = filtered_df[mask]

        st.dataframe(filtered_df.head(num_rows), use_container_width=True)
        st.info(f"Showing {min(num_rows, len(filtered_df))} of {len(filtered_df)} filtered records.")

if select == "Visuals":
    st.title("📊 Cricket Visual Analytics")


    tab_basic, tab_advance = st.tabs(["📉 Basic Charts", "🚀 Advanced Charts"])

    with tab_basic:
        st.subheader("General Match Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Matches Played per Team")
            all_teams = pd.concat([df['Team1'], df['Team2']])
            team_counts = all_teams.value_counts().reset_index()
            team_counts.columns = ['Team', 'Matches']
            fig_teams = px.bar(
                team_counts,
                x='Matches',
                y='Team',
                orientation='h',
                title="Total Matches Played by Each Team",
                color='Matches',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_teams, use_container_width=True)

        with col2:
            st.subheader("Wins per Team")
            win_counts = df['Match_Winner'].value_counts().reset_index()
            win_counts.columns = ['Team', 'Wins']
            fig_wins = px.bar(
                win_counts,
                x='Wins',
                y='Team',
                orientation='h',
                title="Total Matches Won by Each Team",
                color='Wins',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig_wins, use_container_width=True)

        st.divider()

        st.subheader("Top 10 Most Popular Venues")
        venue_counts = df['Venue'].value_counts().head(10).reset_index()
        venue_counts.columns = ['Venue', 'Matches']
        fig_venues = px.bar(
            venue_counts,
            x='Venue',
            y='Matches',
            title="Top 10 Stadiums by Match Count",
            color='Matches',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_venues, use_container_width=True)

    with tab_advance:
        st.subheader("Deep Dive Match Analytics")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Win Margin Distribution")
            fig_margin = px.histogram(
                df,
                x="Win_Margin",
                nbins=20,
                title="Frequency of Win Margins (Runs/Wickets)",
                color="Win_Type",
                marginal="box",  # Adds a box plot on top
                opacity=0.7
            )
            st.plotly_chart(fig_margin, use_container_width=True)

        with col4:
            st.subheader("Toss Winner vs Match Winner")
            df['Toss_Match_Winner'] = (df['Toss_Winner'] == df['Match_Winner']).map({True: 'Yes', False: 'No'})
            toss_win_stats = df['Toss_Match_Winner'].value_counts().reset_index()
            toss_win_stats.columns = ['Toss Winner Won?', 'Count']
            fig_toss_corr = px.pie(
                toss_win_stats,
                values='Count',
                names='Toss Winner Won?',
                title="Did the Toss Winner win the Match?",
                hole=0.4,
                color_discrete_sequence=['#1DB954', '#FF4B4B']
            )
            st.plotly_chart(fig_toss_corr, use_container_width=True)

        st.divider()

        st.subheader("Matches Trend Over the Years")
        # Ensure Date is in datetime format with mixed format support
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce', format='mixed')
        df['Year'] = df['Date'].dt.year
        yearly_matches = df.groupby('Year').size().reset_index(name='Matches')

        fig_trend = px.area(
            yearly_matches,
            x='Year',
            y='Matches',
            title="Total IPL Matches Played per Year",
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#FFA500']
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()
    st.subheader("🏆 Global Match Performance Insights")

    avg_run_margin = round(df[df['Win_Type'] == 'runs']['Win_Margin'].mean(), 1)
    avg_wicket_margin = round(df[df['Win_Type'] == 'wickets']['Win_Margin'].mean(), 1)
    top_team = df['Match_Winner'].value_counts().idxmax()
    top_player = df['Player_of_Match'].value_counts().idxmax()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Avg Win (Runs)", f"{avg_run_margin}")
    k2.metric("Avg Win (Wickets)", f"{avg_wicket_margin}")
    k3.metric("Top Team", top_team)
    k4.metric("MVP (Most POTM)", top_player)

if select == "Analysis":
    st.title("🏆 Team Comparison Analysis")
    st.subheader("Select Teams to Compare")

    teams = sorted(df['Team1'].unique())
    col1, col2 = st.columns(2)

    with col1:
        team1 = st.selectbox("Select Team 1", teams, index=0)
    with col2:
        team2 = st.selectbox("Select Team 2", teams, index=1)

    if team1 == team2:
        st.warning("Please select two different teams for comparison.")
    else:

        if st.button("📊 Show Comparison Analysis"):
            st.divider()

            h2h_df = df[((df['Team1'] == team1) & (df['Team2'] == team2)) | ((df['Team1'] == team2) & (df['Team2'] == team1))]

            if h2h_df.empty:
                st.info(f"No historical matches found between {team1} and {team2}.")
            else:
                st.subheader(f"⚔️ Head-to-Head: {team1} vs {team2}")
                h2h_wins = h2h_df['Match_Winner'].value_counts().reset_index()
                h2h_wins.columns = ['Team', 'Wins']

                fig_h2h = px.pie(
                    h2h_wins,
                    values='Wins',
                    names='Team',
                    title=f"Head-to-Head Win Distribution ({len(h2h_df)} matches)",
                    hole=0.4,
                    color_discrete_sequence=['#008080', '#FF7F50']
                )
                st.plotly_chart(fig_h2h, use_container_width=True)

            st.divider()
            st.subheader("📈 Individual Team Performance")


            # Team performance metrics
            def get_team_stats(team_name):
                t_df = df[(df['Team1'] == team_name) | (df['Team2'] == team_name)]
                total_m = len(t_df)
                total_w = len(df[df['Match_Winner'] == team_name])
                win_pct = round((total_w / total_m) * 100, 1) if total_m > 0 else 0
                avg_run_margin = round(
                    df[(df['Match_Winner'] == team_name) & (df['Win_Type'] == 'runs')]['Win_Margin'].mean(), 1)
                return total_m, total_w, win_pct, avg_run_margin


            t1_m, t1_w, t1_pct, t1_run = get_team_stats(team1)
            t2_m, t2_w, t2_pct, t2_run = get_team_stats(team2)


            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.markdown(f"### {team1}")
                st.metric("Total Matches", t1_m)
                st.metric("Total Wins", t1_w)
                st.metric("Win Percentage", f"{t1_pct}%")
                st.metric("Avg Win Margin (Runs)", t1_run)

            with m_col2:
                st.markdown(f"### {team2}")
                st.metric("Total Matches", t2_m)
                st.metric("Total Wins", t2_w)
                st.metric("Win Percentage", f"{t2_pct}%")
                st.metric("Avg Win Margin (Runs)", t2_run)

            st.divider()

            # Toss Decision Analysis for both teams
            st.subheader("🎯 Toss Strategy Comparison")
            t1_toss = df[(df['Toss_Winner'] == team1)]['Toss_Decision'].value_counts().reset_index()
            t1_toss.columns = ['Decision', 'Count']
            t1_toss['Team'] = team1

            t2_toss = df[(df['Toss_Winner'] == team2)]['Toss_Decision'].value_counts().reset_index()
            t2_toss.columns = ['Decision', 'Count']
            t2_toss['Team'] = team2

            toss_combined = pd.concat([t1_toss, t2_toss])

            fig_toss_compare = px.bar(
                toss_combined,
                x='Team',
                y='Count',
                color='Decision',
                barmode='group',
                title="Toss Decisions: Bat vs Field",
                color_discrete_map={'bat': 'gold', 'field': 'skyblue'}
            )
            st.plotly_chart(fig_toss_compare, use_container_width=True)
