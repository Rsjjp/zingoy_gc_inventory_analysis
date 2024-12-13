# Zingoy.com Gift Card Inventory Analysis

**Overview**

This project focuses on analyzing and visualizing gift card data from Zingoy.com to gain insights into available gift cards, cashback percentages, and top-selling denominations. The analysis aims to support data-driven decisions for selecting value-for-money gift cards and identifying key trends in cashback rates as well Gift card stock status.

**Objectives**

* **Extract and Structure Data:** Fetch gift card inventory and details from Zingoy to create a structured dataset.
* **Store and Manage Data:** Utilize PostgreSQL for reliable storage and efficient querying of the data.
* **Visualize Insights:** Leverage Power BI to create an interactive dashboard with detailed visuals for exploring the data.

**Project Steps**

**1. Data Extraction**

The data was sourced directly from Zingoy.com to capture real-time insights about available gift cards and their cashback percentages. We used the Python `requests` library to scrape the gift card inventory. The extracted data was parsed into a structured format, capturing essential fields like:

* Gift card titles
* Cashback percentages
* Denomination details
* Links for direct access to the gift cards

**2. Data Storage and Management**

For efficient querying and long-term storage, we opted for PostgreSQL, a robust relational database. Using Python's `psycopg2` library, the extracted data was inserted into PostgreSQL tables. Queries were tested and optimized to ensure smooth integration with Power BI.

**3. Data Visualization**

Power BI was used to create an interactive dashboard visualizing trends and enabling users to explore the data dynamically:

* The PostgreSQL database was connected to Power BI using a direct query mode.
* Key measures and calculated columns were added using DAX (Data Analysis Expressions) to enhance the analysis.

**Key Visualizations:**

* Card visuals: Display total number of gift card brands and unique denominations.
* Bar chart: Show the distribution of top-selling denominations by cashback values.
* Pie chart: Highlight the top 5 gift cards with the highest cashback percentages.
* Table visual: Display detailed information about gift cards with clickable links.
* Slicer: Filter gift cards by cashback percentage dynamically.

**Key Insights**

* Total available gift card brands: 231
* Unique denominations: 68
* Top-selling denominations exhibit varying cashback percentages, with a significant concentration in the 0% to 10% range.
* The pie chart reveals the top 5 gift cards offering the highest cashback rates.
* The slicer allows users to filter and explore cashback percentages effectively.

**Tools and Technologies Used**

* Python: For data extraction and preprocessing (libraries like `requests` and `psycopg2`)
* PostgreSQL: For structured data storage and querying
* Power BI: For interactive visualization and dashboard creation
* DAX: For calculated measures and advanced data modeling within Power BI
