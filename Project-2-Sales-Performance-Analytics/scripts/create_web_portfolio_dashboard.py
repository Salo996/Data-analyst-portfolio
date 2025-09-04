#!/usr/bin/env python3
"""
Web Portfolio Dashboard Generator
================================

Creates web-optimized dashboard images specifically for GitHub portfolio display.
Optimized for web viewing with proper aspect ratios and file sizes.

Created by: Salomón Santiago Esquivel
Project: Sales Performance Analytics Dashboard - WEB PORTFOLIO VERSION

Usage:
    python create_web_portfolio_dashboard.py
    
Features:
    - Web-optimized dimensions (16:9 aspect ratio)
    - Smaller file sizes for faster loading
    - Professional portfolio presentation
    - Multiple format options (thumbnail, full-size, showcase)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime
import numpy as np
import os

# Set style for web-optimized charts
plt.style.use('default')
sns.set_palette("husl")

class WebPortfolioDashboard:
    """Create web-optimized visualizations for GitHub portfolio"""
    
    def __init__(self):
        self.db_path = "../data/sales_data.db"
        self.output_dir = "../visualizations/web_portfolio"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Web-optimized color scheme
        self.colors = {
            'primary': '#2E86C1',      # Professional blue
            'secondary': '#28B463',     # Success green  
            'accent': '#F39C12',        # Warning orange
            'danger': '#E74C3C',        # Alert red
            'purple': '#8E44AD',        # Purple
            'dark': '#2C3E50',          # Dark blue-gray
            'light': '#ECF0F1'          # Light gray
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
            print("✅ Data loaded successfully for web portfolio")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            
    def create_portfolio_thumbnail(self):
        """Create thumbnail image for portfolio grid (600x400px)"""
        print("Creating portfolio thumbnail...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor('white')
        
        # Title
        fig.suptitle('Sales Performance Analytics Dashboard\nSalomón Santiago Esquivel', 
                     fontsize=16, fontweight='bold', y=0.95, color=self.colors['dark'])
        
        # Chart 1: Revenue by Category
        revenue_data = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum(), include_groups=False
        ).sort_values(ascending=False)
        
        colors = [self.colors['accent'], self.colors['secondary'], 
                 self.colors['primary'], self.colors['danger']]
        
        bars1 = ax1.bar(revenue_data.index, revenue_data.values, 
                       color=colors[:len(revenue_data)], alpha=0.8)
        ax1.set_title('Revenue Potential by Category', fontsize=10, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45, labelsize=8)
        ax1.tick_params(axis='y', labelsize=8)
        
        # Chart 2: Customer Segmentation
        age_segments = self.users_df.groupby(
            pd.cut(self.users_df['age'], bins=[0, 25, 35, 50, 100], 
                   labels=['Gen Z', 'Millennials', 'Gen X', 'Boomers'])
        ).size()
        
        wedges, texts, autotexts = ax2.pie(age_segments.values, 
                                          labels=age_segments.index, 
                                          autopct='%1.0f%%',
                                          colors=colors[:len(age_segments)], 
                                          startangle=90)
        ax2.set_title('Customer Segmentation', fontsize=10, fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Chart 3: Top Customers
        customer_sales = self.carts_df.groupby('userId')['total'].sum().nlargest(10)
        
        ax3.bar(range(len(customer_sales)), customer_sales.values, 
               color=self.colors['secondary'], alpha=0.8)
        ax3.set_title('Top 10 Customers', fontsize=10, fontweight='bold')
        ax3.set_xlabel('Customer Rank', fontsize=8)
        ax3.tick_params(labelsize=8)
        
        # Chart 4: Key Metrics
        ax4.axis('off')
        
        metrics = [
            f"Total Revenue: ${self.carts_df['total'].sum():,.0f}",
            f"Customers: {len(self.users_df)}",
            f"Avg Order: ${self.carts_df['total'].mean():.0f}",
            f"Products: {len(self.products_df)}"
        ]
        
        for i, metric in enumerate(metrics):
            ax4.text(0.1, 0.8 - i*0.2, metric, fontsize=11, fontweight='bold',
                    color=self.colors['dark'], transform=ax4.transAxes)
        
        ax4.set_title('Key Metrics', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        
        # Save thumbnail
        thumbnail_path = f"{self.output_dir}/sales_performance_thumbnail.png"
        plt.savefig(thumbnail_path, dpi=150, bbox_inches='tight', 
                   facecolor='white', pad_inches=0.1)
        plt.close()
        
        print(f"✅ Thumbnail saved: {thumbnail_path}")
        return thumbnail_path
        
    def create_full_size_dashboard(self):
        """Create full-size dashboard for detailed viewing (1920x1080px)"""
        print("Creating full-size dashboard...")
        
        fig = plt.figure(figsize=(19.2, 10.8))  # 16:9 aspect ratio
        fig.patch.set_facecolor('white')
        
        # Custom grid layout
        gs = fig.add_gridspec(4, 6, 
                            height_ratios=[0.3, 1, 1, 0.8], 
                            width_ratios=[1, 1, 1, 1, 1, 1],
                            hspace=0.3, wspace=0.3,
                            top=0.93, bottom=0.07, left=0.05, right=0.95)
        
        # Main title
        fig.suptitle('Sales Performance Analytics Dashboard\nSalomón Santiago Esquivel - Data Analyst Portfolio', 
                     fontsize=24, fontweight='bold', y=0.97, color=self.colors['dark'])
        
        # KPI Row (Top)
        kpis = [
            ('Total Revenue', f'${self.carts_df["total"].sum():,.0f}', self.colors['primary']),
            ('Customers', f'{len(self.users_df)}', self.colors['secondary']),
            ('Orders', f'{len(self.carts_df)}', self.colors['accent']),
            ('Avg Order Value', f'${self.carts_df["total"].mean():.0f}', self.colors['danger'])
        ]
        
        for i, (title, value, color) in enumerate(kpis):
            if i < 4:  # Only show first 4 KPIs
                ax = fig.add_subplot(gs[0, i])
                
                # KPI card
                ax.add_patch(plt.Rectangle((0.1, 0.2), 0.8, 0.6, 
                                         facecolor=color, alpha=0.1, 
                                         edgecolor=color, linewidth=2))
                
                ax.text(0.5, 0.6, value, ha='center', va='center', 
                       fontsize=18, fontweight='bold', color=color)
                ax.text(0.5, 0.35, title, ha='center', va='center', 
                       fontsize=10, fontweight='bold', color=self.colors['dark'])
                
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis('off')
        
        # Chart 1: Revenue by Category (Large - spans 3 columns)
        ax1 = fig.add_subplot(gs[1, :3])
        
        revenue_data = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum(), include_groups=False
        ).sort_values(ascending=False)
        
        colors_list = [self.colors['accent'], self.colors['secondary'], 
                      self.colors['primary'], self.colors['danger']]
        
        bars1 = ax1.bar(revenue_data.index, revenue_data.values, 
                       color=colors_list[:len(revenue_data)], alpha=0.8, 
                       edgecolor='white', linewidth=2)
        
        ax1.set_title('Revenue Potential by Category', fontsize=16, fontweight='bold', 
                     pad=15, color=self.colors['dark'])
        ax1.set_ylabel('Revenue Potential ($)', fontsize=12)
        
        # Add value labels
        for bar, value in zip(bars1, revenue_data.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenue_data.values)*0.02,
                    f'${value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        ax1.grid(axis='y', alpha=0.3)
        ax1.set_facecolor('#fafafa')
        
        # Chart 2: Customer Age Distribution (Right side)
        ax2 = fig.add_subplot(gs[1, 3:])
        
        age_segments = self.users_df.groupby(
            pd.cut(self.users_df['age'], bins=[0, 25, 35, 50, 100], 
                   labels=['Gen Z\n(<25)', 'Millennials\n(25-35)', 'Gen X\n(36-50)', 'Boomers\n(50+)'])
        ).size()
        
        wedges, texts, autotexts = ax2.pie(age_segments.values, 
                                          labels=age_segments.index, 
                                          autopct='%1.1f%%',
                                          colors=colors_list[:len(age_segments)], 
                                          startangle=90, explode=[0.05]*len(age_segments))
        
        ax2.set_title('Customer Age Segmentation', fontsize=16, fontweight='bold', 
                     pad=15, color=self.colors['dark'])
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
        
        # Chart 3: Top Customers Performance (Bottom left)
        ax3 = fig.add_subplot(gs[2, :3])
        
        customer_sales = self.carts_df.groupby('userId')['total'].sum().nlargest(15)
        
        bars3 = ax3.bar(range(len(customer_sales)), customer_sales.values, 
                       color=self.colors['secondary'], alpha=0.8, 
                       edgecolor='white', linewidth=1)
        
        ax3.set_title('Top 15 Customers by Total Spending', fontsize=16, fontweight='bold', 
                     pad=15, color=self.colors['dark'])
        ax3.set_ylabel('Total Spent ($)', fontsize=12)
        ax3.set_xlabel('Customer Rank', fontsize=12)
        
        ax3.grid(axis='y', alpha=0.3)
        ax3.set_facecolor('#fafafa')
        
        # Chart 4: Product Ratings (Bottom right)
        ax4 = fig.add_subplot(gs[2, 3:])
        
        rating_data = self.products_df.groupby('category')['rating'].mean()
        
        bars4 = ax4.bar(rating_data.index, rating_data.values, 
                       color=colors_list[:len(rating_data)], alpha=0.8,
                       edgecolor='white', linewidth=2)
        
        ax4.set_title('Average Product Rating by Category', fontsize=16, fontweight='bold', 
                     pad=15, color=self.colors['dark'])
        ax4.set_ylabel('Average Rating', fontsize=12)
        ax4.set_ylim(0, 5)
        
        # Add value labels
        for bar, value in zip(bars4, rating_data.values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        ax4.grid(axis='y', alpha=0.3)
        ax4.set_facecolor('#fafafa')
        
        # Business Insights Panel (Bottom)
        ax5 = fig.add_subplot(gs[3, :])
        ax5.axis('off')
        
        # Create insights background
        ax5.add_patch(plt.Rectangle((0.02, 0.1), 0.96, 0.8, 
                                   facecolor=self.colors['light'], alpha=0.7, 
                                   edgecolor=self.colors['primary'], linewidth=2))
        
        insights_text = f"""
KEY BUSINESS INSIGHTS: • {revenue_data.index[0].title()} category leads with ${revenue_data.iloc[0]:,.0f} revenue potential • 
{len(age_segments)} customer segments with Millennials as primary target • Average customer age: {self.users_df['age'].mean():.0f} years • 
Top product rating: {self.products_df['rating'].max():.1f}/5.0 stars

STRATEGIC RECOMMENDATIONS: • Focus marketing budget on {revenue_data.index[0]} category • Develop retention programs for high-value customers • 
Optimize inventory for top-rated products • Target Millennial demographic for expansion
        """
        
        ax5.text(0.05, 0.5, insights_text.strip(), fontsize=12, 
                color=self.colors['dark'], transform=ax5.transAxes, 
                va='center', wrap=True)
        
        # Save full dashboard
        full_path = f"{self.output_dir}/sales_performance_full_dashboard.png"
        plt.savefig(full_path, dpi=200, bbox_inches='tight', 
                   facecolor='white', pad_inches=0.1)
        plt.close()
        
        print(f"✅ Full dashboard saved: {full_path}")
        return full_path
        
    def create_github_showcase_image(self):
        """Create perfect image for GitHub portfolio showcase"""
        print("Creating GitHub showcase image...")
        
        # Perfect size for GitHub display (1200x630 - optimal for social sharing)
        fig, ax = plt.subplots(1, 1, figsize=(12, 6.3))
        fig.patch.set_facecolor('white')
        
        # Create a showcase layout
        gs = fig.add_gridspec(2, 4, height_ratios=[0.3, 1], width_ratios=[1, 1, 1, 1],
                            hspace=0.15, wspace=0.15, 
                            top=0.95, bottom=0.1, left=0.05, right=0.95)
        
        # Title section
        ax_title = fig.add_subplot(gs[0, :])
        ax_title.axis('off')
        
        ax_title.text(0.5, 0.7, 'Sales Performance Analytics Dashboard', 
                     ha='center', va='center', fontsize=20, fontweight='bold',
                     color=self.colors['dark'], transform=ax_title.transAxes)
        ax_title.text(0.5, 0.3, 'End-to-End Data Pipeline | SQL Analytics | Python Visualization | Business Intelligence', 
                     ha='center', va='center', fontsize=12, 
                     color=self.colors['primary'], transform=ax_title.transAxes)
        
        # Mini Chart 1: Revenue
        ax1 = fig.add_subplot(gs[1, 0])
        revenue_data = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum(), include_groups=False
        ).sort_values(ascending=False)[:3]  # Top 3 only
        
        ax1.bar(range(len(revenue_data)), revenue_data.values, 
               color=[self.colors['accent'], self.colors['secondary'], self.colors['primary']])
        ax1.set_title('Revenue by Category', fontsize=10, fontweight='bold')
        ax1.set_xticks(range(len(revenue_data)))
        ax1.set_xticklabels([cat[:4] + '.' for cat in revenue_data.index], fontsize=8)
        ax1.tick_params(labelsize=8)
        
        # Mini Chart 2: Customer Segments
        ax2 = fig.add_subplot(gs[1, 1])
        age_segments = self.users_df.groupby(
            pd.cut(self.users_df['age'], bins=[0, 25, 35, 50, 100], 
                   labels=['<25', '25-35', '36-50', '50+'])
        ).size()
        
        ax2.pie(age_segments.values, labels=age_segments.index, autopct='%1.0f%%',
               colors=[self.colors['primary'], self.colors['secondary'], 
                      self.colors['accent'], self.colors['danger']])
        ax2.set_title('Age Segments', fontsize=10, fontweight='bold')
        
        # KPIs Panel
        ax3 = fig.add_subplot(gs[1, 2])
        ax3.axis('off')
        
        kpis_text = f"""KEY METRICS
        
💰 ${self.carts_df['total'].sum():,.0f}
Total Revenue

👥 {len(self.users_df)} Customers
{len(self.carts_df)} Orders

📊 ${self.carts_df['total'].mean():.0f}
Avg Order Value"""
        
        ax3.text(0.1, 0.9, kpis_text, fontsize=9, fontweight='bold',
                color=self.colors['dark'], transform=ax3.transAxes, va='top')
        
        # Technologies Panel
        ax4 = fig.add_subplot(gs[1, 3])
        ax4.axis('off')
        
        tech_text = """TECHNOLOGIES
        
🔧 Python | pandas
   SQLite | matplotlib

📈 SQL Analytics
   Window Functions

💼 Business Intelligence
   Customer Segmentation
   
🎯 Portfolio Project
   Interview Ready"""
        
        ax4.text(0.1, 0.9, tech_text, fontsize=9, fontweight='bold',
                color=self.colors['primary'], transform=ax4.transAxes, va='top')
        
        # Save showcase
        showcase_path = f"{self.output_dir}/sales_performance_github_showcase.png"
        plt.savefig(showcase_path, dpi=200, bbox_inches='tight', 
                   facecolor='white', pad_inches=0.05)
        plt.close()
        
        print(f"✅ GitHub showcase saved: {showcase_path}")
        return showcase_path
        
    def generate_all_web_images(self):
        """Generate all web-optimized images"""
        print("🚀 Starting Web Portfolio Dashboard Generation")
        print("=" * 60)
        
        try:
            results = {}
            
            # Generate all images
            results['thumbnail'] = self.create_portfolio_thumbnail()
            results['full_dashboard'] = self.create_full_size_dashboard()
            results['github_showcase'] = self.create_github_showcase_image()
            
            print("\n" + "=" * 60)
            print("✅ All web portfolio images created successfully!")
            print(f"\nOutput directory: {os.path.abspath(self.output_dir)}")
            print("\n📁 Files created:")
            print(f"   1. Thumbnail (600x400): sales_performance_thumbnail.png")
            print(f"   2. Full Dashboard (1920x1080): sales_performance_full_dashboard.png") 
            print(f"   3. GitHub Showcase (1200x630): sales_performance_github_showcase.png")
            
            print(f"\n📊 Business Metrics Analyzed:")
            print(f"   💰 Revenue: ${self.carts_df['total'].sum():,.0f}")
            print(f"   👥 Customers: {len(self.users_df)}")
            print(f"   📦 Products: {len(self.products_df)}")
            print(f"   🛒 Orders: {len(self.carts_df)}")
            
            print(f"\n🎯 Ready for GitHub portfolio update!")
            
            return results
            
        except Exception as e:
            print(f"❌ Error generating web images: {e}")
            return None
            
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()

def main():
    """Main execution"""
    dashboard = WebPortfolioDashboard()
    results = dashboard.generate_all_web_images()
    
    if results:
        print(f"\n🎉 Success! Your web portfolio images are ready!")
        print(f"\nNext steps:")
        print(f"1. Copy images to your portfolio repository")
        print(f"2. Update your index.html to use the new images")
        print(f"3. Commit and push to GitHub Pages")
    else:
        print(f"\n❌ Failed to generate images. Check the console for errors.")

if __name__ == "__main__":
    main()