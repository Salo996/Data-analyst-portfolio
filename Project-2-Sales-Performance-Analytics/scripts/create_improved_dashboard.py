#!/usr/bin/env python3
"""
IMPROVED Sales Performance Analytics - Professional Dashboard
============================================================

This script creates an enhanced, professional dashboard with better spacing,
larger charts, and improved visual presentation for portfolio showcase.

Created by: Salomón Santiago Esquivel
Project: Sales Performance Analytics Dashboard - IMPROVED VERSION

Usage:
    python create_improved_dashboard.py
    
Key Improvements:
    - Larger figure sizes for better readability
    - Better spacing between charts
    - Enhanced color schemes and typography
    - Professional layout for portfolio presentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime
import numpy as np
import os

# Set style for professional charts
plt.style.use('default')  # Using default for better control
sns.set_palette("husl")

class ImprovedSalesVisualizationDashboard:
    """Create professional, well-spaced visualizations for Sales Performance Analytics"""
    
    def __init__(self):
        self.db_path = "../data/sales_data.db"
        self.output_dir = "../visualizations"
        
        # Create visualizations directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Enhanced professional color scheme
        self.colors = {
            'primary': '#1f77b4',      # Professional blue
            'secondary': '#2ca02c',     # Success green  
            'accent': '#ff7f0e',        # Warning orange
            'danger': '#d62728',        # Alert red
            'purple': '#9467bd',        # Purple
            'brown': '#8c564b',         # Brown
            'pink': '#e377c2',          # Pink
            'gray': '#7f7f7f',          # Gray
            'olive': '#bcbd22',         # Olive
            'cyan': '#17becf'           # Cyan
        }
        
        # Load data
        self.load_data()
        
    def load_data(self):
        """Load data from SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            
            # Load main datasets
            self.products_df = pd.read_sql_query("SELECT * FROM products", self.conn)
            self.users_df = pd.read_sql_query("SELECT * FROM users", self.conn)
            self.carts_df = pd.read_sql_query("SELECT * FROM carts", self.conn)
            self.cart_items_df = pd.read_sql_query("SELECT * FROM cart_items", self.conn)
            
            print(f"Data loaded successfully:")
            print(f"   - Products: {len(self.products_df)} items")
            print(f"   - Users: {len(self.users_df)} customers")  
            print(f"   - Carts: {len(self.carts_df)} transactions")
            print(f"   - Cart Items: {len(self.cart_items_df)} line items")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def create_comprehensive_professional_dashboard(self):
        """Create a single, large, well-spaced professional dashboard"""
        print("\nCreating Comprehensive Professional Dashboard...")
        
        # Calculate all necessary data
        # Revenue data
        revenue_data = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum()
        ).sort_values(ascending=False)
        
        # Customer segmentation
        def categorize_age(age):
            if age < 25:
                return 'Gen Z\n(<25)'
            elif 25 <= age <= 35:
                return 'Millennials\n(25-35)'
            elif 36 <= age <= 50:
                return 'Gen X\n(36-50)'
            else:
                return 'Boomers\n(50+)'
        
        self.users_df['age_segment'] = self.users_df['age'].apply(categorize_age)
        age_segments = self.users_df['age_segment'].value_counts()
        
        # Customer sales analysis
        customer_sales = self.carts_df.groupby('userId')['total'].sum().sort_values(ascending=False)[:15]
        
        # Product ratings by category
        rating_data = self.products_df.groupby('category')['rating'].mean()
        
        # Create the large professional dashboard
        fig = plt.figure(figsize=(24, 16))  # Much larger figure size
        fig.patch.set_facecolor('white')
        
        # Create custom grid layout with more space
        gs = fig.add_gridspec(3, 3, 
                            height_ratios=[0.4, 1.3, 1.3], 
                            width_ratios=[1, 1, 1],
                            hspace=0.35,  # More vertical space
                            wspace=0.25,  # More horizontal space
                            top=0.92,     # Leave space for title
                            bottom=0.08,  # Bottom margin
                            left=0.06,    # Left margin
                            right=0.94)   # Right margin
        
        # Main title
        fig.suptitle('Sales Performance Analytics Dashboard\nSalomón Santiago Esquivel - Data Analyst Portfolio', 
                     fontsize=28, fontweight='bold', y=0.96, color='#2c3e50')
        
        # KPI Summary Row (Top)
        kpi_metrics = [
            ('Total Revenue', f'${self.carts_df["total"].sum():,.0f}', self.colors['primary']),
            ('Total Customers', f'{len(self.users_df):,}', self.colors['secondary']),
            ('Avg Order Value', f'${self.carts_df["total"].mean():.0f}', self.colors['accent'])
        ]
        
        for i, (title, value, color) in enumerate(kpi_metrics):
            ax = fig.add_subplot(gs[0, i])
            
            # Create KPI card with border
            ax.add_patch(plt.Rectangle((0.05, 0.15), 0.9, 0.7, 
                                     facecolor=color, alpha=0.1, 
                                     edgecolor=color, linewidth=3))
            
            ax.text(0.5, 0.65, value, ha='center', va='center', 
                   fontsize=24, fontweight='bold', color=color)
            ax.text(0.5, 0.35, title, ha='center', va='center', 
                   fontsize=14, fontweight='bold', color='#34495e')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        # Chart 1: Revenue Potential by Category (Middle Left)
        ax1 = fig.add_subplot(gs[1, 0])
        colors_list = [self.colors['accent'], self.colors['secondary'], 
                      self.colors['primary'], self.colors['danger']]
        
        bars1 = ax1.bar(revenue_data.index, revenue_data.values, 
                       color=colors_list[:len(revenue_data)], 
                       alpha=0.8, edgecolor='white', linewidth=2)
        
        ax1.set_title('Revenue Potential by Category', fontsize=18, fontweight='bold', 
                     pad=20, color='#2c3e50')
        ax1.set_ylabel('Revenue Potential ($)', fontsize=14, color='#34495e')
        ax1.tick_params(axis='x', rotation=45, labelsize=12)
        ax1.tick_params(axis='y', labelsize=12)
        
        # Add value labels on bars
        for bar, value in zip(bars1, revenue_data.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenue_data.values)*0.02,
                    f'${value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Grid and styling
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        ax1.set_facecolor('#fafafa')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # Chart 2: Customer Age Segmentation (Middle Center)
        ax2 = fig.add_subplot(gs[1, 1])
        
        wedges, texts, autotexts = ax2.pie(age_segments.values, 
                                          labels=age_segments.index, 
                                          autopct='%1.1f%%',
                                          colors=colors_list[:len(age_segments)], 
                                          startangle=90, 
                                          explode=[0.08]*len(age_segments),
                                          shadow=True)
        
        ax2.set_title('Customer Age Segmentation', fontsize=18, fontweight='bold', 
                     pad=20, color='#2c3e50')
        
        # Enhance pie chart text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(12)
        
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
        
        # Chart 3: Top 15 Customers by Total Spending (Middle Right)
        ax3 = fig.add_subplot(gs[1, 2])
        
        bars3 = ax3.bar(range(len(customer_sales)), customer_sales.values, 
                       color=self.colors['secondary'], alpha=0.8, 
                       edgecolor='white', linewidth=2)
        
        ax3.set_title('Top 15 Customers by Total Spending', fontsize=18, fontweight='bold', 
                     pad=20, color='#2c3e50')
        ax3.set_ylabel('Total Spent ($)', fontsize=14, color='#34495e')
        ax3.set_xlabel('Customer Rank', fontsize=14, color='#34495e')
        ax3.tick_params(labelsize=12)
        
        # Grid and styling
        ax3.grid(axis='y', alpha=0.3, linestyle='--')
        ax3.set_facecolor('#fafafa')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        
        # Chart 4: Average Product Rating by Category (Bottom Left)
        ax4 = fig.add_subplot(gs[2, 0])
        
        bars4 = ax4.bar(rating_data.index, rating_data.values, 
                       color=colors_list[:len(rating_data)], 
                       alpha=0.8, edgecolor='white', linewidth=2)
        
        ax4.set_title('Average Product Rating by Category', fontsize=18, fontweight='bold', 
                     pad=20, color='#2c3e50')
        ax4.set_ylabel('Average Rating', fontsize=14, color='#34495e')
        ax4.set_ylim(0, 5)
        ax4.tick_params(axis='x', rotation=45, labelsize=12)
        ax4.tick_params(axis='y', labelsize=12)
        
        # Add value labels
        for bar, value in zip(bars4, rating_data.values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Grid and styling
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
        ax4.set_facecolor('#fafafa')
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        
        # Chart 5: Customer Value Distribution (Bottom Center)
        ax5 = fig.add_subplot(gs[2, 1])
        
        spending_distribution = self.carts_df.groupby('userId')['total'].sum()
        
        ax5.hist(spending_distribution, bins=20, alpha=0.8, 
                color=self.colors['purple'], edgecolor='white', linewidth=1)
        ax5.set_title('Customer Spending Distribution', fontsize=18, fontweight='bold', 
                     pad=20, color='#2c3e50')
        ax5.set_xlabel('Total Spent ($)', fontsize=14, color='#34495e')
        ax5.set_ylabel('Number of Customers', fontsize=14, color='#34495e')
        ax5.tick_params(labelsize=12)
        
        # Grid and styling
        ax5.grid(axis='y', alpha=0.3, linestyle='--')
        ax5.set_facecolor('#fafafa')
        ax5.spines['top'].set_visible(False)
        ax5.spines['right'].set_visible(False)
        
        # Chart 6: Key Business Insights (Bottom Right)
        ax6 = fig.add_subplot(gs[2, 2])
        ax6.axis('off')
        
        # Create insights box
        ax6.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, 
                                   facecolor='#ecf0f1', alpha=0.8, 
                                   edgecolor=self.colors['primary'], linewidth=2))
        
        # Calculate key insights
        top_category = revenue_data.index[0]
        avg_age = self.users_df['age'].mean()
        repeat_customers = len(self.carts_df.groupby('userId').filter(lambda x: len(x) > 1))
        top_rating = self.products_df['rating'].max()
        
        insights = [
            "KEY BUSINESS INSIGHTS",
            "",
            f"💼 {top_category.title()} leads revenue potential",
            f"👥 Average customer age: {avg_age:.0f} years",
            f"🔄 {repeat_customers} repeat customers ({repeat_customers/len(self.users_df)*100:.0f}%)",
            f"⭐ Highest product rating: {top_rating:.1f}/5.0",
            "",
            "STRATEGIC RECOMMENDATIONS",
            "",
            "🎯 Focus marketing on top category",
            "💡 Develop retention programs",  
            "🚀 Optimize high-rated products",
            "📊 Target primary age segment"
        ]
        
        for i, insight in enumerate(insights):
            if insight in ["KEY BUSINESS INSIGHTS", "STRATEGIC RECOMMENDATIONS"]:
                weight = 'bold'
                size = 14
                color = self.colors['primary']
            elif insight == "":
                continue
            else:
                weight = 'normal'
                size = 12
                color = '#2c3e50'
            
            ax6.text(0.1, 0.9 - i*0.065, insight, fontsize=size, fontweight=weight, 
                    color=color, transform=ax6.transAxes, va='top')
        
        # Save the improved dashboard
        chart_path = f"{self.output_dir}/improved_sales_performance_dashboard.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white', 
                   pad_inches=0.2)
        plt.close()
        
        print(f"Improved Dashboard saved: {chart_path}")
        return chart_path
        
    def create_individual_enhanced_charts(self):
        """Create individual enhanced charts with better spacing"""
        print("\nCreating Individual Enhanced Charts...")
        
        charts_created = []
        
        # 1. Enhanced Revenue Chart
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor('white')
        
        revenue_data = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum()
        ).sort_values(ascending=False)
        
        colors = [self.colors['accent'], self.colors['secondary'], 
                 self.colors['primary'], self.colors['danger']]
        
        bars = ax.bar(revenue_data.index, revenue_data.values, 
                     color=colors[:len(revenue_data)], 
                     alpha=0.8, edgecolor='white', linewidth=3)
        
        ax.set_title('Revenue Potential by Category\nSalomón Santiago Esquivel - Data Analyst Portfolio', 
                    fontsize=20, fontweight='bold', pad=30, color='#2c3e50')
        ax.set_ylabel('Revenue Potential ($)', fontsize=16, color='#34495e')
        ax.tick_params(axis='x', rotation=45, labelsize=14)
        ax.tick_params(axis='y', labelsize=14)
        
        # Add value labels
        for bar, value in zip(bars, revenue_data.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenue_data.values)*0.02,
                   f'${value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=14)
        
        # Enhanced styling
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_facecolor('#fafafa')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        revenue_path = f"{self.output_dir}/enhanced_revenue_chart.png"
        plt.savefig(revenue_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        charts_created.append(revenue_path)
        
        # 2. Enhanced Customer Segmentation Chart
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        fig.patch.set_facecolor('white')
        
        def categorize_age(age):
            if age < 25:
                return 'Gen Z\n(<25)'
            elif 25 <= age <= 35:
                return 'Millennials\n(25-35)'
            elif 36 <= age <= 50:
                return 'Gen X\n(36-50)'
            else:
                return 'Boomers\n(50+)'
        
        self.users_df['age_segment'] = self.users_df['age'].apply(categorize_age)
        age_segments = self.users_df['age_segment'].value_counts()
        
        wedges, texts, autotexts = ax.pie(age_segments.values, 
                                         labels=age_segments.index, 
                                         autopct='%1.1f%%',
                                         colors=colors[:len(age_segments)], 
                                         startangle=90, 
                                         explode=[0.1]*len(age_segments),
                                         shadow=True,
                                         textprops={'fontsize': 14})
        
        ax.set_title('Customer Age Segmentation\nSalomón Santiago Esquivel - Data Analyst Portfolio', 
                    fontsize=20, fontweight='bold', pad=30, color='#2c3e50')
        
        # Enhance text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(14)
        
        plt.tight_layout()
        segment_path = f"{self.output_dir}/enhanced_customer_segmentation.png"
        plt.savefig(segment_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        charts_created.append(segment_path)
        
        print(f"Enhanced charts created: {len(charts_created)} charts")
        return charts_created
        
    def generate_all_improved_visualizations(self):
        """Generate all improved visualizations"""
        print("Starting IMPROVED Sales Performance Analytics Visualization Generation")
        print("=" * 80)
        
        try:
            # Generate comprehensive dashboard
            dashboard_path = self.create_comprehensive_professional_dashboard()
            
            # Generate individual enhanced charts
            individual_charts = self.create_individual_enhanced_charts()
            
            print("\n" + "=" * 80)
            print("All IMPROVED visualizations created successfully!")
            print(f"\nOutput directory: {self.output_dir}")
            print(f"Charts created:")
            print(f"   1. Comprehensive Professional Dashboard (MAIN)")
            print(f"   2. Enhanced Revenue Chart")
            print(f"   3. Enhanced Customer Segmentation Chart")
            
            # Summary statistics
            total_revenue = self.carts_df['total'].sum()
            total_customers = len(self.users_df)
            avg_order_value = self.carts_df['total'].mean()
            
            print(f"\nKey Business Insights:")
            print(f"   - Total Revenue Analyzed: ${total_revenue:,.0f}")
            print(f"   - Customer Base: {total_customers} customers")
            print(f"   - Average Order Value: ${avg_order_value:.0f}")
            
            print(f"\nReady for professional portfolio presentation!")
            
            return {
                'main_dashboard': dashboard_path,
                'individual_charts': individual_charts,
                'total_revenue': total_revenue,
                'total_customers': total_customers,
                'avg_order_value': avg_order_value
            }
            
        except Exception as e:
            print(f"Error generating improved visualizations: {e}")
            return None
        
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()

def main():
    """Main execution function"""
    dashboard = ImprovedSalesVisualizationDashboard()
    results = dashboard.generate_all_improved_visualizations()
    
    if results:
        print(f"\nSuccess! Your IMPROVED Sales Performance Analytics visualizations are ready.")
        print(f"Main dashboard: {results['main_dashboard']}")
        print(f"Use these professional charts for your portfolio and interviews!")
    else:
        print(f"\nFailed to generate improved visualizations. Please check the data and try again.")

if __name__ == "__main__":
    main()