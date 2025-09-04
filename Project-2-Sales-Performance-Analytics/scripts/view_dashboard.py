#!/usr/bin/env python3
"""
Dashboard Viewer for VS Code
============================

Simple script to display the improved dashboard in VS Code using matplotlib.
This allows you to view the results directly in your development environment.

Created by: Salomón Santiago Esquivel
Usage: python view_dashboard.py
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def view_improved_dashboard():
    """Display the improved dashboard in VS Code"""
    
    # Path to the improved dashboard
    dashboard_path = "../visualizations/improved_sales_performance_dashboard.png"
    
    if not os.path.exists(dashboard_path):
        print(f"Dashboard not found at: {dashboard_path}")
        print("Please run create_improved_dashboard.py first")
        return
    
    # Load and display the image
    img = mpimg.imread(dashboard_path)
    
    # Create figure with the exact size to avoid rescaling
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    ax.imshow(img)
    ax.axis('off')  # Hide axes for clean display
    
    plt.title('Improved Sales Performance Analytics Dashboard', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    
    print("Displaying improved dashboard...")
    print("Close the plot window to continue.")
    
    # Show the plot
    plt.show()
    
    print("Dashboard viewing complete!")
    
    # Also show file information
    print(f"\nDashboard saved at: {os.path.abspath(dashboard_path)}")
    print("Key improvements made:")
    print("✅ Larger figure size (24x16 instead of 16x12)")
    print("✅ Better spacing between charts (hspace=0.35, wspace=0.25)")
    print("✅ Professional color scheme and typography")
    print("✅ Enhanced KPI cards with borders")
    print("✅ Improved grid styling and background colors")
    print("✅ Better text formatting and sizing")
    print("✅ Strategic business insights panel")

def view_comparison():
    """View original vs improved dashboard side by side"""
    
    original_path = "../visualizations/sales_performance_analytics_portfolio_showcase.png"
    improved_path = "../visualizations/improved_sales_performance_dashboard.png"
    
    if not os.path.exists(original_path) or not os.path.exists(improved_path):
        print("Both dashboard files need to exist for comparison")
        return
    
    # Load images
    original_img = mpimg.imread(original_path)
    improved_img = mpimg.imread(improved_path)
    
    # Create side-by-side comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))
    
    ax1.imshow(original_img)
    ax1.set_title('Original Dashboard', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    ax2.imshow(improved_img)
    ax2.set_title('Improved Dashboard', fontsize=14, fontweight='bold')
    ax2.axis('off')
    
    fig.suptitle('Dashboard Comparison: Original vs Improved', 
                 fontsize=18, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    print("Comparison complete!")

def main():
    """Main function with menu"""
    print("Sales Performance Analytics Dashboard Viewer")
    print("=" * 50)
    print("1. View Improved Dashboard")
    print("2. View Original vs Improved Comparison")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == '1':
        view_improved_dashboard()
    elif choice == '2':
        view_comparison()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice. Please run again.")

if __name__ == "__main__":
    main()