from  django.shortcuts import render
from ocflib.lab.stats import current_semester_start
from ocflib.printing.printers import PRINTERS
from ocflib.printing.quota import get_connection
from ocflib.vhost import web, application, mail

def stats_money(request):
    return render(
        request,
        'stats/money_saved.html',
        {
            'title': 'Savings Statistics',
            'start_date': current_semester_start,
            'print_data': stats_printing(0.08),
            'website_data': stats_website(25),
            'value_data': stats_students(),
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

def _stats_website():
    domains = set()
    for primary_domain, vhost_config in web.get_vhosts().items():
        domains.add(primary_domain)
    for primary_domain, vhost_config in application.get_app_vhosts().items():
        domains.add(primary_domain)
    for vhost in mail.get_mail_vhosts():
        domains.add(vhost.domain)
    return len(domains)
def stats_website(cost):
    return [_stats_website()*cost, _stats_website()]

def _stats_students():
    """
    with get_connection() as c:
        c.execute(
            'SELECT count(distinct `session`.`user`) AS `count` FROM `session` WHERE date(`session`.`start`) > "2017-08-22";'
                )
    return c.fetchone()['count']
    """
    return 20000 #Dummy data

def stats_students():
    return [_stats_students(), 8, _stats_students()*2]
