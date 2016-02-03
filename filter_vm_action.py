"""
FilterVmAction - custom action.

Simple action for filtering VM on the presence of metadata/extra spec
"evacuate" flag
"""
from mistral.actions import base


class FilterVmAction(base.Action):
    """
    Filter and return VMs whith the flag 'evacuate' either on vm metadtata
    or flavor extra spec.
    """

    def __init__(self, flavors, vms):
        """init."""
        self._flavors = flavors
        self._vms = vms

    def run(self):
        """Entry point for the action execution."""
        result = []

        for vm in self._vms:
            if str(vm['metadata'].get('evacuate')).upper() == 'TRUE'\
                or (str(vm['metadata'].get('evacuate')).upper() != 'FALSE'
                    and vm['flavor']['id'] in self._flavors):
                result.append(vm['id'])

        return result