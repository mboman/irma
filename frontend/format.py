

def format_av(output, result):
    if 'data' in result:
        data = result['data']
        if 'scan_results' in data:
            res_list = data['scan_results'].values()
            if len(res_list) > 1:
                # if multiple output, filter None results
                res = [item for item in res_list if item is not None]
                output['result'] = " - ".join(res)
            else:
                output['result'] = res_list[0]
        else:
            output['result'] = "not parsed"
        if 'name' in result and 'version' in data:
            name = data['name']
            version = data['version']
            output['version'] = "{0} {1}".format(name, version)
        elif 'name' in data:
            output['version'] = data['name']
    else:
        output['result'] = "Error"
    return


def format_vt(output, result):
    """ VT AVs list
    'Bkav', 'MicroWorld-eScan', 'nProtect', 'K7AntiVirus', 'NANO-Antivirus',
    'F-Prot', 'Norman', 'Kaspersky', 'ByteHero', 'F-Secure', 'TrendMicro',
    'McAfee-GW-Edition', 'Sophos', 'Jiangmin', 'ViRobot', 'Commtouch',
    'AhnLab-V3', 'VBA32', 'Rising', 'Ikarus', 'Fortinet', 'Panda',
    'CAT-QuickHeal', 'McAfee', 'Malwarebytes', 'K7GW', 'TheHacker',
    'TotalDefense', 'TrendMicro-HouseCall', 'Avast', 'ClamAV', 'BitDefender',
    'Agnitum', 'Comodo', 'DrWeb', 'VIPRE', 'AntiVir', 'Emsisoft', 'Antiy-AVL',
    'Kingsoft', 'Microsoft', 'SUPERAntiSpyware', 'GData', 'ESET-NOD32',
    'AVG', 'Baidu-International', 'Symantec', 'PCTools',
    """
    output['type'] = "web"
    if 'data' in result:
        data = result['data'].values()[0]
        if type(data) is int:
            output['result'] = "error {0}".format(data)
        if 'response_code' in data and data['response_code'] == 0:
            output['result'] = "file never scanned"
        if 'scans' in data:
            scan = data['scans']
            for av in ['ClamAV', 'Kaspersky', 'Symantec', 'McAfee',
                       'Sophos', 'Comodo', 'ESET-NOD32', 'F-Prot']:
                if av in scan:
                    output[av] = scan[av]['result']
        if 'scan_date' in data:
            output['version'] = data['scan_date']
    else:
        output['result'] = "Error"
    return


def format_static(output, result):
    output['type'] = "information"
    if 'data' in result:
        data = result['data'].values()[0]
        if type(data) == dict:
            output['result'] = data
        else:
            output['result'] = "no results"
    else:
        output['result'] = "not a PE file"
    return


def format_nsrl(output, _):
    output['type'] = "database"
    output['result'] = "no formatter"
    output['version'] = "unknown"
    return


def format_default(output, _):
    output['result'] = "no formatter"
    output['version'] = "unknown"
    return


def sanitize_dict(d):
    new = {}
    for k, v in d.iteritems():
        if isinstance(v, dict):
            v = sanitize_dict(v)
        newk = k.replace('.', '_').replace('$', '')
        new[newk] = v
    return new

probe_formatter = {
    # antivirus
    'ClamAV': format_av,
    'ComodoCAVL': format_av,
    'EsetNod32': format_av,
    'FProt': format_av,
    'Kaspersky': format_av,
    'McAfeeVSCL': format_av,
    'Sophos': format_av,
    'Symantec': format_av,
    # database
    'Nsrl': format_nsrl,
    # information
    'StaticAnalyzer': format_static,
    # web
    'VirusTotal': format_vt,
    }


def format_result(probe, raw_result):
    probe_result = sanitize_dict(raw_result)
    formatter = probe_formatter.get(probe, format_default)
    res = {}
    formatter(res, probe_result)
    return res
