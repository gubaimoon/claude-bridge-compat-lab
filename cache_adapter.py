"""Experimental cache-marker compatibility for the Claude Code bridge."""
from copy import deepcopy


def adapt_request(request):
    result = deepcopy(request)
    system = result.get('system')
    if isinstance(system, list):
        for block in system:
            if isinstance(block, dict):
                block.pop('cache_control', None)
    tools = result.get('tools')
    if isinstance(tools, list):
        for tool in tools:
            if isinstance(tool, dict):
                tool.pop('cache_control', None)
    return result
