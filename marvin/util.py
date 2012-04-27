def get_channel(line):
    if line.startswith('#'):
        return line
    else:
        return '#' + line
