import sys

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="cmis_storage.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "cmis_storage",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
        CMIS_STORAGE_OPTIONS={
            'repositoryUrl': 'http://localhost:8080/alfresco/api/-default-/public/cmis/versions/1.0/atom',
            'username': 'admin',
            'password': 'admin',
            'baseFolder': '/'
        }
    )

    try:
        import django

        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback

    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
