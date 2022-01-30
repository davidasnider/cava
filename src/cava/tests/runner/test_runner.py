from cava.runner.actions import indigo_executor


def test_call_action_group(set_environ):
    uri = "/actions/test%20for%20cava"
    my_executor = indigo_executor(uri=uri)
    my_executor.execute_action()
    assert my_executor.success  # This should be true


def test_call_action_group_fail(set_environ):
    uri = "/thisisnotvalid"
    my_executor = indigo_executor(uri=uri)
    my_executor.execute_action()
    assert my_executor.success is False  # This should be true
