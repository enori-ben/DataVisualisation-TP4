from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "cleaned_world_bank.csv"
RESULTS_DIR = ROOT_DIR / "results"

sns.set_theme(style="whitegrid", palette="deep")


def load_data():
    """Load the cleaned World Bank dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Cleaned dataset not found. Run data_preprocessing.py first."
        )

    return pd.read_csv(DATA_FILE)


def prepare_visualization_data(df):
    """Prepare data for GDP and life expectancy visualizations."""

    required_columns = [
        "GDP_Per_Capita",
        "Life_Expectancy",
        "Population"
    ]

    data = df.dropna(subset=required_columns).copy()

    data = data[
        (data["GDP_Per_Capita"] > 0)
        & (data["Population"] > 0)
    ]

    return data


def plot_scatter(data):
    """Create a scatter plot of GDP per capita and life expectancy."""

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=data,
        x="GDP_Per_Capita",
        y="Life_Expectancy",
        alpha=0.6,
        s=45
    )

    plt.xscale("log")
    plt.title("GDP per Capita vs Life Expectancy")
    plt.xlabel("GDP per Capita (log scale)")
    plt.ylabel("Life Expectancy (years)")
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / "01_scatter.png", dpi=300)
    plt.close()


def plot_bubble(data):
    """Create a bubble chart where bubble size represents population."""

    plt.figure(figsize=(11, 7))

    sizes = (
        data["Population"]
        / data["Population"].max()
        * 1200
    )

    plt.scatter(
        data["GDP_Per_Capita"],
        data["Life_Expectancy"],
        s=sizes,
        alpha=0.4,
        edgecolors="black",
        linewidths=0.3
    )

    plt.xscale("log")
    plt.title("Bubble Chart: GDP, Life Expectancy and Population")
    plt.xlabel("GDP per Capita (log scale)")
    plt.ylabel("Life Expectancy (years)")
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / "02_bubble.png", dpi=300)
    plt.close()


def plot_density(data):
    """Create a two-dimensional density visualization."""

    plt.figure(figsize=(10, 6))

    plt.hexbin(
        data["GDP_Per_Capita"],
        data["Life_Expectancy"],
        gridsize=35,
        bins="log",
        cmap="viridis",
        mincnt=1
    )

    plt.xscale("log")
    plt.colorbar(label="Logarithmic observation count")
    plt.title("2D Density: GDP per Capita vs Life Expectancy")
    plt.xlabel("GDP per Capita (log scale)")
    plt.ylabel("Life Expectancy (years)")
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / "03_density.png", dpi=300)
    plt.close()


def plot_correlation_heatmap(df):
    """Create a Pearson correlation matrix using complete observations."""

    columns = [
        "GDP_Per_Capita",
        "Life_Expectancy",
        "Internet_Users_Pct",
        "Population"
    ]

    correlation_data = df[columns].dropna()

    correlation = correlation_data.corr(method="pearson")

    plt.figure(figsize=(9, 7))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        vmin=-1,
        vmax=1,
        center=0
    )

    plt.title("Pearson Correlation Matrix")
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "04_correlation_heatmap.png",
        dpi=300
    )

    correlation.to_csv(RESULTS_DIR / "correlation.csv")
    plt.close()

    print(
        "Observations used for correlation:",
        len(correlation_data)
    )


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading cleaned dataset...")
    df = load_data()

    visualization_data = prepare_visualization_data(df)

    print(
        "Observations for scatter, bubble and density:",
        len(visualization_data)
    )

    print("Generating scatter plot...")
    plot_scatter(visualization_data)

    print("Generating bubble chart...")
    plot_bubble(visualization_data)

    print("Generating 2D density plot...")
    plot_density(visualization_data)

    print("Generating correlation heatmap...")
    plot_correlation_heatmap(df)

    print("\nAll visualizations have been generated successfully.")


if __name__ == "__main__":
    main()
