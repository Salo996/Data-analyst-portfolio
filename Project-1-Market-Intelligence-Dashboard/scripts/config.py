# API Configuration File
# Market Intelligence Dashboard - Salomón Santiago

"""
Configuration file for API keys and project settings.
Replace 'your_api_key_here' with actual API keys.
"""

# API Keys (Replace with your actual keys)
ALPHA_VANTAGE_API_KEY = 'Q7415GXZACN0TYUY'
NEWS_API_KEY = 'your_news_api_key_here'  # Optional

# Database Configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'market_intelligence',
    'user': 'your_username',
    'password': 'your_password'
}

# Target Companies for Analysis
TECH_COMPANIES = {
    # Lenovo Direct Competitors
    'LNVGY': 'Lenovo Group Limited',
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'HPQ': 'HP Inc.',
    'DELL': 'Dell Technologies Inc.',
    
    # Semiconductor & Components
    'IBM': 'International Business Machines',
    'INTC': 'Intel Corporation',
    'AMD': 'Advanced Micro Devices',
    'NVDA': 'NVIDIA Corporation',
    'QCOM': 'Qualcomm Incorporated',
    
    # Consumer Electronics
    'SONY': 'Sony Group Corporation',
    
    # Additional Tech Leaders
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'TSLA': 'Tesla Inc.',
    'META': 'Meta Platforms Inc.'
}

# Analysis Parameters
ANALYSIS_CONFIG = {
    'lookback_days': 90,        # Historical data period
    'update_frequency': 'daily', # Data refresh frequency
    'volatility_threshold': 0.05, # 5% price change threshold
    'volume_threshold': 1.5      # 150% of average volume
}

# File Paths
DATA_PATH = '../data/'
SQL_PATH = '../sql/'
DASHBOARD_PATH = '../dashboard/'

print("Configuration loaded successfully!")
print(f"Tracking {len(TECH_COMPANIES)} companies for market intelligence analysis.")