import plotly.graph_objects as go
import numpy as np

def plot_transaction_distribution(df, results, mean, std):

    if mean is not None and std is not None:
        upper = mean + 2 * std
        lower = mean - 2 * std
    else:
        upper, lower = None, None

    fig = go.Figure()

    # -----------------------
    # BINNING
    # -----------------------
    bins = np.histogram_bin_edges(df["amount"], bins=20)
    counts, edges = np.histogram(df["amount"], bins=bins)

    bin_centers = [(edges[i] + edges[i+1]) / 2 for i in range(len(edges)-1)]
    bin_labels = [
        f"£{int(edges[i])} - £{int(edges[i+1])}"
        for i in range(len(edges)-1)
    ]

    # -----------------------
    # HISTOGRAM
    # -----------------------
    fig.add_trace(go.Bar(
        x=bin_centers,
        y=counts,
        name="Transactions",
        marker=dict(color="#4F46E5"),
        customdata=bin_labels,
        hovertemplate="%{customdata}<br>%{y} transactions<extra></extra>"
    ))

    # -----------------------
    # ANOMALIES
    # -----------------------
    if results:
        anomaly_amounts = [r["amount"] for r in results]

        fig.add_trace(go.Scatter(
            x=anomaly_amounts,
            y=[max(counts) * 0.15] * len(anomaly_amounts),
            mode="markers",
            name="Anomalies",
            marker=dict(color="red", size=10),
            customdata=[
                (r["user_id"], r["z_score"]) for r in results
            ],
            hovertemplate=(
                "User ID: %{customdata[0]}<br>"
                "Amount: £%{x}<br>"
                "Z-Score: %{customdata[1]:.2f}"
                "<extra></extra>"
            )
        ))

    # -----------------------
    # LINES
    # -----------------------
    fig.add_vline(
        x=mean,
        line_dash="dash",
        line_color="black",
        line_width=2,
        annotation_text="Mean",
        annotation_position="top",
        annotation_font=dict(color="black")
    )

    if upper is not None:
        fig.add_vline(
            x=upper,
            line_dash="dot",
            line_color="red",
            line_width=2,
            annotation_text="High Threshold",
            annotation_position="top",
            annotation_font=dict(color="black")
        )

    if lower is not None:
        fig.add_vline(
            x=lower,
            line_dash="dot",
            line_color="red",
            line_width=2,
            annotation_text="Low Threshold",
            annotation_position="top",
            annotation_font=dict(color="black")
        )

    # -----------------------
    # LAYOUT
    # -----------------------
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="black", size=12),

        xaxis=dict(
            title="Transaction Amount (£)",
            title_font=dict(color="black"),
            tickfont=dict(color="black"),
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            linecolor="black",
            tickcolor="black",
            zeroline=False,
            tickformat="£,.0f",
            type="log"
        ),

        yaxis=dict(
            title="Transactions",
            title_font=dict(color="black"),
            tickfont=dict(color="black"),
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            linecolor="black",
            tickcolor="black",
            zeroline=False
        ),

        legend=dict(font=dict(color="black")),
        showlegend=True
    )

    return fig