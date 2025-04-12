import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/Users/yibaozhang/Downloads/round-2-island-data-bottle/merged.csv", sep=';')

# Convert to proper datetime with correct timestamp handling
df['date'] = pd.to_datetime('2024-01-02') + pd.to_timedelta(df['day'], unit='D') + pd.to_timedelta(df['timestamp'] * (24*3600/1e6), unit='s')

# Group by product and calculate statistics
product_stats = df.groupby('product').agg({
    'mid_price': ['mean', 'std', 'min', 'max', 'count']
}).round(2)

# Create pivot table for correlation analysis
prices_pivot = df.pivot_table(index='date', columns='product', values='mid_price')

# Calculate correlation matrix
correlation_matrix = prices_pivot.corr()

# Plotting
# Get unique products and calculate subplot layout
products = df['product'].unique()
n_products = len(products)

# Create two separate figures: one for prices, one for correlation
# Price trends figure
fig_prices = plt.figure(figsize=(15, 3*((n_products+1)//2)))
for idx, product in enumerate(products, 1):
    ax = fig_prices.add_subplot((n_products+1)//2, 2, idx)
    product_data = df[df['product'] == product]
    ax.plot(product_data['date'], product_data['mid_price'])
    ax.set_title(f'{product} Price Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.setp(ax.get_xticklabels(), rotation=45)
    ax.grid(True)
    # Format date ticks
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d %H:%M'))
    ax.xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())

fig_prices.tight_layout()
plt.show()

# Correlation heatmap in a separate figure
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Price Correlation Matrix')
plt.tight_layout()
plt.show()

# Get CROISSANT data first
croissant_data = df[df['product']=='CROISSANT'].set_index('date')[['mid_price']]
croissant_data.columns = ['CROISSANT']

# Calculate spreads with proper timestamp alignment
products_to_compare = ['BASKET1', 'BASKET2', 'DJEMBES', 'JAM']
for product in products_to_compare:
    prod_data = df[df['product']==product].set_index('date')[['mid_price']]
    prod_data.columns = [product]
    croissant_data = croissant_data.join(prod_data)

spreads = {
    f'CROISSANT-{p}': croissant_data['CROISSANT'] - croissant_data[p]
    for p in products_to_compare
}

# Create spread plots with enhanced visualization
fig_spreads = plt.figure(figsize=(15, 10))
for idx, (spread_name, spread_values) in enumerate(spreads.items(), 1):
    ax = fig_spreads.add_subplot(2, 2, idx)
    ax.plot(spread_values.index, spread_values.values)
    ax.axhline(y=spread_values.mean(), color='r', linestyle='--', label='Mean')
    ax.axhline(y=spread_values.mean() + spread_values.std(), color='g', linestyle=':', label='+1 STD')
    ax.axhline(y=spread_values.mean() - spread_values.std(), color='g', linestyle=':', label='-1 STD')
    ax.set_title(f'Spread: {spread_name}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Spread Value')
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation=45)
    ax.grid(True)
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d %H:%M'))
    ax.xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())

fig_spreads.tight_layout()
plt.show()

# Enhanced spread statistics
spread_stats = pd.DataFrame({
    name: {
        'mean': values.mean(),
        'std': values.std(),
        'min': values.min(),
        'max': values.max(),
        'skew': values.skew(),
        'kurtosis': values.kurtosis(),
        'sharpe': values.mean() / values.std() if values.std() != 0 else 0
    }
    for name, values in spreads.items()
}).round(3)

print("\nProduct Statistics:")
print(product_stats)
print("\nCorrelation Matrix:")
print(correlation_matrix.round(3))
print("\nSpread Statistics:")
print(spread_stats)

