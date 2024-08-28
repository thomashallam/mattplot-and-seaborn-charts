import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


output_dir = './output'

# Sample data
data = {
    'Date': ['2022-12-01', '2024-03-03', '2024-04-02', '2024-06-02', '2024-09-02','2025-10-03', ],
    'Project': ['Project Name', 'Project Name2','Project Name4', 'Project Name','Project Name2', 'Project Name3'],
    'Number1': [22, 22, 23, 14, 13, 15],
    'Number2': [44, 1, 22, 44, 13, 16]
}

# Create a DataFrame
df = pd.DataFrame(data)
print(df.head(5))

# Quarterly aggregation using matplotlib

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Calculate Totals
df['Total'] = df['Number1'] + df['Number2']

# Extract Year-Quarter
df['Year-Quarter'] = df['Date'].dt.year.astype(str) + '-Q' + df['Date'].dt.quarter.astype(str)
# df['Year-Quarter'] = df['Date'].dt.to_period('Q')

# Generate a complete list of Year-Quarter periods
all_periods = pd.period_range(start=df['Date'].min(), end=df['Date'].max(), freq='Q').strftime('%Y-Q%q')

# Ensure all combinations of Year-Quarter and Project are present
df = df.set_index(['Year-Quarter', 'Project']).reindex(
    pd.MultiIndex.from_product([all_periods, df['Project'].unique()], names=['Year-Quarter', 'Project']),
    fill_value=0
).reset_index()

# Group by Project and Year-Quarter, then sum the totals
grouped = df.groupby(['Year-Quarter','Project'])['Total'].sum().unstack()

# Define a custom color palette
# colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Example colors for each project

# Define a color map
#cmap = plt.get_cmap('tab10')  # Choose a color map

# Define a custom color palette
palette = sns.color_palette("Paired", n_colors=len(grouped.columns))  # Use a palette with a number of colors

# Set figure size to 1280x800 pixels (16x10 inches with 80 dpi)
fig, ax = plt.subplots(figsize=(16, 10), dpi=80)

# Plotting the stacked bar chart with seaborn colour pallete (use colormap for cmap)
grouped.plot(kind='bar', stacked=True, ax=ax, color=palette)

# Calculate and plot total value at the top of each bar
totals = grouped.sum(axis=1)
for i, total in enumerate(totals):
    if total > 0:  # Only add text if total is greater than 0
        ax.text(i, total, str(total), ha='center', va='bottom', fontsize=12, color='black')
        
# Add labels and title
plt.title('Project Totals by Quarter', fontsize=16)
plt.ylabel('Total',fontsize=14)
plt.xlabel('Quarters',fontsize=14)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(title='Project',fontsize=14,title_fontsize='13')
# Remove the black border
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig(f'{output_dir}/total_by_year_quarter.png', format='png', bbox_inches='tight', pad_inches=0.1)

# Show plot
plt.tight_layout()
plt.show()

