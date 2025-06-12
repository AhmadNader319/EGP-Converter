import requests  # For sending HTTP requests to the CurrencyFreaks API

# =====================================================================
# ENVIRONMENT & DEPENDENCIES
# ---------------------------------------------------------------------
# Required Libraries:
#   - requests: For HTTP communication with the API
# Install via pip:
#   pip install requests
#
# API Credentials:
#   - Register at https://currencyfreaks.com/
#   - Obtain your API key from the dashboard after registration
# =====================================================================

base_url = "https://api.currencyfreaks.com/v2.0"

# =====================================================================
# PROJECT OBJECTIVES
# ---------------------------------------------------------------------
# [Idea#1 - Current Rates]
#   - Fetch and store the latest exchange rates (daily basis)

# [Idea#2 - Historical Rates]
#   - hist1: Store rates from the last 10 days
#   - hist2: Store rates for a user-specified date
#   - hist3: Store monthly rates from the last 12 months
#   - hist4: Store annual rates from the past 4 years
#   - hist5: Store rates for 30 consecutive days in a selected month

# [Idea#3 - Currency Conversion]
#   - Convert between currencies using either:
#     a) latest available rates
#     b) historical rates from storage
#   - User selects currency codes and optionally a date
# =====================================================================

# =====================================================================
# DATA SOURCES
# ---------------------------------------------------------------------
# DataSource#1: CurrencyFreaks API
#   - Source of real-time and historical exchange rates
#   - Used when requested data is not available in storage

# DataSource#2: IBM DB2 (Simulated ETL)
#   - Storage backend for historical exchange rates
#   - Stores key currencies: USD, EUR, EGP
# =====================================================================

# =====================================================================
# DATABASE SCHEMA (Destination)
# ---------------------------------------------------------------------
# Table Columns:
#   - date      : timestamp
#   - base      : varchar(3)        (base currency code)
#   - EGP_Rate  : numeric(1,6)      (Egyptian Pound)
#   - USD_Rate  : numeric(1,6)      (US Dollar)
#   - EUR_Rate  : numeric(1,6)      (Euro)
#   - DZD_Rate  : numeric(1,6)      (Algerian Dinar)
# =====================================================================

# =====================================================================
# API ENDPOINTS
# ---------------------------------------------------------------------
# Option 1: Latest Exchange Rates
#   https://api.exchangeratesapi.io/v1/latest?access_key=API_KEY
#
# Option 2: Historical Exchange Rates
#   https://api.exchangeratesapi.io/v1/YYYY-MM-DD?access_key=API_KEY&symbols=USD,CAD,EUR
# =====================================================================

# =====================================================================
# CURRENCY CONVERSION METHODS
# ---------------------------------------------------------------------
# Method 1: Use real-time exchange rates via API
# Method 2: Use stored exchange rates from database (historical)
# =====================================================================
