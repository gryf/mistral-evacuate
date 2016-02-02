from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result


class EvacuateVmAction(NovaAction):

    def __init__(self, uuid, on_shared_storage, evacuate):
        self._uuid = uuid
        self._on_shared_storage = on_shared_storage
        self._evacuate = evacuate

    def run(self):
        client = self._get_client()

        if self._evacuate:
            client.servers.evacuate(self._uuid,
                                    on_shared_storage=self._on_shared_storage)
