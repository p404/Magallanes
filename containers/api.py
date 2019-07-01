from core.api import add_host, delete_host
from kubernetes import client, config, watch

def magallanes_service(service_obj):
   hostname = service_obj.metadata.annotations.get('magallanes/hostname')
   host     = str(service_obj.status.load_balancer.ingress[0].ip)
   port     = str(service_obj.spec.ports[0].port)
   external = True if service_obj.metadata.annotations.get('magallanes/external') == 'true' else False
   return hostname, host, external, port

def magallanes_init():
   config.load_kube_config()
   watch_obj = watch.Watch()
   v1 = client.CoreV1Api()

   for event in watch_obj.stream(v1.list_service_for_all_namespaces):
      if (event['type'] == 'ADDED' or event['type'] == 'MODIFIED') & (event['object'].metadata.annotations is not None):
          if 'magallanes' in event['object'].metadata.annotations:
            if event['object'].status.load_balancer.ingress is not None:
               hostname, host, external, port = magallanes_service(event['object'])
               add_host(hostname, host, external, port)
      if (event['type'] == 'DELETED') &  (event['object'].metadata.annotations is not None):
         if 'magallanes' in event['object'].metadata.annotations:
            hostname, host, external, port = magallanes_service(event['object'])
            delete_host(hostname, host, external, port)