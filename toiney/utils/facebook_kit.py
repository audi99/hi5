from toiney.core.models.device import device_id
# register with facebook kit (phone number)


def auth():
    kit_token = '3d6ee4b25dcd3e54deccf9f10ff12b6c'
    kit_id = '158845517509768'

    access_token = 'AA|{0}|{1}'.format(kit_id, kit_token)
    return access_token


def variant():
    # queries
    params = {
        'method': 'tagged.mobile.experiments.doVariantAssignmentForDevice',
        'experiment': 'prime_android_account_kit',
        'variant': '1',
        'device_id': device_id,
        'application_id': 'user'
    }

    return params
