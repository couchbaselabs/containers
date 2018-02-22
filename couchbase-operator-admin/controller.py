# kubernetes controller for applying cluster-admin
# credentials to couchbase-operator deployments
import json
import jsonpickle
from openshift import client, config
from kubernetes import client as kubeClient, watch

# use local .kube/config unless running inside
# of a pod
try:
    config.load_kube_config()
except:
    config.load_incluster_config()

class JSONSerializable(object):
    def json(self):
        return json.loads(jsonpickle.encode(self, unpicklable=False))

class Metadata(object):
    def __init__(self, name, project):
        self.name = name
        self.namespace = project

class ClusterAdminRoleRef(object):
    def __init__(self):
        self.kind = "ClusterRole"
        self.name = "cluster-admin"
        self.apiGroup = "rbac.authorization.k8s.io"

class DefaultServiceAccountSubject(object):
    def __init__(self, project):
        self.kind = "ServiceAccount"
        self.name = "default"
        self.apiGroup = "rbac.authorization.k8s.io"
        self.namespace = project

class ClusterRoleBinding(JSONSerializable):
    def __init__(self, project):
        self.kind= "ClusterRoleBinding"
        self.name = "{}-operator-cluster-admin".format(project)
        self.metadata = Metadata(self.name, project)
        self.subjects= [DefaultServiceAccountSubject(project)]
        self.roleRef = ClusterAdminRoleRef()

class SecurityContextConstraints(JSONSerializable):
    def __init__(self, project):
        self.kind = "SecurityContextConstraints"
        self.name = "{}-scc".format(project)
        user = "system:serviceaccount:{}:default".format(project)
        self.metadata = Metadata(self.name, project)
        self.allowPrivilegedContainer = False
        self.readOnlyRootFilesystem = False
        self.runAsUser = SecurityContextConstraintType("RunAsAny")
        self.seLinuxContext = SecurityContextConstraintType("MustRunAs")
        self.fsGroup = SecurityContextConstraintType("RunAsAny")
        self.supplementalGroups = SecurityContextConstraintType("RunAsAny")
        self.priority = 10
        self.users = [user]

class SecurityContextConstraintType(object):
    def __init__(self, typ):
        self.type = typ


def update_project_scc(project):
    api = client.SecurityOpenshiftIoV1Api()
    scc = SecurityContextConstraints(project)
    try:
        api.read_security_context_constraints(scc.name)
    except kubeClient.rest.ApiException:
        api.create_security_context_constraints(scc.json())

def update_project_rbac(project):
    api = client.OapiApi()
    rbac = ClusterRoleBinding(project)
    try:
        try:
            api.read_cluster_role_binding(rbac.name)
        except kubeClient.rest.ApiException:
             api.create_cluster_role_binding(rbac.json())
    except ValueError:
        # object exists but it's return value is not parsable
        # this is underlying client bug
        pass

def main():

    # watch for creation of CRD's
    crds = kubeClient.CustomObjectsApi()
    domain = "couchbase.database.couchbase.com"
    resource_version = ''
    while True:
	stream = watch.Watch().stream(crds.list_cluster_custom_object,
                                      domain, "v1beta1",
                                      "couchbaseclusters",
                                      resource_version=resource_version)

        # only process ADD events
	for event in stream:
            if event['type'] != "ADDED":
                continue
            obj = event.get("raw_object")
            metadata = obj.get("metadata")
            project = metadata["namespace"]
            try:
                update_project_scc(project)
                update_project_rbac(project)
                print("Set up project: {}!".format(project))
            except Exception as ex:
                print("Unexpected exception occured: {}".format(ex))

if __name__ == "__main__":
    main()
