import pytest
from selene import browser, be, have


"""
Параметризуйте фикстуру несколькими вариантами размеров окна
Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот)
"""


def is_mobile(width):
    return width < 1012


@pytest.fixture(
    scope='function',
    autouse=True,
    params=[(1920, 1080), (1440, 900), (360, 640), (800, 600)]
)

def browser_manager(request):
    browser.config.base_url = 'https://github.com'
    browser.config.window_width = request.param[0]
    browser.config.window_height = request.param[1]
    yield
    browser.quit()


def test_github_desktop():
    if is_mobile(browser.config.window_width):
        pytest.skip('Этот тест только для десктопа')
    browser.open('https://github.com/')
    browser.element('[href="/login"]').click()
    assert browser.element('#login_field').should(be.visible)
    assert browser.element('#password').should(be.visible)
    assert browser.element('.auth-form-header').should(
        have.exact_text('Sign in to GitHub'))


def test_github_mobile():
    if not is_mobile(browser.config.window_width):
        pytest.skip('Этот тест только для мобильных устройств')
    browser.open('https://github.com/')
    browser.element('[aria-label="Toggle navigation"] [class=Button-content]').click()
    browser.element('[href="/login"]').click()
    assert browser.element('#login_field').should(be.visible)
    assert browser.element('#password').should(be.visible)
    assert browser.element('.auth-form-header').should(
        have.exact_text('Sign in to GitHub'))