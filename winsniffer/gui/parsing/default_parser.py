from packet_parser import PacketParser


class DefaultParser(PacketParser):

    def condition(self, protocols, data):
        return True

    def parse(self, frame, data):

        threshold = 80

        if data == '\x00':
            data_preview = '00'

        elif self.is_printable(data):
            # Cut the printable data at the threshold
            data_preview = data[:min(threshold, len(data) - 1)]
            data_preview = unicode(data_preview).replace('\r\n', ' ').replace('\n', ' ')
        else:
            # Cut the raw non-printable data at the fourth of the threshold
            data_preview = data[:min(threshold / 3, len(data) - 1)]
            data_preview = self.hex_dump(data_preview)

        # We truncated the data so add a ... indicator for that
        if len(data) > threshold:
            data_preview += "..."

        return data_preview
