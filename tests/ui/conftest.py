import pytest
from setting import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY

if not all([BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY]):
    raise Exception('Need setup browserstack credentials for execute tests')

remote_server_url = f'https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub'

_desired_cap1 = {
 'browser': 'Chrome',
 'browser_version': '80.0',
 'os': 'Windows',
 'os_version': '10',
 'resolution': '1024x768'
}

desired_cap_1 = dict(_desired_cap1, **{
    'name': 'Bstack-[Python] Sample Test in Safari',
    'browserstack.debug': True
})

_desired_cap2 = {
 'browser': 'Safari',
 'browser_version': '13.0',
 'os': 'OS X',
 'os_version': 'Catalina',
 'resolution': '1024x768'
}

desired_cap_2 = dict(_desired_cap2, **{
    'name': 'Bstack-[Python] Sample Test in Safari',
    'browserstack.debug': True
})

@pytest.fixture(
    scope='session',
    params=[
        # desired_cap_1,
        desired_cap_2,
    ],
)
def parametrized_splinter_driver_kwargs(splinter_webdriver, request):
    """Parametrized webdriver kwargs."""
    if splinter_webdriver == 'remote':
        return request.param
    return {}


# @pytest.fixture(scope='session')
# def splinter_webdriver():
#     """Override splinter webdriver name."""
#     return 'remote'


@pytest.fixture(scope='session')
def splinter_browser_class(request, parametrized_splinter_driver_kwargs):
    from pytest_splinter.plugin import Browser

    def FixedBrowser(driver_name, *args, **kwargs):
        if driver_name == "remote":
            kwargs.pop('firefox_profile')
            kwargs.pop('moz:firefoxOptions')
            kwargs['command_executor'] = remote_server_url
            kwargs['desired_capabilities'] = parametrized_splinter_driver_kwargs
        return Browser(
            driver_name,
            *args, **kwargs
        )

    return FixedBrowser
