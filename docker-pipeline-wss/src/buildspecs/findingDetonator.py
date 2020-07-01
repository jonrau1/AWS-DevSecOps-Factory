import json

with open('dagdaFinding.json') as jsonFile:
    data = json.load(jsonFile)
    dagdaMalware = str(data[0]['static_analysis']['malware_binaries'])
    osVulnCount = str(data[0]['static_analysis']['os_packages']['vuln_os_packages'])
    pckgVulnCounter = str(data[0]['static_analysis']['prog_lang_dependencies']['vuln_dependencies'])
    if dagdaMalware == '[]':
        print('Dagda scan completed with no Malware detected! Total number of vulnerable OS packages is ' + osVulnCount + ' Total number of vulnerable code dependencies is ' + pckgVulnCounter)
        exit(0)
    else:
        print('Dagda scan detected Malware! Total number of vulnerable OS packages is ' + osVulnCount + ' Total number of vulnerable code dependencies is ' + pckgVulnCounter)
        exit(1)