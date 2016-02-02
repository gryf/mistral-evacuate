"""
FilterVmAction - custom action.

Simple action for filtering VM on the presence of metadata/extra spec
"evacuate" flag
"""
from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result


class FilterVmException(Exception):
    pass


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
            return Result(data={'evacuate': True, 'uuid': self._uuid})
        elif str(metadata.get('evacuate')).upper() == 'FALSE':
            return Result(data={'evacuate': False, 'uuid': self._uuid})

        # Ether is no metadata for vm - check flavor.
        try:
            # Maybe this should be done in different action
            # only once per whole workflow.
            # In case there is ~100 VMs to evacuate, there will be
            # the same amount of calls to nova API.
            flavor = filter(
                lambda f: f.id == self._flavor,
                client.flavors.list()
            )[0]
        except IndexError:
            raise FilterVmException('Flavor not found')

        evacuate = flavor.get_keys().get('evacuation:evacuate')

        if str(evacuate).upper() == 'TRUE':
            return Result(data={'evacuate': True, 'uuid': self._uuid})

        return Result(data={'evacuate': False, 'uuid': self._uuid})
