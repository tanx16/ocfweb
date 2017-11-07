from ocflib.lab.stats import current_semester_start
from  django.shortcuts import render
from ocflib.printing.printers import PRINTERS
from ocflib.printing.quota import get_connection
from ocflib.vhost import web, application, mail
from ocfweb.stats.accounts import _get_account_stats

def stats_money(request):
    return render(
        request,
        'stats/money_saved.html',
        {
            'title': 'Savings Statistics',
            'start_date': current_semester_start,
            'print_data': stats_printing(0.08),
            'website_count': stats_website(),
            'website_cost': website_cost(25)
        },
    )
    # Go to utils/acct/check-dns to see how to aggregate the vhosts
# Returns number of pages printed this sememster
def _stats_printing():
    with get_connection() as c:
        c.execute(
                'SELECT sum((`public_jobs`.`count` * `public_jobs`.`pages`)) AS `sum` FROM `public_jobs` WHERE date(`public_jobs`.`day`) > "2017-08-22";')
    return c.fetchone()['sum']

def stats_printing(cost):
    return ['{:,.2f}'.format(float(_stats_printing())*cost), _stats_printing()]

def stats_website():
    domains = set()
    for primary_domain, vhost_config in web.get_vhosts().items():
        domains.add(primary_domain)
    for primary_domain, vhost_config in application.get_app_vhosts().items():
        domains.add(primary_domain)
    for vhost in mail.get_mail_vhosts():
        domains.add(vhost.domain)
    return len(domains)
def website_cost(cost):
    return stats_website()*cost
