import consul

CONSUL_CLIENT = consul.Consul()

def add_host_consul(hostname, host, external, port):
   CONSUL_CLIENT.kv.put('ingress/{}/port'.format(hostname), port)
   CONSUL_CLIENT.kv.put('ingress/{}/host'.format(hostname), host)
   CONSUL_CLIENT.kv.put('ingress/{}/external'.format(hostname), "{}".format(external))

def delete_host_consul(hostname):
   CONSUL_CLIENT.kv.delete('ingress/{}'.format(hostname), recurse=True)