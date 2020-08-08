import re
import urllib.request 


def getCeneoPrice(product_id, debug_enabled = False):
    request = urllib.request.urlopen("https://www.ceneo.pl/" + str(product_id))
    html = request.read().decode('UTF-8')
    
    retval = []
     
    pattern = '<span class="value">([0-9]{1,})<\/span><span class="penny">,([0-9]{2})<\/span>'
    for match in re.findall(pattern, html):
        retval.append(match)
        
    if(debug_enabled):
        with open('CeneoPage.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
    if((len(retval) > 0) and (len(retval[0]) == 2)):
        return float('{0}.{1}'.format(retval[0][0],retval[0][1]))
    else:
        return -1