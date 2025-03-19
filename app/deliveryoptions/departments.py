"""
Departments module for the Django app.
Contains mapping of department reference codes to their names and URLs.
"""

# Dictionary mapping department reference codes to department names and URLs
# Used to determine which department is responsible for a record
# and to provide contact information for Freedom of Information requests
DEPARTMENT_DETAILS = {
    "AB": {
        "deptname": "Nuclear Decommissioning Authority",
        "depturl": "https://www.gov.uk/government/organisations/nuclear-decommissioning-authority",
    },
    "ADM": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    "AIR": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    "CAB": {
        "deptname": "Cabinet Office",
        "depturl": "http://www.cabinetoffice.gov.uk/content/freedom-information-foi",
    },
    "CO": {
        "deptname": "Foreign and Commonwealth Office",
        "depturl": "http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/",
    },
    "COAL": {
        "deptname": "Department for Business, Energy and Industrial Strategy",
        "depturl": "https://www.gov.uk/government/organisations/department-for-business-energy-and-industrial-strategy",
    },
    "DEFE": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    "DO": {
        "deptname": "Foreign and Commonwealth Office",
        "depturl": "http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/",
    },
    "ES": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    "FCO": {
        "deptname": "Foreign and Commonwealth Office",
        "depturl": "http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/",
    },
    "FO": {
        "deptname": "Foreign and Commonwealth Office",
        "depturl": "http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/",
    },
    "PREM": {
        "deptname": "Cabinet Office",
        "depturl": "http://www.cabinetoffice.gov.uk/content/freedom-information-foi",
    },
    "T 352": {
        "deptname": "Cabinet Office",
        "depturl": "http://www.cabinetoffice.gov.uk/content/freedom-information-foi",
    },
    "WO": {
        "deptname": "Ministry of Defence",
        "depturl": "https://www.gov.uk/government/organisations/ministry-of-defence",
    },
    # Note: Additional departments can be added to this dictionary as needed
}