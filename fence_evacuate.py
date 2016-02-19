#!/usr/bin/python -tt

import sys
import logging
import atexit
from mistralclient.api import client
sys.path.append("/usr/share/fence")
from fencing import run_delay, all_opt, atexit_handler, check_input, \
        process_input, show_docs


def define_new_opts():
    all_opt["domain"] = {
        "getopt": "d:",
        "longopt": "domain",
        "help": "-d, --domain=[string]          DNS domain in which hosts"
                         " live, useful when the cluster uses short names and"
                         " nova uses FQDN",
        "required": "0",
        "shortdesc": "DNS domain in which hosts live",
        "default": "",
        "order": 5,
    }
    all_opt["user"] = {
        "getopt": "u:",
        "longopt": "user",
        "help": "-u, --rabbit_user=string User to connect to Mistral",
        "required": "1",
        "shortdesc": "User to connect to Mistral",
        "default": "",
        "order": 5,
    }
    all_opt["password"] = {
        "getopt": "p:",
        "longopt": "password",
        "help": "-p, --password=string Password to connect to Mistral",
        "required": "1",
        "shortdesc": "Password to connect to Mistral",
        "default": "",
        "order": 5,
    }
    all_opt["tenant"] = {
        "getopt": "t:",
        "longopt": "tenant",
        "help": "-t, --tenant=string Tenant name to connect to Mistral",
        "required": "1",
        "shortdesc": "Tenant name to connect to Mistral",
        "default": "",
        "order": 5,
    }
    all_opt["auth_url"] = {
        "getopt": "a:",
        "longopt": "auth_url",
        "help": "-a, --auth_url=string auth_url to connect to Mistral",
        "required": "1",
        "shortdesc": "auth_url to connect to Mistral",
        "default": "",
        "order": 5,
    }
    all_opt["wf_name"] = {
        "getopt": "w:",
        "longopt": "wf_name",
        "help": "-w, --wf_name=string Workflow name to run by Mistral",
        "required": "1",
        "shortdesc": "Workflow name to run by Mistral",
        "default": "",
        "order": 5,
    }


def format_message(host, on_shared_storage):
    result = {
        "search_opts": {
            "host": host
        },
        "on_shared_storage": on_shared_storage,
        "flavor_extra_specs": {
            "evacuation:evacuate": True
        }
    }
    return result


def evacuate(host, options):
    user = options["--user"]
    password = options["--password"]
    tenant = options["--tenant"]
    auth_url = options["--auth_url"]
    wf_name = options["--wf_name"]

    input_json = format_message(host, False)

    mistral = client.client(
        username=user,
        api_key=password,
        project_name=tenant,
        auth_url=auth_url
    )

    mistral.executions.create(wf_name,
                              input_json)


def main():
    atexit.register(atexit_handler)

    device_opt = ["user", "domain", "password", "tenant", "auth_url",
                  "wf_name", "port"]
    define_new_opts()
    all_opt["shell_timeout"]["default"] = "180"

    options = check_input(device_opt, process_input(device_opt))

    docs = {}
    docs["shortdesc"] = "Fence agent for nova compute nodes"
    docs["longdesc"] = "fence_evacuate is a Nova fencing notification agent"
    docs["vendorurl"] = ""

    show_docs(options, docs)
    run_delay(options)

    host = None
    # Potentially we should make this a pacemaker feature
    if options["--domain"] != "" and "--plug" in options:
        options["--plug"] = options["--plug"] + "." + options["--domain"]

    if "--plug" in options:
        host = options["--plug"]

    if options['--action'] in ['reboot', 'off']:
        if host is None:
            logging.error('No host specified')
            sys.exit(1)

        evacuate(host, options)
        logging.error('Cannot connect to mistral')
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
