
def new_tax_regime(gross, variable):
    Basic_salary = 0.5 * (gross - variable)
    PF = 0.12 * Basic_salary

    # Tax slabs
    slab1 = 1200000
    slab2 = 1600000
    slab3 = 2000000
    slab4 = 2400000

    # Carryforward tax calculations
    carryforward1 = 0.15 * (slab2 - slab1) + 60000
    carryforward2 = 0.2 * (slab3 - slab2) + carryforward1
    carryforward3 = 0.25 * (slab4 - slab3) + carryforward2

    # Compute Gross Taxable Income
    Gross_taxable_income = gross - variable - 75000

    # Tax Calculation
    if Gross_taxable_income >= slab1:
        if Gross_taxable_income <= slab2:
            tax = 0.15 * (Gross_taxable_income - slab1)
        elif Gross_taxable_income <= slab3:
            tax = 0.2 * (Gross_taxable_income - slab2) + carryforward1
        elif Gross_taxable_income <= slab4:
            tax = 0.25 * (Gross_taxable_income - slab3) + carryforward2
        else:  # If Gross_taxable_income > slab4
            tax = 0.3 * (Gross_taxable_income - slab4) + carryforward3
    else:
        tax = 0

    return tax  # Fixed syntax


def calculate_hra_exemption(gross_salary, hra_received, rent_paid, is_metro):
    """
    Calculate HRA exemption based on Indian tax rules.

    Parameters:
    - gross_salary (float): The gross salary of the employee.
    - hra_received (float): The actual HRA received from the employer.
    - rent_paid (float): The actual rent paid by the employee.
    - is_metro (bool): True if the employee lives in a metro city, False otherwise.

    Returns:
    - dict: Contains the HRA exemption amount and taxable HRA.
    """

    # Assuming Basic Salary is 50% of Gross Salary
    basic_salary = 0.5 * gross_salary

    # Rule 1: Actual HRA received
    actual_hra = hra_received

    # Rule 2: Rent paid - 10% of Basic Salary
    rent_minus_10percent = rent_paid - (0.1 * basic_salary)

    # Rule 3: 50% of Basic Salary for Metro, 40% for Non-Metro
    city_percentage = 0.5 if is_metro else 0.4
    basic_salary_percentage = city_percentage * basic_salary

    # Minimum of the three rules is the exempted HRA
    hra_exemption = max(0, min(actual_hra, rent_minus_10percent, basic_salary_percentage))

    # Taxable HRA = HRA received - Exempted HRA
    taxable_hra = max(0, hra_received - hra_exemption)

    return hra_exemption




# Calculate HRA exemption


# Display Results



def old_tax_regime(gross, variable, section80c, home_loan, hra_received, rent_paid, nps):
    actual_gross= gross-variable
    basic_salary = int(0.5 * actual_gross)
    PF = int(0.12 * basic_salary)
    slab1 = 250000
    slab2 = 500000
    slab3 = 1000000

    hra_exemption = calculate_hra_exemption(gross_salary=gross, hra_received=hra_received, rent_paid=rent_paid, is_metro=True)

    #calculate taxable income
    NetTaxableIncome = actual_gross-PF-50000-section80c-home_loan-hra_exemption-nps

    if NetTaxableIncome >= slab2:
       if NetTaxableIncome <= slab3:
            tax= 0.20*(NetTaxableIncome-slab2) + 0.05*(slab2-slab1)
       else:
            tax= 0.3*(NetTaxableIncome-slab3) + 0.05*(slab2-slab1)
    else:
            tax=0
    return tax




