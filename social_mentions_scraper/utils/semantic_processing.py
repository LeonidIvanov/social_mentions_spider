import re

# This regex string have to be extended with tlds and ctlds from source like https://www.iana.org/domains/root/db
TLDS_REGEX = r'\.wordpress\.com|\.com|\.net|\.org|\.info|\.coop|\.int'


def get_name_from_domain(domain):
    messy_name = re.split(TLDS_REGEX, domain)
    messy_name = messy_name[0].split('.')[-1]
    return messy_name.replace('http://', '').replace('https://', '')
