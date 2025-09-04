#!/usr/bin/env python3
"""
FINAL Clean Dashboard - Fixed Bottom Title Overlap
================================================

Final fixes:
- Much more space between middle and bottom charts
- Remove redundant bottom title text
- Perfect spacing for "Top 12 Customers" title visibility

Usage: python create_final_clean_dashboard.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np
import os

plt.style.use('default')

class FinalCleanDashboard:
    """Create the final clean dashboard with perfect spacing"""
    
    def __init__(self):
        self.db_path = "../data/sales_data.db"
        self.output_dir = "../visualizations/final_clean"
        
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
            print("Data loaded successfully for final clean dashboard")
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def create_final_clean_dashboard(self):
        """Create the final clean dashboard with perfect spacing and no redundant text"""
        print("Creating final clean dashboard...")
        
        # Even LARGER figure size for maximum spacing
        fig = plt.figure(figsize=(20, 15))  # Increased height from 14 to 15
        fig.patch.set_facecolor('white')
        
        # MAXIMUM spacing grid layout
        gs = fig.add_gridspec(3, 4, 
                            height_ratios=[0.25, 1.0, 1.0],  # Balanced middle/bottom
                            width_ratios=[1, 1, 1, 1],
                            hspace=0.6,   # MAXIMUM vertical space
                            wspace=0.3,   # Good horizontal space
                            top=0.90,     
                            bottom=0.10,  # Less bottom margin (no bottom text)
                            left=0.08,    
                            right=0.92)   
        
        # Clean, professional title (no bottom redundancy needed)
        fig.suptitle('Sales Performance Analytics Dashboard\nSalomón Santiago Esquivel', 
                     fontsize=18, fontweight='bold', y=0.95, color=self.colors['dark'])
        
        # Calculate all data
        revenue_data = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum(), include_groups=False
        ).sort_values(ascending=False)
        
        age_segments = self.users_df.groupby(
            pd.cut(self.users_df['age'], bins=[0, 25, 35, 50, 100], 
                   labels=['Gen Z\n(<25)', 'Millennials\n(25-35)', 'Gen X\n(36-50)', 'Boomers\n(50+)'])
        ).size()
        
        customer_sales = self.carts_df.groupby('userId')['total'].sum().nlargest(12)
        rating_data = self.products_df.groupby('category')['rating'].mean()
        
        colors_list = [self.colors['accent'], self.colors['secondary'], 
                      self.colors['primary'], self.colors['danger']]
        
        # KPI Cards Row (Top)
        kpis = [
            ('Total Revenue', f'${self.carts_df["total"].sum():,.0f}', self.colors['primary']),
            ('Total Customers', f'{len(self.users_df)}', self.colors['secondary']),
            ('Total Orders', f'{len(self.carts_df)}', self.colors['accent']),
            ('Avg Order Value', f'${self.carts_df["total"].mean():.0f}', self.colors['danger'])
        ]
        
        for i, (title, value, color) in enumerate(kpis):
            ax = fig.add_subplot(gs[0, i])
            
            ax.add_patch(plt.Rectangle((0.1, 0.2), 0.8, 0.6, 
                                     facecolor=color, alpha=0.1, 
                                     edgecolor=color, linewidth=2))
            
            ax.text(0.5, 0.65, value, ha='center', va='center', 
                   fontsize=16, fontweight='bold', color=color)
            ax.text(0.5, 0.35, title, ha='center', va='center', 
                   fontsize=10, fontweight='bold', color=self.colors['dark'])
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        # Chart 1: Revenue by Category (Middle Left)
        ax1 = fig.add_subplot(gs[1, :2])
        
        bars1 = ax1.bar(revenue_data.index, revenue_data.values, 
                       color=colors_list[:len(revenue_data)], 
                       alpha=0.8, edgecolor='white', linewidth=2)
        
        ax1.set_title('Revenue Potential by Category', fontsize=16, fontweight='bold', 
                     pad=25, color=self.colors['dark'])
        ax1.set_ylabel('Revenue Potential ($)', fontsize=12, color=self.colors['dark'])
        ax1.tick_params(axis='x', rotation=45, labelsize=11)
        ax1.tick_params(axis='y', labelsize=11)
        
        for bar, value in zip(bars1, revenue_data.values):
            ax1.text(bar.get_x() + bar.get_width()/2, 
                    bar.get_height() + max(revenue_data.values)*0.03,
                    f'${value:,.0f}', ha='center', va='bottom', 
                    fontweight='bold', fontsize=11)
        
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        ax1.set_facecolor('#fafafa')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # Chart 2: Customer Age Segmentation (Middle Right)
        ax2 = fig.add_subplot(gs[1, 2:])
        
        wedges, texts, autotexts = ax2.pie(
            age_segments.values, 
            labels=age_segments.index, 
            autopct='%1.1f%%',
            colors=colors_list[:len(age_segments)], 
            startangle=90, 
            explode=[0.12]*len(age_segments),
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )
        
        ax2.set_title('Customer Age Segmentation', fontsize=16, fontweight='bold', 
                     pad=25, color=self.colors['dark'])
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(12)
        
        # Chart 3: Top Customers (Bottom Left) - MAXIMUM spacing from above
        ax3 = fig.add_subplot(gs[2, :2])
        
        bars3 = ax3.bar(range(len(customer_sales)), customer_sales.values, 
                       color=self.colors['secondary'], alpha=0.8, 
                       edgecolor='white', linewidth=2)
        
        # MAXIMUM padding to clear revenue chart labels
        ax3.set_title('Top 12 Customers by Total Spending', 
                     fontsize=14, fontweight='bold', 
                     pad=40,  # MAXIMUM padding - was 30, now 40
                     color=self.colors['dark'])
        
        ax3.set_ylabel('Total Spent ($)', fontsize=12, color=self.colors['dark'])
        ax3.set_xlabel('Customer Rank', fontsize=12, color=self.colors['dark'])
        ax3.tick_params(labelsize=10)
        ax3.grid(axis='y', alpha=0.3, linestyle='--')
        ax3.set_facecolor('#fafafa')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        
        # Chart 4: Product Ratings (Bottom Right)
        ax4 = fig.add_subplot(gs[2, 2:])
        
        bars4 = ax4.bar(rating_data.index, rating_data.values, 
                       color=colors_list[:len(rating_data)], alpha=0.8,
                       edgecolor='white', linewidth=2)
        
        ax4.set_title('Average Product Rating by Category', fontsize=16, fontweight='bold', 
                     pad=25, color=self.colors['dark'])
        ax4.set_ylabel('Average Rating', fontsize=12, color=self.colors['dark'])
        ax4.set_ylim(0, 5)
        ax4.tick_params(axis='x', rotation=45, labelsize=11)
        ax4.tick_params(axis='y', labelsize=11)
        
        for bar, value in zip(bars4, rating_data.values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
                    f'{value:.2f}', ha='center', va='bottom', 
                    fontweight='bold', fontsize=11)
        
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
        ax4.set_facecolor('#fafafa')
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        
        # NO REDUNDANT BOTTOM TEXT - Clean finish
        
        # Save the final clean dashboard
        dashboard_path = f"{self.output_dir}/sales_performance_final_clean.png"
        plt.savefig(dashboard_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', pad_inches=0.3)
        plt.close()
        
        print(f"Final clean dashboard saved: {dashboard_path}")
        return dashboard_path
        
    def create_clean_thumbnail(self):
        """Create matching clean thumbnail"""
        print("Creating clean thumbnail...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 9))
        fig.patch.set_facecolor('white')
        
        # Clean title - no redundant text
        fig.suptitle('Sales Performance Analytics\nSalomón Santiago', 
                     fontsize=14, fontweight='bold', y=0.95, color=self.colors['dark'])
        
        # Data for thumbnail
        revenue_data = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum(), include_groups=False
        ).sort_values(ascending=False)
        
        age_segments = self.users_df.groupby(
            pd.cut(self.users_df['age'], bins=[0, 25, 35, 50, 100], 
                   labels=['<25', '25-35', '36-50', '50+'])
        ).size()
        
        customer_sales = self.carts_df.groupby('userId')['total'].sum().nlargest(8)
        
        colors = [self.colors['accent'], self.colors['secondary'], 
                 self.colors['primary'], self.colors['danger']]
        
        # Chart 1: Revenue
        bars1 = ax1.bar(revenue_data.index, revenue_data.values, 
                       color=colors[:len(revenue_data)], alpha=0.8)
        ax1.set_title('Revenue by Category', fontsize=11, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45, labelsize=9)
        
        # Chart 2: Age segments - Clean pie
        wedges, texts, autotexts = ax2.pie(
            age_segments.values, labels=age_segments.index, autopct='%1.0f%%',
            colors=colors[:len(age_segments)], explode=[0.08]*len(age_segments),
            textprops={'fontsize': 9}
        )
        ax2.set_title('Customer Segments', fontsize=11, fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Chart 3: Top customers
        ax3.bar(range(len(customer_sales)), customer_sales.values, 
               color=self.colors['secondary'], alpha=0.8)
        ax3.set_title('Top Customers', fontsize=11, fontweight='bold')
        ax3.set_xlabel('Customer Rank', fontsize=9)
        ax3.tick_params(labelsize=9)
        
        # Chart 4: Key metrics (clean, no redundant text)
        ax4.axis('off')
        metrics_text = f"""KEY METRICS

Revenue: ${self.carts_df['total'].sum():,.0f}
Customers: {len(self.users_df)}
Orders: {len(self.carts_df)}
Avg Order: ${self.carts_df['total'].mean():.0f}

Professional Business
Intelligence Analysis"""
        
        ax4.text(0.1, 0.9, metrics_text, fontsize=10, fontweight='bold',
                color=self.colors['dark'], transform=ax4.transAxes, va='top')
        
        plt.tight_layout()
        
        # Save clean thumbnail
        thumb_path = f"{self.output_dir}/sales_performance_final_clean_thumbnail.png"
        plt.savefig(thumb_path, dpi=200, bbox_inches='tight', 
                   facecolor='white', pad_inches=0.2)
        plt.close()
        
        print(f"Clean thumbnail saved: {thumb_path}")
        return thumb_path
        
    def generate_final_clean_suite(self):
        """Generate the final clean dashboard suite"""
        print("Creating FINAL CLEAN Dashboard Suite")
        print("=" * 60)
        
        try:
            results = {}
            
            results['main_dashboard'] = self.create_final_clean_dashboard()
            results['thumbnail'] = self.create_clean_thumbnail()
            
            print("\n" + "=" * 60)
            print("SUCCESS: Final clean dashboard suite complete!")
            print(f"\nFINAL FIXES APPLIED:")
            print(f"- MAXIMUM vertical spacing (hspace=0.6)")
            print(f"- Bottom title padding increased to 40")
            print(f"- Removed redundant bottom text")
            print(f"- Clean, professional finish")
            
            return results
            
        except Exception as e:
            print(f"Error: {e}")
            return None
            
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()

def main():
    dashboard = FinalCleanDashboard()
    results = dashboard.generate_final_clean_suite()
    
    if results:
        print(f"\nPERFECT: Final clean dashboard ready for upload!")

if __name__ == "__main__":
    main()