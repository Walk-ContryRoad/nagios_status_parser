import shutil, re, json

class SimpleConfigParser():

    """
        SimpleConfigParser
        Inspired by: http://www.decalage.info/fr/python/configparser
        Polished up a bit by Charles Hamilton (musashi@nefaria.com)

        >>> s = SimpleConfigParser()
        >>> config_options = s.parse_config('/etc/kernel-img.conf')
        >>> config_options['do_symlinks']
        'yes'

    """

    def __init__(self, comment_char = '#', option_char = '=', \
                allow_duplicates = False, strip_quotes = True):
        self.comment_char = comment_char
        self.option_char = option_char
        self.allow_duplicates = allow_duplicates
        self.strip_quotes = strip_quotes


    def parse_config(self, filename):
        self.options = {}
        config_file = open(filename, 'r')
        for line in config_file:
            if self.comment_char in line:
                line, comment = line.split(self.comment_char, 1)
            if self.option_char in line:
                option, value = line.split(self.option_char, 1)
                option = option.strip()
                value = value.strip()
                value = value.strip('"\'')
                if self.allow_duplicates:
                    if option in self.options:
                        if not type(self.options[option]) == list:
                            old_value = self.options[option]
                            self.options[option] = [value] + [old_value]
                        else:
                            self.options[option] += [value]
                    else:
                        self.options[option] = value
                else:
                    self.options[option] = value
        config_file.close()
        return self.options


class NagiosStatusParser():

    """
        NagiosStatusParser -- a parser for Nagios' status.dat file

        >>> s = SimpleConfigParser()
        >>> nagios_config = s.parse_config('/etc/nagios3/nagios.cfg')
        >>> nagios_config['status_file']
        '/var/cache/nagios3/status.dat'
        >>> n = NagiosStatusParser(nagios_config['status_file'])
        >>> json_data = n.to_json()
        >>> import json
        >>> status_data = json.loads(json_data)

    """

    def __init__(self, status_file):
        shutil.copy(status_file, '/tmp/nagios_status.tmp')
        # Ugh.. read the whole file into memory because re.finditer
        # won't work correctly without the entire file 
        # (i.e., can't do it in chunks)
        data = open(status_file, 'r').read()
        self.host_stats = []                
        for match in re.finditer(r"[^{]*\{([^}]+)\}", data):
            options = {}
            for line in match.group(1).splitlines():
                line = line.strip()
                if not re.match('^[\s]*$', line):
                    option, value = line.split('=', 1)
                    options[option] = value
            self.host_stats += [options]


    def to_json(self, indent = 0):
        if indent:
            return json.dumps(self.host_stats, indent = indent)
        else:
            return json.dumps(self.host_stats)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
