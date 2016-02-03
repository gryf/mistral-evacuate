Mistral evacuate plugin
=======================

This is a PoC for providing automatic evacuation for VMs in OpenStack cloud
using Mistral.

Installation
------------

#. Copy ``filter_vm_action.py`` and ``evacuate_vm_action.py``
   to the place reachable by python interpreter -
   see ``PYTHONPATH`` or ``sys.path`` for reference.
#. Append lines

   .. code:: ini

      [entry_points]
      mistral.actions =
          …
          custom.filter_vm = filter_vm_action:FilterVmAction
          custom.evacuate = evacuate_vm_action:EvacuateVmAction

   to ``setup.cfg`` file under Mistral repository
#. Run db-sync tool via either

   .. code:: shell-session

      $ tools/sync_db.sh --config-file <path-to-config>

   or

   .. code:: shell-session

      $ mistral-db-manage --config-file <path-to-config> populate

#. Register Mistral workflow:

   .. code:: shell-session

      $ mistral workflow-create host-evacuate.yaml

#. Create JSON file with content similar to:

   .. code:: json

     {
         "search_opts": {
             "host": "compute-hostanme"
         },
         "on_shared_storage": false
     }

#. Trigger the action via:

   .. code:: shell-session

      $ mistral execution-create host-evacuate input.json

   where ``input.json`` is a file created in previous step.
