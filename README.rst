Mistral evacuate plugin
=======================

This is a PoC for providing automatic evacuation for VMs in OpenStack cloud
using Mistral.

Installation
------------

#. Copy ``filter_vm.py`` to the place reachable by python interpreter - see
   ``PYTHONPATH`` or ``sys.path`` for reference.
#. Append line

   .. code:: ini

      [entry_points]
      mistral.actions =
          …
          custom.filter_vms = evac_poc:FilterAndEvacuate

   to ``setup.cfg`` file under Mistral repository
#. Reinstall Mistral if it was installed in system (not in virtualenv).
#. Run db-sync tool via either

   .. code:: shell-session

      $ tools/sync_db.sh --config-file <path-to-config>

   or

   .. code:: shell-session

      $ mistral-db-manage --config-file <path-to-config> populate

#. Register Mistral workflow:

   .. code:: shell-session

      $ mistral workflow-create evacuate-workflow.yaml

#. Create JSON file with content similar to:

   .. code:: json

     {
         "search_opts": {
             "host": "compute-hostanme"
         }
     }

#. Trigger the action via:
   TBD
