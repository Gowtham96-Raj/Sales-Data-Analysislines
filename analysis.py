"""
Sales Data Analysis Project
Author: Gowtham Raj

This script:
1. Loads the sales dataset
2. Cleans and validates the data
3. Calculates key business metrics
4. Creates summary CSV files
5. Generates sales and profit charts
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd


def find_dataset() -> Path:
    """Find the sales CSV file in the current folder."""
    possible_names = [
        "sales_data.csv",
        "sales_data (1).csv",
        "Sales_data.csv",
        "Sales_Data.csv",
    ]

    for filename in possible_names:
        path = Path(filename)
        if path.exists():
            return path

    csv_files = list(Path(".").glob("*.csv"))
    if len(csv_files) == 1:
        return csv_files[0]

    raise FileNotFoundError(
        "Sales dataset not found. Keep analysis.py and the sales CSV file "
        "in the same folder."
    )


def load_and_clean_data(csv_path: Path) -> pd.DataFrame:
    """Load, validate, and clean the sales dataset."""
    df = pd.read_csv(csv_path)

    required_columns = {
        "Order_ID",
        "Date",
        "Region",
        "Product",
        "Sales",
        "Profit",
    }

    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")

    df = df.drop_duplicates()
    df = df.dropna(
        subset=["Order_ID", "Date", "Region", "Product", "Sales", "Profit"]
    )

    df["Profit_Margin_Percent"] = (
        df["Profit"] / df["Sales"] * 100
    ).round(2)

    return df


def print_kpis(df: pd.DataFrame) -> None:
    """Display the main business KPIs."""
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()
    average_order_value = total_sales / total_orders if total_orders else 0
    profit_margin = total_profit / total_sales * 100 if total_sales else 0

    best_region = (
        df.groupby("Region")["Sales"].sum().idxmax()
        if not df.empty
        else "N/A"
    )
    best_product = (
        df.groupby("Product")["Sales"].sum().idxmax()
        if not df.empty
        else "N/A"
    )

    print("\nSALES PERFORMANCE SUMMARY")
    print("-" * 35)
    print(f"Total Sales: ₹{total_sales:,.2f}")
    print(f"Total Profit: ₹{total_profit:,.2f}")
    print(f"Total Orders: {total_orders}")
    print(f"Average Order Value: ₹{average_order_value:,.2f}")
    print(f"Overall Profit Margin: {profit_margin:.2f}%")
    print(f"Top Region by Sales: {best_region}")
    print(f"Top Product by Sales: {best_product}")


def create_summaries(df: pd.DataFrame, output_dir: Path) -> None:
    """Create region, product, and monthly summary files."""
    output_dir.mkdir(exist_ok=True)

    region_summary = (
        df.groupby("Region", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .sort_values("Total_Sales", ascending=False)
    )
    region_summary["Profit_Margin_Percent"] = (
        region_summary["Total_Profit"]
        / region_summary["Total_Sales"]
        * 100
    ).round(2)

    product_summary = (
        df.groupby("Product", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    monthly_summary = (
        df.assign(Month=df["Date"].dt.to_period("M").astype(str))
        .groupby("Month", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
        )
    )

    region_summary.to_csv(output_dir / "region_summary.csv", index=False)
    product_summary.to_csv(output_dir / "product_summary.csv", index=False)
    monthly_summary.to_csv(output_dir / "monthly_summary.csv", index=False)

    print("\nREGION SUMMARY")
    print(region_summary.to_string(index=False))

    print("\nPRODUCT SUMMARY")
    print(product_summary.to_string(index=False))


def create_charts(df: pd.DataFrame, output_dir: Path) -> None:
    """Generate portfolio-ready sales and profit charts."""
    output_dir.mkdir(exist_ok=True)

    regional_sales = (
        df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    )
    regional_sales.plot(kind="bar", title="Total Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Sales (₹)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / "sales_by_region.png", dpi=300)
    plt.close()

    product_profit = (
        df.groupby("Product")["Profit"].sum().sort_values(ascending=False)
    )
    product_profit.plot(kind="bar", title="Total Profit by Product")
    plt.xlabel("Product")
    plt.ylabel("Profit (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "profit_by_product.png", dpi=300)
    plt.close()

    daily_sales = df.groupby("Date")["Sales"].sum().sort_index()
    daily_sales.plot(
        kind="line",
        marker="o",
        title="Sales Trend Over Time",
    )
    plt.xlabel("Date")
    plt.ylabel("Sales (₹)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "sales_trend.png", dpi=300)
    plt.close()


def main() -> None:
    """Run the complete sales analysis."""
    try:
        csv_path = find_dataset()
        print(f"Dataset loaded: {csv_path.name}")

        sales_data = load_and_clean_data(csv_path)

        if sales_data.empty:
            raise ValueError("The dataset contains no valid rows after cleaning.")

        output_dir = Path("output")
        print_kpis(sales_data)
        create_summaries(sales_data, output_dir)
        create_charts(sales_data, output_dir)

        sales_data.to_csv(output_dir / "cleaned_sales_data.csv", index=False)

        print("\nAnalysis completed successfully.")
        print("Results and charts are available in the 'output' folder.")

    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
