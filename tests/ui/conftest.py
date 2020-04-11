import pytest
from splinter import Browser

from setting import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, WEB_DRIVER_NAME, get_test_browser_configs, \
    IS_LOCAL_BROWSER_EXECUTION

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

# Need if u want optimize restart browser(only clear cache), but then u can't start many browsers with many OS
# @pytest.fixture(scope='session')
# def splinter_browser_class(request, parametrized_splinter_driver_kwargs):
#     from pytest_splinter.plugin import Browser
#
#     def FixedBrowser(driver_name, *args, **kwargs):
#         if driver_name == "remote":
#             kwargs.pop('firefox_profile')
#             kwargs.pop('moz:firefoxOptions')
#             kwargs['command_executor'] = remote_server_url
#             kwargs['desired_capabilities'] = parametrized_splinter_driver_kwargs
#         return Browser(
#             driver_name,
#             *args, **kwargs
#         )
#
#     return FixedBrowser


@pytest.fixture()
def func_browser(request, splinter_webdriver, parametrized_splinter_driver_kwargs):
    parametrized_splinter_driver_kwargs['name'] = request.node.name
    browser_cfg = {
        'driver_name': splinter_webdriver,
        'desired_capabilities': parametrized_splinter_driver_kwargs,
    }
    if not IS_LOCAL_BROWSER_EXECUTION:
        browser_cfg['command_executor'] = remote_server_url
    _browser = Browser(**browser_cfg)
    def quit_func_browser():
        _browser.quit()
    request.addfinalizer(quit_func_browser)
    return _browser

