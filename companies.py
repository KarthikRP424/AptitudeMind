# ============================================================
# AptitudeMind - Company System
# ============================================================


# ------------------------------------------------------------
# Companies
# ------------------------------------------------------------

COMPANIES = {

    "TCS": {
        "name": "TCS",
        "category": "IT Services"
    },

    "Infosys": {
        "name": "Infosys",
        "category": "IT Services"
    },

    "Wipro": {
        "name": "Wipro",
        "category": "IT Services"
    },

    "Accenture": {
        "name": "Accenture",
        "category": "IT Services"
    },

    "Cognizant": {
        "name": "Cognizant",
        "category": "IT Services"
    },

    "Capgemini": {
        "name": "Capgemini",
        "category": "IT Services"
    },

    "Deloitte": {
        "name": "Deloitte",
        "category": "Consulting"
    },

    "IBM": {
        "name": "IBM",
        "category": "Technology"
    },

    "HCL": {
        "name": "HCL",
        "category": "IT Services"
    },

    "Tech Mahindra": {
        "name": "Tech Mahindra",
        "category": "IT Services"
    },

    "Amazon": {
        "name": "Amazon",
        "category": "Product Company"
    },

    "Microsoft": {
        "name": "Microsoft",
        "category": "Product Company"
    },

    "Google": {
        "name": "Google",
        "category": "Product Company"
    },

    "Goldman Sachs": {
        "name": "Goldman Sachs",
        "category": "Finance / Technology"
    },

    "JPMorgan Chase": {
        "name": "JPMorgan Chase",
        "category": "Finance / Technology"
    },

    "Oracle": {
        "name": "Oracle",
        "category": "Technology"
    },

    "Cisco": {
        "name": "Cisco",
        "category": "Technology"
    },

    "Walmart": {
        "name": "Walmart",
        "category": "Retail / Technology"
    }
}


# ------------------------------------------------------------
# Get All Companies
# ------------------------------------------------------------

def get_companies():
    """
    Return all available company names.
    """

    return list(COMPANIES.keys())


# ------------------------------------------------------------
# Check Whether a Company Exists
# ------------------------------------------------------------

def is_valid_company(company):
    """
    Check whether the company exists in the system.
    """

    return company in COMPANIES


# ------------------------------------------------------------
# Get Company Information
# ------------------------------------------------------------

def get_company_info(company):
    """
    Return information about a company.
    """

    return COMPANIES.get(company)


# ------------------------------------------------------------
# Search Companies
# ------------------------------------------------------------

def search_companies(keyword):
    """
    Search companies by name.

    Example:
        search_companies("ama")
        -> ["Amazon"]
    """

    keyword = keyword.lower().strip()

    results = []

    for company in COMPANIES:

        if keyword in company.lower():

            results.append(company)

    return results