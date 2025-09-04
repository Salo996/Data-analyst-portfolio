#!/usr/bin/env python3
"""
Simple Web Portfolio Dashboard Generator
=======================================

Creates web-optimized dashboard images for GitHub portfolio.
No special characters to avoid encoding issues.

Created by: Salomon Santiago Esquivel
Usage: python create_simple_web_dashboard.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np
import os

# Set style for web-optimized charts
plt.style.use('default')

class SimpleWebPortfolioDashboard:
    """Create web-optimized visualizations for GitHub portfolio"""
    
    def __init__(self):
        self.db_path = "../data/sales_data.db"
        self.output_dir = "../visualizations/web_portfolio"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Professional color scheme
        self.colors = {
            'primary': '#2E86C1',      
            'secondary': '#28B463',     
            'accent': '#F39C12',        
            'danger': '#E74C3C',        
            'purple': '#8E44AD',        
            'dark': '#2C3E50',          
            'light': '#ECF0F1'          
        }
        
        self.load_data()
        
    def load_data(self):
        """Load data from SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.products_df = pd.read_sql_query("SELECT * FROM products", self.conn)
            self.users_df = pd.read_sql_query("SELECT * FROM users", self.conn)
            self.carts_df = pd.read_sql_query("SELECT * FROM carts", self.conn)
            self.cart_items_df = pd.read_sql_query("SELECT * FROM cart_items", self.conn)
            print("Data loaded successfully for web portfolio")
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def create_main_portfolio_image(self):
        """Create the main portfolio showcase image"""
        print("Creating main portfolio showcase image...")
        
        # Perfect size for GitHub display (1200x630)
        fig = plt.figure(figsize=(16, 10))
        fig.patch.set_facecolor('white')
        
        # Create grid layout
        gs = fig.add_gridspec(3, 4, 
                            height_ratios=[0.4, 1.3, 1.3], 
                            width_ratios=[1, 1, 1, 1],
                            hspace=0.3, wspace=0.2,
                            top=0.92, bottom=0.08, left=0.06, right=0.94)
        
        # Main title
        fig.suptitle('Sales Performance Analytics Dashboard\nSalomon Santiago Esquivel - Data Analyst Portfolio', 
                     fontsize=22, fontweight='bold', y=0.96, color=self.colors['dark'])
        
        # Calculate data
        revenue_data = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum(), include_groups=False
        ).sort_values(ascending=False)
        
        age_segments = self.users_df.groupby(
            pd.cut(self.users_df['age'], bins=[0, 25, 35, 50, 100], 
                   labels=['Gen Z (<25)', 'Millennials (25-35)', 'Gen X (36-50)', 'Boomers (50+)'])
        ).size()
        
        customer_sales = self.carts_df.groupby('userId')['total'].sum().nlargest(12)
        rating_data = self.products_df.groupby('category')['rating'].mean()
        
        # KPI Row (Top)
        kpis = [
            ('Total Revenue', f'${self.carts_df["total"].sum():,.0f}', self.colors['primary']),
            ('Total Customers', f'{len(self.users_df)}', self.colors['secondary']),
            ('Total Orders', f'{len(self.carts_df)}', self.colors['accent']),
            ('Avg Order Value', f'${self.carts_df["total"].mean():.0f}', self.colors['danger'])
        ]
        
        for i, (title, value, color) in enumerate(kpis):
            ax = fig.add_subplot(gs[0, i])
            
            # KPI card with border
            ax.add_patch(plt.Rectangle((0.05, 0.15), 0.9, 0.7, 
                                     facecolor=color, alpha=0.1, 
                                     edgecolor=color, linewidth=3))
            
            ax.text(0.5, 0.65, value, ha='center', va='center', 
                   fontsize=18, fontweight='bold', color=color)
            ax.text(0.5, 0.35, title, ha='center', va='center', 
                   fontsize=11, fontweight='bold', color=self.colors['dark'])
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        # Chart 1: Revenue by Category (Middle Left)
        ax1 = fig.add_subplot(gs[1, :2])
        colors_list = [self.colors['accent'], self.colors['secondary'], 
                      self.colors['primary'], self.colors['danger']]
        
        bars1 = ax1.bar(revenue_data.index, revenue_data.values, 
                       color=colors_list[:len(revenue_data)], alpha=0.8, 
                       edgecolor='white', linewidth=2)
        
        ax1.set_title('Revenue Potential by Category', fontsize=16, fontweight='bold', 
                     pad=15, color=self.colors['dark'])
        ax1.set_ylabel('Revenue Potential ($)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45, labelsize=11)
        
        # Add value labels
        for bar, value in zip(bars1, revenue_data.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenue_data.values)*0.02,
                    f'${value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax1.grid(axis='y', alpha=0.3)
        ax1.set_facecolor('#fafafa')
        
        # Chart 2: Customer Segmentation (Middle Right)
        ax2 = fig.add_subplot(gs[1, 2:])
        
        wedges, texts, autotexts = ax2.pie(age_segments.values, 
                                          labels=age_segments.index, 
                                          autopct='%1.1f%%',
                                          colors=colors_list[:len(age_segments)], 
                                          startangle=90, explode=[0.08]*len(age_segments))
        
        ax2.set_title('Customer Age Segmentation', fontsize=16, fontweight='bold', 
                     pad=15, color=self.colors['dark'])
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
        
        # Chart 3: Top Customers (Bottom Left)
        ax3 = fig.add_subplot(gs[2, :2])
        
        bars3 = ax3.bar(range(len(customer_sales)), customer_sales.values, 
                       color=self.colors['secondary'], alpha=0.8, 
                       edgecolor='white', linewidth=1)
        
        ax3.set_title('Top 12 Customers by Total Spending', fontsize=16, fontweight='bold', 
                     pad=15, color=self.colors['dark'])
        ax3.set_ylabel('Total Spent ($)', fontsize=12)
        ax3.set_xlabel('Customer Rank', fontsize=12)
        
        ax3.grid(axis='y', alpha=0.3)
        ax3.set_facecolor('#fafafa')
        
        # Chart 4: Product Ratings (Bottom Right)
        ax4 = fig.add_subplot(gs[2, 2:])
        
        bars4 = ax4.bar(rating_data.index, rating_data.values, 
                       color=colors_list[:len(rating_data)], alpha=0.8,
                       edgecolor='white', linewidth=2)
        
        ax4.set_title('Average Product Rating by Category', fontsize=16, fontweight='bold', 
                     pad=15, color=self.colors['dark'])
        ax4.set_ylabel('Average Rating', fontsize=12)
        ax4.set_ylim(0, 5)
        ax4.tick_params(axis='x', rotation=45, labelsize=11)
        
        # Add value labels
        for bar, value in zip(bars4, rating_data.values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax4.grid(axis='y', alpha=0.3)
        ax4.set_facecolor('#fafafa')
        
        # Save main image
        main_path = f"{self.output_dir}/sales_performance_portfolio_main.png"
        plt.savefig(main_path, dpi=200, bbox_inches='tight', 
                   facecolor='white', pad_inches=0.1)
        plt.close()
        
        print(f"Main portfolio image saved: {main_path}")
        return main_path
        
    def create_thumbnail_image(self):
        """Create thumbnail for portfolio grid"""
        print("Creating thumbnail image...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
        fig.patch.set_facecolor('white')
        
        fig.suptitle('Sales Performance Analytics\nSalomon Santiago Esquivel', 
                     fontsize=14, fontweight='bold', y=0.95, color=self.colors['dark'])
        
        # Mini charts for thumbnail
        revenue_data = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum(), include_groups=False
        ).sort_values(ascending=False)
        
        # Chart 1
        bars1 = ax1.bar(revenue_data.index, revenue_data.values, 
                       color=[self.colors['accent'], self.colors['secondary'], 
                             self.colors['primary'], self.colors['danger']])
        ax1.set_title('Revenue by Category', fontsize=10, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45, labelsize=8)
        
        # Chart 2
        age_segments = self.users_df.groupby(
            pd.cut(self.users_df['age'], bins=[0, 25, 35, 50, 100], 
                   labels=['<25', '25-35', '36-50', '50+'])
        ).size()
        
        ax2.pie(age_segments.values, labels=age_segments.index, autopct='%1.0f%%',
               colors=[self.colors['primary'], self.colors['secondary'], 
                      self.colors['accent'], self.colors['danger']])
        ax2.set_title('Customer Segments', fontsize=10, fontweight='bold')
        
        # Chart 3
        customer_sales = self.carts_df.groupby('userId')['total'].sum().nlargest(8)
        ax3.bar(range(len(customer_sales)), customer_sales.values, 
               color=self.colors['secondary'])
        ax3.set_title('Top Customers', fontsize=10, fontweight='bold')
        ax3.set_xlabel('Customer Rank', fontsize=8)
        
        # Chart 4 - Key metrics
        ax4.axis('off')
        metrics_text = f"""KEY METRICS

Revenue: ${self.carts_df['total'].sum():,.0f}
Customers: {len(self.users_df)}
Orders: {len(self.carts_df)}
Avg Order: ${self.carts_df['total'].mean():.0f}

Technologies:
Python | SQL | pandas
matplotlib | SQLite"""
        
        ax4.text(0.1, 0.9, metrics_text, fontsize=9, fontweight='bold',
                color=self.colors['dark'], transform=ax4.transAxes, va='top')
        
        plt.tight_layout()
        
        # Save thumbnail
        thumb_path = f"{self.output_dir}/sales_performance_thumbnail.png"
        plt.savefig(thumb_path, dpi=150, bbox_inches='tight', 
                   facecolor='white', pad_inches=0.1)
        plt.close()
        
        print(f"Thumbnail saved: {thumb_path}")
        return thumb_path
        
    def generate_all_images(self):
        """Generate all web images"""
        print("Starting Web Portfolio Image Generation")
        print("=" * 50)
        
        try:
            results = {}
            
            results['main'] = self.create_main_portfolio_image()
            results['thumbnail'] = self.create_thumbnail_image()
            
            print("\n" + "=" * 50)
            print("SUCCESS: All web portfolio images created!")
            print(f"\nOutput directory: {os.path.abspath(self.output_dir)}")
            print("\nFiles created:")
            print(f"1. Main Portfolio Image: sales_performance_portfolio_main.png")
            print(f"2. Thumbnail Image: sales_performance_thumbnail.png")
            
            print(f"\nBusiness Metrics:")
            print(f"Revenue: ${self.carts_df['total'].sum():,.0f}")
            print(f"Customers: {len(self.users_df)}")
            print(f"Orders: {len(self.carts_df)}")
            
            print(f"\nReady for GitHub portfolio update!")
            
            return results
            
        except Exception as e:
            print(f"Error: {e}")
            return None
            
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()

def main():
    dashboard = SimpleWebPortfolioDashboard()
    results = dashboard.generate_all_images()
    
    if results:
        print(f"\nSUCCESS! Portfolio images ready!")
        print(f"Next: Copy these images to your portfolio repository")

if __name__ == "__main__":
    main()