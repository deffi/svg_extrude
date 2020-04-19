from contextlib import nullcontext


def conditional_context(condition, context_manager, alternative_enter_result):
    if condition:
        return context_manager
    else:
        return nullcontext(alternative_enter_result)
