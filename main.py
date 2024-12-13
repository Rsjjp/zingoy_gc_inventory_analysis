from bs4 import BeautifulSoup
import requests
import pandas as pd
import psycopg2

# Database connection details
db_details = {
    "dbname": "Vouchersales",
    "user": "postgres",
    "password": "333725",
    "host": "localhost",
    "port": "5432"
}

current_page = 1
proceed = True
items = []

while proceed:
    url = "https://www.zingoy.com/gift-cards?page=" + str(current_page)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    # Check for "Oops! It seems there are no gift cards available"
    no_cards = soup.find("div", string="Oops! It seems there are no gift cards available")
    if no_cards:
        proceed = False
        break

    # Find all gift card containers
    all_gv = soup.find_all("div", class_="card-footer")

    for gc in all_gv:
        item = {}

        # Extract title
        title_tag = gc.find("div", class_="card-footer-title giftcard_name_length roboto-regular")
        if title_tag:
            item['Title'] = title_tag.text.strip()

        # Extract link
        link_tag = gc.find("a", class_="gc-ptrn dblock")
        if link_tag:
            item['Link'] = "https://www.zingoy.com" + link_tag['href']

        # Fetch additional details from the individual gift card page
        if 'Link' in item:
            gift_card_page = requests.get(item['Link'])
            gift_card_soup = BeautifulSoup(gift_card_page.text, "html.parser")

            # Cashback
            cashback_tag = gift_card_soup.find("div", class_="pt20 p5 grid-20 tablet-grid-10 roboto-medium csecondary f16 roboto-regular")
            if cashback_tag:
                item['Cashback'] = cashback_tag.text.strip()
            else:
                item['Cashback'] = "Not Any"

            # Gift Card Values (if multiple)
            value_tags = gift_card_soup.find_all("div", class_="pt20 pl20 grid-20 tablet-grid-15 roboto-medium 100-zingcash grid-parent f18 roboto-bold bold")  # Adjust selector as needed
            if value_tags:
                gift_card_values = [value.text.strip() for value in value_tags]
                item['Gift Card Values'] = ", ".join(gift_card_values)
            else:
                item['Gift Card Values'] = "Not Any"

        # Extract stock availability (Available Denomination)
        denomination = gc.find("div", class_="cl giftcard-count f13 roboto-regular")
        if denomination:
            item['Available Denomination'] = denomination.text.strip()

        # Append the item
        if item:
            items.append(item)
            print(item)

    current_page += 1
    if current_page == 22:  # Limit the number of pages for testing
        break

# Save the results to DataFrame
df = pd.DataFrame(items)

# Update existing data in PostgreSQL
try:
    conn = psycopg2.connect(**db_details)
    cursor = conn.cursor()

    # Create table if it doesn't exist (with unique title)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS gift_cards (
        id SERIAL PRIMARY KEY,
        title TEXT UNIQUE,
        link TEXT,
        cashback TEXT,
        gift_card_values TEXT,
        available_denomination TEXT
    );
    """
    cursor.execute(create_table_query)
    print("Table created or already exists.")

    # Update table with scraped data
    for _, row in df.iterrows():
        update_query = """
        INSERT INTO gift_cards (title, link, cashback, gift_card_values, available_denomination)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (title) 
        DO UPDATE 
        SET cashback = EXCLUDED.cashback,
            gift_card_values = EXCLUDED.gift_card_values,
            available_denomination = EXCLUDED.available_denomination;
        """
        cursor.execute(update_query, (
            row['Title'], 
            row['Link'], 
            row['Cashback'], 
            row['Gift Card Values'], 
            row['Available Denomination']
        ))
        print(f"Processed title: {row['Title']}")

    # Commit and close
    conn.commit()
    print("Data updated in PostgreSQL successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()