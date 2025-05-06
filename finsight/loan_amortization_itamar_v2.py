"""
- Confidential -
© FINSIGHT Group Inc.

-------------------------------------------------------------------------------------
Finance understanding and coding assignment - Loan Amortization (פירוט תשלומי הלוואה)
-------------------------------------------------------------------------------------

The code below create the payment details of a loan over monthly periods ("Loan Amortization").
The users of the loan_amortization function are the lenders (usually a bank), who wants to run a report of the
payments they will get from loans over time.

The main inputs of a loan are:
- total_periods: loan's time length, in months.
- yearly_interest_rate: the loan's interest rate, in %.
- monthly_payment: the amount, in $, the borrower of the loan needs to pay every month for the loan.

As an example, when you run run_loan_amortization_example1 below, the code will run
  amortization of 60 periods (5 years) loan, with yearly interest rate of 12% and monthly payments of $22500.

loan_amortization function will print the borrower's payments and the remaining of the loan's balance.
When you run run_loan_amortization_example1 below, you will get a print of:
payment dates = ['2012-01-01', '2013-02-01', '2013-03-01', '2013-04-01', '2012-05-01', ...]
balance = [1000000.0, 987500.0, 974875.0, 962123.75, 949244.9875 ...]
interest paid = [0.0, 10000.0, 9875.0, 9748.75, 9621.2375, ...]
principal paid = [0.0, 12500.0, 12625.0, 12751.25, 12878.7625, ...]

- balance ("יתרת הקרן"): The amount of $ the borrower owns the lender.
- principal paid ("תשלומי קרן"): Amounts the borrower pays, to return the balance to the lender.
- interest paid ("תשלומי ריבית"): Interest amount the borrower pays for taking the loan,
                                  as % of the reminder of the balance of the loan.
                                  Unlike principal payments, interest payments do not reduce the balance.

Note 1: The first values of each output('2012-01-01', 1000000.0, 0.0, 0.0), are for the initial state of the loan,
  before the loan, before the borrower starts to pay the loan back to the lender.


Please read the code of loan_amortization function below, and make sure you understand it before making changes.
In this assignment, you will need to adapt the code to support new features, to support more complex types of loans.
You can freely create data structures for inputs and outputs.
You can change the inputs and output to support the new feature.
You can assume the inputs are already have been validated, no need to validate it.
You can divide the code into functions, classes and files as you see fit.
There is no need to document your code in this assignment, but make functions/classes/files names easily understandable.


The new features needed to be implemented in this assignment:
-------------------------------------------------------------

=====================
"Interest Frequency"
=====================
Instead of paying interest every 1 month (Monthly), some loans are paid interest only
  every 3 (Quarterly) / 6 (Semi-annually) / 12 (Annually) months.
- A quarterly interest ("ריבית רבעונית") loan will pay interest only every 3 periods, on periods 3,6,9,12,15..,60
- A semi-annually interest ("ריבית חצי-שנתית") loan will pay interest only every 6 periods, on periods 6,12,18..,60
- An annually interest ("ריבית שנתית") loan will pay interest only every 12 periods, on periods 12,24,36,48,60

Note 2: Take into account that different periods between interest payment, have different balance,
  and therefore, accrue different amount of interest each month.
Note 3: The principal paid each month is still calculated in the same way. e.g. in a quarterly interest loan,
  in periods 1,2,4,5,7,8, etc.. the principal paid will be equal to monthly_payment, as there is no interest
  payment in those periods.

Add interest_frequency variable as an input for the loan, decide on its type and values for each frequency.
Adapt the code to support "Interest Frequency".


============
"Prepayment"
============
The user (the lender) wants to add "prepayment assumption" to the amortization, to simulate the change in loan payments
  if the borrower want to prepay some of the loan ("פרעון מוקדם חלקי").
The user will provide a prepayment_rate assumption, as a decimal number (e.g. 0.02 for 2% prepayment each month).
Each period, in addition to the regular "scheduled" principal paid (which derived from monthly_payment),
  an additional "prepayment" principal is paid:
- "prepayment" principal paid[period_i] = balance[period_i] * prepayment_rate
- balance[period_i] is the balance AFTER the regular "scheduled" principal is deduced from the balance
- "prepayment" principal paid[period_i] should be deducted from the loan's balance by that amount (the borrower
  returned more $ to the lender then required, so it will pay the loan faster and with less interest over time).

As the lender needs to keep track of prepayments separately, split principal_paid into scheduled_principal and
prepayment_principal. Optionally, keep principal_paid=scheduled_principal+prepayment_principal as one of the outputs.

=====================
"Prepayment Interest"
=====================
In case the loan is paying interest Quarterly/Semi-Annually/Annual (see "Interest Frequency" above),
  and the loan have non-zero prepayment_rate (see "Prepayment" above),
  we also need to calculate the interest that the amount of prepayment_principal had accrued, but not paid yet.
The prepayment_interest needs to be paid for the prepayment_principal amount AT THAT period, INSTEAD of
  being paid at the next interest paid.

As the lender needs to keep track of prepayments separately, split interest_paid into scheduled_interest and
prepayment_interest. Optionally, keep interest_paid=scheduled_interest+prepayment_interest as one of the outputs.

Note 4: obviously, for monthly interest loans, prepayment_interest is always 0.
Note 5: similarly, for quarterly interest loans, prepayment_interest is 0 for periods 3,6,9,12,15..60,
  prepayment_interest > 0 on periods 1,2,4,5... if prepayment_rate > 0 and yearly_interest_rate > 0
  and there is still balance in those periods (to be partly paid as prepayment_principal).


==================
"Loan Aggregation"
==================
The lender have a portfolio of many loans. The loan amortization should support running amortization
  for multiple loans.
- The output should include the total of [balance, scheduled_principal, prepayment_principal,
    scheduled_interest, prepayment_interest] aggregated from all the loans given.
- The input should support multiple loans.
- Each loan have its own [initial_balance, total_periods, yearly_interest_rate, monthly_payment, interest_frequency].
- prepayment_rate and payment_timeline are shared between loans, and given for the whole loans' portfolio.
- payment_timeline is long enough to be used by all those loans, the output's length should be at the same length
    as payment_timeline. Take into account that some loans are shorter than payment_timeline and of other loans.
- Running complexity should be O(total_periods * number of loans * number of fields in the output).
  Initial loan_amortization is already running at that complexity. No need to optimize runtime in this assignment.
"""

from datetime import date
from dataclasses import dataclass

def loan_amortization(
    initial_balance: float,
    total_periods: int,
    yearly_interest_rate: float,
    monthly_payment: float,
    payment_timeline: list[date],
    interest_frequency: int = 1,
    prepayment_rate: float = 0.0,
):
    size = total_periods + 1  # period 0 is the initial state, periods 1,2...total_periods are payment periods.
    # outputs:
    balance = [0.0] * size
    balance[0] = initial_balance

    scheduled_principal_paid = [0.0] * size
    prepayment_principal_paid = [0.0] * size

    scheduled_interest_paid = [0.0] * size
    prepayment_interest_paid = [0.0] * size

    total_paid = [0.0] * size
    accrued_interest = 0.0

    # loan amortization, for periods 1 to total_periods
    for period_i in range(1, total_periods + 1):
        # calculate interest for 30 days of interest per month (of 360 a year), using the yearly rate
        monthly_interest = balance[period_i - 1] * (yearly_interest_rate / 100.0) * 30 / 360
        accrued_interest += monthly_interest if monthly_interest > 0 else 0

        if period_i % interest_frequency == 0:
            scheduled_interest_paid[period_i] = accrued_interest
            accrued_interest = 0.0

        scheduled_principal_paid[period_i] = monthly_payment - scheduled_interest_paid[period_i]

        # if this is the last period of the loan, pay all remaining balance
        if period_i == total_periods:
            scheduled_principal_paid[period_i] = max(0.0, balance[period_i - 1])

        remaining_balance = balance[period_i - 1] - scheduled_principal_paid[period_i]

        prepayment_principal_paid[period_i] = max(0.0, remaining_balance * prepayment_rate)
        balance[period_i] = remaining_balance - prepayment_principal_paid[period_i]

        if (interest_frequency > 1 and  # not monthly interest
            prepayment_principal_paid[period_i] > 0 and   # prepayment_principal_paid > 0
            period_i % interest_frequency != 0 and     # not interest payment period
            yearly_interest_rate > 0      # yearly_interest_rate > 0
        ):
            prepayment_interest_paid[period_i] = prepayment_principal_paid[period_i] * (
                        yearly_interest_rate / 100.0) * 30 / 360 * (period_i % interest_frequency)

            scheduled_interest_paid[period_i] = max(0, scheduled_interest_paid[period_i] - prepayment_interest_paid[period_i])

            balance[period_i] += prepayment_interest_paid[period_i]

        total_paid[period_i] = (scheduled_principal_paid[period_i] + prepayment_principal_paid[period_i] +
                                scheduled_interest_paid[period_i] + prepayment_interest_paid[period_i])

    # print output:
    print("payment dates = " + str(list(d.strftime("%Y-%m-%d") for d in payment_timeline)))
    print("balance = " + str(balance))
    print("scheduled interest paid = " + str(scheduled_interest_paid))
    print("prepayment interest paid = " + str(prepayment_interest_paid))
    print("scheduled principal paid = " + str(scheduled_principal_paid))
    print("prepayment principal paid = " + str(prepayment_principal_paid))
    print(f"total paid = {total_paid}")
    return balance, scheduled_principal_paid, prepayment_principal_paid, scheduled_interest_paid, prepayment_interest_paid


@dataclass
class LoanData:
    initial_balance: float
    total_periods: int
    yearly_interest_rate: float
    monthly_payment: float
    interest_frequency: int
    prepayment_rate: float

def portfolio_loan_amortization(
        loans: list[LoanData],
        payment_timeline: list[date],
):
    total_balance = [0.0] * len(payment_timeline)
    total_scheduled_principal_paid = [0.0] * len(payment_timeline)
    total_prepayment_principal_paid = [0.0] * len(payment_timeline)
    total_scheduled_interest_paid = [0.0] * len(payment_timeline)
    total_prepayment_interest_paid = [0.0] * len(payment_timeline)

    for loan in loans:
        balance, scheduled_principal_paid, prepayment_principal_paid, scheduled_interest_paid, prepayment_interest_paid = loan_amortization(
            loan.initial_balance,
            loan.total_periods,
            loan.yearly_interest_rate,
            loan.monthly_payment,
            payment_timeline,
            loan.interest_frequency,
            loan.prepayment_rate,
        )

        # aggregate the outputs of all loans
        for i in range(len(payment_timeline) -1):
            try:
                total_balance[i] += balance[i+1]
                total_scheduled_principal_paid[i] += scheduled_principal_paid[i]
                total_prepayment_principal_paid[i] += prepayment_principal_paid[i]
                total_scheduled_interest_paid[i] += scheduled_interest_paid[i]
                total_prepayment_interest_paid[i] += prepayment_interest_paid[i]
            except IndexError:
                pass
    print(f'total_balance = {total_balance}')
    print(f'total_scheduled_principal_paid = {total_scheduled_principal_paid}')
    print(f'total_prepayment_principal_paid = {total_prepayment_principal_paid}')
    print(f'total_scheduled_interest_paid = {total_scheduled_interest_paid}')
    print(f'total_prepayment_interest_paid = {total_prepayment_interest_paid}')


def get_timeline(initial_date: date, periods: int) -> list[date]:
    """:return: list of loan dates starting from initial date"""
    # no need to understand/change this function
    timeline: list[date] = []
    day = initial_date.day
    mm = initial_date.month
    yyyy = initial_date.year
    for i in range(periods + 1):
        month = (mm + i - 1) % 12 + 1
        year = (yyyy * 12 + i - 1) // 12 + 1
        timeline.append(date(year, month, day))
    return timeline


def run_loan_amortization_example1():
    loan_amortization(1000000.0, 60, 12.0, 22500.0,
                      get_timeline(date(2012, 1, 1), 60))

def run_loan_amortization_example2():
    loan_amortization(
        1000000.0, 60, 12.0, 22500.0,
        get_timeline(date(2012, 1, 1), 60),
        interest_frequency=3,
    )

def run_loan_amortization_example3():
    loan_amortization(
        1000000.0, 60, 12.0, 22500.0,
        get_timeline(date(2012, 1, 1), 60),
        interest_frequency=3,
        prepayment_rate=0.02,
    )

def run_loan_amortization_example4():
    loan_amortization(
        10000.0, 12, 10.0, 900.0,
        get_timeline(date(2012, 1, 1), 60),
        interest_frequency=3,
        prepayment_rate=0.02,
    )

def run_portfolio_loan_amortization_example1():
    portfolio_loan_amortization(
        [
            LoanData(initial_balance=1000000.0, total_periods=60, yearly_interest_rate=12.0, monthly_payment=22500.0, interest_frequency=3, prepayment_rate=0.02),
            LoanData(10000.0, 12, 10.0, 900.0, 3, 0.02),
        ],
        get_timeline(date(2012, 1, 1), 60),
    )


# run_portfolio_loan_amortization_example1()
# run_loan_amortization_example1()
# run_loan_amortization_example2()
run_loan_amortization_example3()
# run_loan_amortization_example4()


#  © FINSIGHT Group Inc.
# - Confidential -