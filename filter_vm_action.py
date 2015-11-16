"""
FilterVmAction - custom action.

Simple action for filtering VM on the presence of metadata/extra spec
"evacuate" flag
"""
from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result


class FilterVmAction(NovaAction):
    """
    Filter and return VMs whith the flag 'evacuate' either on vm metadtata
    or flavor extra spec.
    """

    def __init__(self, metadata, flavor, uuid):
        """init."""
        self._metadata = metadata
        self._flavor = flavor
        self._uuid = uuid

    def run(self):
        """Entry point for the action execution."""
        client = self._get_client()
        metadata = self._metadata

        if str(metadata.get('evacuate')).upper() == 'TRUE':
            return Result(data={'status': 0, 'uuid': self._uuid})
        elif str(metadata.get('evacuate')).upper() == 'FALSE':
            return Result(error='sie nie udalo!!!!1111jeden')

        # ether is no metadata for vm - check flavor
        flavors = client.flavors.list()
        try:
            flavor = filter(lambda x: x.id == self._flavor, flavors)[0]
        except:
            raise Exception('Flavor not found')

        evacuate = flavor.get_keys().get('evacuation:evacuate')

        if str(evacuate).upper() == 'TRUE':
            return Result(data={'status': 0, 'uuid': self._uuid})

        return Result(data='1', error=True)
