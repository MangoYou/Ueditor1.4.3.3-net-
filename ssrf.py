#coding : utf-8
from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server

flag=0

class DynamicResolver(object):

    def _doDynamicResponse(self, query):
        name = query.name.name
        global flag
        if flag==0 or flag==1:
            ip="106.14.189.174"
            flag=flag+1
        else:
            ip="192.168.121.129"
            flag=0

        print name+" ===> "+ip

        answer = dns.RRHeader(
            name=name,
            type=dns.A,
            cls=dns.IN,
            ttl=0,
            payload=dns.Record_A(address=b'%s'%ip,ttl=0)
        )
        answers = [answer]
        authority = []
        additional = []
        return answers, authority, additional

    def query(self, query, timeout=None):
        return defer.succeed(self._doDynamicResponse(query))

def main():
    factory = server.DNSServerFactory(
        clients=[DynamicResolver(), client.Resolver(resolv='/etc/resolv.conf')]
    )

    protocol = dns.DNSDatagramProtocol(controller=factory)
    reactor.listenUDP(53, protocol)
    reactor.run()



if __name__ == '__main__':
    raise SystemExit(main())
