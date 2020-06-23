import argparse
import sys
from math import pow, log, ceil

parser = argparse.ArgumentParser()
parser.add_argument('--type', action="store", type=str)
parser.add_argument('--payment', action="store", type=float)
parser.add_argument('--principal', action="store", type=float)
parser.add_argument('--periods', action="store", type=int)
parser.add_argument('--interest', action="store", type=float)
arg_results = parser.parse_args()

# check for invalid parameter numbers/combinations as per spec.
if len(sys.argv) < 5:
    print("Incorrect parameters")
    exit()
elif arg_results.type is None or arg_results.interest is None:
    print("Incorrect parameters")
    exit()
elif arg_results.type != 'annuity' and arg_results.type != 'diff':
    print("Incorrect parameters")
    exit()
elif arg_results.type == 'diff' and arg_results.payment is not None:
    print("Incorrect parameters")
    exit()
elif arg_results.payment is not None and arg_results.payment < 0:
    print("Incorrect parameters")
    exit()
elif arg_results.principal is not None and arg_results.principal < 0:
    print("Incorrect parameters")
    exit()
elif arg_results.periods is not None and arg_results.periods < 0:
    print("Incorrect parameters")
    exit()
elif arg_results.interest is not None and arg_results.interest < 0:
    print("Incorrect parameters")
    exit()


def months():
    cp = arg_results.principal
    mp = arg_results.payment
    ir = arg_results.interest
    nir = (1/12) * (ir / 100)
    count_of_periods = ceil(log((mp / (mp - (nir * cp))), (1 + nir)))
    if count_of_periods < 12:
        print("You need {} months to repay this credit!".format(count_of_periods))
    elif count_of_periods == 12:
        print("You need 1 year to repay this credit!")
    elif count_of_periods < 24:
        print("You need {} year and {} months to repay this credit!".format
              (count_of_periods // 12, count_of_periods % 12))
    elif count_of_periods % 12 == 0:
        print("You need {} years to repay this credit!".format(count_of_periods // 12))
    else:
        print("You need {} years and {} months to repay this credit!".format(count_of_periods // 12,
                                                                             count_of_periods % 12))
    print("Overpayment = {}".format(ceil((mp * count_of_periods) - cp)))


def annuity():
    cp = arg_results.principal
    count_of_periods = arg_results.periods
    ir = arg_results.interest
    nir = (1/12) * (ir / 100)
    annuity_payment = cp * ((nir * pow((1 + nir), count_of_periods)) / (pow((1 + nir), count_of_periods) - 1))
    print("Your annuity payment = {}!".format(ceil(annuity_payment)))
    print("Overpayment = {}".format(ceil((ceil(annuity_payment) * count_of_periods) - cp)))


def principal():
    mp = arg_results.payment
    count_of_periods = arg_results.periods
    ir = arg_results.interest
    nir = (1 / 12) * (ir / 100)
    cp = mp / ((nir * pow((1 + nir), count_of_periods)) / (pow((1 + nir), count_of_periods) - 1))
    print("Your credit principal = {}!".format(int(cp)))
    print("Overpayment = {}".format(ceil((mp * count_of_periods) - cp)))


def calc_diff():
    p = arg_results.principal
    n = arg_results.periods
    i = (1 / 12) * (arg_results.interest / 100)
    total_payments = 0
    for m in range(1, n + 1):
        d1 = int(ceil((p / n) + (i * (p - (p * (m - 1) / n)))))
        total_payments += d1
        print("Month {}: paid out {}".format(m, d1))
    print()
    print("Overpayment = {}".format(int(total_payments - p)))


def calc_annuity():
    if arg_results.principal is None:
        principal()
    elif arg_results.payment is None:
        annuity()
    elif arg_results.periods is None:
        months()


if arg_results.type == 'diff':
    calc_diff()
else:
    calc_annuity()
