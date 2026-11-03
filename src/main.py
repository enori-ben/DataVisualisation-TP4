from .data_preprocessing import main as preprocess_data
from .visualizations import main as generate_visualizations
from .interactive_visualizations import main as generate_interactive_visualizations
from .network_analysis import main as generate_network_analysis


def main():
    print("\n========== DATA PREPROCESSING ==========")
    preprocess_data()

    print("\n========== STATIC VISUALIZATIONS ==========")
    generate_visualizations()

    print("\n========== INTERACTIVE VISUALIZATIONS ==========")
    generate_interactive_visualizations()

    print("\n========== NETWORK ANALYSIS ==========")
    generate_network_analysis()

    print("\n========== PROJECT COMPLETED ==========")


if __name__ == "__main__":
    main()
