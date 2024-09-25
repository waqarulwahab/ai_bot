import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def visualize_status_plot(valid_df, invalid_df, other_status_df):
    # Count occurrences for Valid and Invalid DataFrames
    valid_count = valid_df['status'].count()
    invalid_count = invalid_df['status'].count()

    # Any status not matching "Valid" or "Invalid" should be counted as "Other"
    other_count = other_status_df[~other_status_df['status'].isin(['Valid', 'Invalid'])]['status'].count()

    # Create the Plotly figure
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=['Valid'],
        y=[valid_count],
        name='Valid',
        marker_color='green'  # Green for Valid
    ))

    fig.add_trace(go.Bar(
        x=['Invalid'],
        y=[invalid_count],
        name='Invalid',
        marker_color='red'  # Red for Invalid
    ))

    fig.add_trace(go.Bar(
        x=['Other'],
        y=[other_count],
        name='Other',
        marker_color='yellow'  # Yellow for Other
    ))

    # Update layout
    fig.update_layout(
        title='Status Plot',
        xaxis_title='Status',
        yaxis_title='Count',
        barmode='group',
        xaxis_tickangle=-45
    )

    # Render the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)