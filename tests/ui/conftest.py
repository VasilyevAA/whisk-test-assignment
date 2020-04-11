import pytest
from setting import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, WEB_DRIVER_NAME, get_test_browser_configs

if not all([BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY]):
    raise Exception('Need setup browserstack credentials for execute tests')

remote_server_url = f'https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub'


@pytest.fixture(
    scope='session',
    params=get_test_browser_configs(),
    ids=lambda param: repr('_'.join(param.get(i) for i in ['os', 'os_version', 'browser', 'browser_version']))
)
def parametrized_splinter_driver_kwargs(splinter_webdriver, request):
    """Parametrized webdriver kwargs."""
    if splinter_webdriver == 'remote':
        return request.param
    return {}


@pytest.fixture(scope='session')
def splinter_webdriver():
    """Override splinter webdriver name."""
    return WEB_DRIVER_NAME


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


@pytest.fixture()
def func_browser(request, browser):
    def quit_func_browser():
        browser.quit()
    request.addfinalizer(quit_func_browser)
    return browser
