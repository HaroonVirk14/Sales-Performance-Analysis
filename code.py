import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'C:/Users/Haroon Virk/Downloads/archive/amazon.csv'
amazon_data = pd.read_csv(file_path)

# Function to convert price from string to float
def convert_price(price):
    return float(price.replace('₹', '').replace(',', '').strip())



# Apply the conversion function to price columns
amazon_data['discounted_price'] = amazon_data['discounted_price'].apply(convert_price)
amazon_data['actual_price'] = amazon_data['actual_price'].apply(convert_price)



# Convert discount percentage to float
amazon_data['discount_percentage'] = amazon_data['discount_percentage'].str.rstrip('%').astype('float')



# Extract the first category as the main category
amazon_data['main_category'] = amazon_data['category'].str.split('|').str[0]



# Convert rating to float, handling non-numeric values
def convert_rating(rating):
    try:
        return float(rating)
    except ValueError:
        return None

amazon_data['rating'] = amazon_data['rating'].apply(convert_rating)



# Drop rows with invalid or missing ratings
amazon_data = amazon_data.dropna(subset=['rating'])



# Price Analysis
average_discounted_price = amazon_data['discounted_price'].mean()
median_discounted_price = amazon_data['discounted_price'].median()
range_discounted_price = amazon_data['discounted_price'].max() - amazon_data['discounted_price'].min()

average_actual_price = amazon_data['actual_price'].mean()
median_actual_price = amazon_data['actual_price'].median()
range_actual_price = amazon_data['actual_price'].max() - amazon_data['actual_price'].min()



# Identify products with the highest and lowest discounts
amazon_data['discount_amount'] = amazon_data['actual_price'] - amazon_data['discounted_price']
highest_discount_product = amazon_data.loc[amazon_data['discount_amount'].idxmax()]
lowest_discount_product = amazon_data.loc[amazon_data['discount_amount'].idxmin()]



price_summary = {
    'Average Discounted Price': average_discounted_price,
    'Median Discounted Price': median_discounted_price,
    'Range Discounted Price': range_discounted_price,
    'Average Actual Price': average_actual_price,
    'Median Actual Price': median_actual_price,
    'Range Actual Price': range_actual_price,
    'Highest Discount Product': highest_discount_product,
    'Lowest Discount Product': lowest_discount_product
}




print("Price Analysis Summary:")
for key, value in price_summary.items():
    print(f"{key}: {value}")



# Rating Analysis
plt.figure(figsize=(10, 6))
sns.histplot(amazon_data['rating'], bins=20, kde=True)
plt.title('Distribution of Product Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()




average_rating_by_category = amazon_data.groupby('main_category')['rating'].mean()
print("\nAverage Rating by Category:")
print(average_rating_by_category)




# Category Analysis
category_sales_summary = amazon_data.groupby('main_category').agg({
    'discounted_price': ['mean', 'sum', 'count'],
    'rating': 'mean'
}).reset_index()
category_sales_summary.columns = ['Category', 'Average Discounted Price', 'Total Discounted Price', 'Number of Products', 'Average Rating']

print("\nCategory Sales Summary:")
print(category_sales_summary)



# Discount Analysis
plt.figure(figsize=(10, 6))
sns.scatterplot(data=amazon_data, x='discount_percentage', y='rating')
plt.title('Correlation between Discount Percentage and Rating')
plt.xlabel('Discount Percentage')
plt.ylabel('Rating')
plt.grid(True)
plt.show()




# Correlation analysis
discount_rating_correlation = amazon_data[['discount_percentage', 'rating']].corr().iloc[0, 1]
print(f"\nCorrelation between Discount Percentage and Rating: {discount_rating_correlation}")



# Determine the optimal discount range
optimal_discount_range = amazon_data.groupby(pd.cut(amazon_data['discount_percentage'], bins=[0, 20, 40, 60, 80, 100]))['rating'].mean()
print("\nOptimal Discount Range:")
print(optimal_discount_range)
