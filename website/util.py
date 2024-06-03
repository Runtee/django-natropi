from .models import Website


def project_name():
    try:
        website, created = Website.objects.get_or_create(id=1)
        return website.name
    except Exception as e:
        print(e)
        return 'Blank Name'

project = project_name()