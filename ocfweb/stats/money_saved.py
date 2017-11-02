from ocflib.lab.stats import current_semester_start
from ocfweb.stats.printing import _pages_printed_data
from ocfweb.stats.accounts import _get_account_stats
from  django.shortcuts import render
from ocflib.printing.printers import PRINTERS
from ocflib.printing.quota import get_connection
from ocflib.vhost import web

def stats_money(request):
    return render(
        request,
        'stats/money_saved.html',
        {
            'title': 'Savings Statistics',
            'start_date': current_semester_start,
            'print_data': _stats_printing(),
            'group_accounts': _get_account_stats()['cumulative_group_accounts'][-1],
        },
    )
    # Go to utils/acct/check-dns to see how to aggregate the vhosts
# Returns number of pages printed this sememster
def _stats_printing():
    with get_connection() as c:
        c.execute(
                'SELECT sum((`public_jobs`.`count` * `public_jobs`.`pages`)) AS `sum` FROM `public_jobs` WHERE date(`public_jobs`.`day`) > "2017-08-22";')
    return c.fetchone()['sum']
