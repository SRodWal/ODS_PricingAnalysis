# ODS_PricingAnalysis
Hondura's national power grid pricing descriptions

Data source : https://www.ods.org.hn

-------------------- Current state ------------------------

1. Downloading data module: ✓  (scraptest.py)

  a. Inputs: website with the excel files.
  b. Outputs: Excel file in a desired directory.
  c. Past problems: Requites a website's headers -> Solution: Download the files through opera
  d. Possible Upgrades: Search for the monthly-pricing webpage.
    Comments: Webscraping
  
  
2. Reading files module: ✓ (getnames.py + pandas.read_excel(***) )

  a. Inputs: file's directory, file's type (e.j. .xlsx)
  b. outputs: Dataframes for each file.
  c. Past problem: Wont use the directory's path -> Solution: Read files in the scrip's directory.
  d. Possible Upgrades: Change of module of library, use paths propperly. 
  
3. Data Analysis: 
  a. Inputs: Dataframes
  b. Outputs: Graphs.
  Comments: Data sorting, categorization and vizualization.
