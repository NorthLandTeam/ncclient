from .default import DefaultDeviceHandler

class NdsatcomDeviceHandler(DefaultDeviceHandler):
    def __init__(self, device_params):
        super(NdsatcomDeviceHandler, self).__init__(device_params)

    def get_capabilities(self):
        # Just need to replace a single value in the default capabilities
        c = super(NdsatcomDeviceHandler, self).get_capabilities()
        c.append('http://tail-f.com/ns/netconf/actions/1.0')
        c.append('http://tail-f.com/ns/netconf/extensions')
        c.append('http://ndsatcom.com/ns/compression?module=compression&revision=2018-03-14')
        c.append('http://ndsatcom.com/ns/crypto?module=crypto&revision=2018-04-23')
        c.append('http://ndsatcom.com/ns/dvb?module=dvb&revision=2017-07-12')
        c.append('http://ndsatcom.com/ns/gre?module=gre&revision=2018-03-15')
        c.append('http://ndsatcom.com/ns/mcast?module=mcast&revision=2017-11-22')
        c.append('http://ndsatcom.com/ns/ndsatcom?module=ndsatcom&revision=2013-08-08')
        c.append('http://ndsatcom.com/ns/node?module=node&revision=2018-02-27')
        c.append('http://ndsatcom.com/ns/odu?module=odu&revision=2017-12-18')
        c.append('http://ndsatcom.com/ns/openamip?module=openamip&revision=2018-03-12')
        c.append('http://ndsatcom.com/ns/qos?module=qos&revision=2018-01-25')
        c.append('http://ndsatcom.com/ns/satmux?module=satmux-sub&revision=2017-05-05')
        c.append('http://ndsatcom.com/ns/skywan?module=skywan&revision=2018-02-09')
        c.append('http://ndsatcom.com/ns/skywan5gstatic?module=skywan5gstatic&revision=2015-07-10')
        c.append('http://ndsatcom.com/ns/skywaniduwebui?module=skywaniduwebui&revision=2017-05-16')
        c.append('http://ndsatcom.com/ns/tdma?module=tdma&revision=2018-04-16')
        c.append('http://ndsatcom.com/ns/tdmacalc?module=tdmacalc-sub&revision=2018-02-09')
        c.append('http://tail-f.com/ns/aaa/1.1?module=tailf-aaa&revision=2015-06-16')

        return c