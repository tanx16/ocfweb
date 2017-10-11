from ocflib.lab.stats import current_semester_start
from ocfweb.stats.printing import _pages_printed_data
from ocfweb.stats.accounts import _get_account_stats
from  django.shortcuts import render

def stats_money(request):
    return render(
        request,
        'stats/money_saved.html',
        {
            'title': 'Savings Statistics',
            'start_date': current_semester_start,
            'print_data': _pages_printed_data(),
            'account_data': _get_account_stats(),
        },
    )
