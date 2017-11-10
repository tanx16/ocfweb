from  django.shortcuts import render
from ocflib.lab.stats import current_semester_start
from ocflib.printing.printers import PRINTERS
from ocflib.printing.quota import get_connection
from ocflib.vhost import web, application, mail

PAGE_COST = 0.08
PAGES_PER_SEMESTER = 100
GROUP_WEBSITE_COST = 25
PERSONAL_WEBSITE_COST = 2

def stats_money(request):
    return render(
        request,
        'stats/money_saved.html',
        {
            'title': 'Savings Statistics',
            'start_date': current_semester_start,
            'print_data': stats_printing(PAGE_COST),
            'website_data': stats_website(GROUP_WEBSITE_COST),
            'value_data': stats_students(PAGE_COST, PAGES_PER_SEMESTER, PERSONAL_WEBSITE_COST),
            'constants': [PAGE_COST, PAGES_PER_SEMESTER, GROUP_WEBSITE_COST, PERSONAL_WEBSITE_COST],
        },
    )
# Returns number of pages printed this sememster
def _stats_printing():
    with get_connection() as c:
        c.execute(
                'SELECT sum((`public_jobs`.`count` * `public_jobs`.`pages`)) AS `sum` FROM `public_jobs` WHERE date(`public_jobs`.`day`) > "2017-08-22";')
    return c.fetchone()['sum']

def stats_printing(cost):
    return [format_money(float(_stats_printing())*cost), _stats_printing()]

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
    with get_connection(db='ocfstats') as c:
        c.execute(
            'SELECT * FROM `unique_users_in_lab_count_public` WHERE 1;'
            )
    return c.fetchone()['users']

def stats_students(pagecost, pages, webcost):
    return [_stats_students(), format_money(pagecost*pages), format_money(_stats_students()*webcost)]
def format_money(cost):
    return '{:,.2f}'.format(float(cost))
