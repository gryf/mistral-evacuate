"""
FindFlavorsByExtraSpecs - custom action.

It works pretty similar to nova.flavors_findall, but it looks for items in
flavors extra spec
"""

from mistral.actions.openstack.actions import NovaAction


class FindFlavorsByExtraSpecs(NovaAction):

    def __init__(self, extra_specs):
        if type(extra_specs) is dict:
            self._extra_specs = extra_specs
        else:
            raise TypeError("Extra spec must be a dictionary")

    def run(self):
        client = self._get_client()
        flavors = client.flavors.list()
        result = []

        for flavor in flavors:
            flavor_extra_specs = flavor.get_keys().items()
            if all(
                    item in flavor_extra_specs
                    for item in self._extra_specs.items()
            ):
                result.append(flavor.id)

        return result