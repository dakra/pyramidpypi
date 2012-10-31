import os
import glob
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPOk, HTTPNotFound

@view_config(route_name='upload')
def upload(request):
    """Receive package from `python setup.py sdist upload -r localeggserver`"""

    name = request.params.get('name', '').lower()
    version = request.params.get('version')
    action = request.params.get(':action')
    content = request.params.get('content')

    if not (name and version and content.file and action == 'file_upload'):
        raise HTTPBadRequest()

    path = os.path.join(request.registry.settings['egg_path'], name)

    if not os.path.exists(path):
        os.makedirs(path)

    open(os.path.join(path, content.filename), 'wb').write(content.file.read())

    raise HTTPOk()

@view_config(route_name='pypi_listing', renderer='package_list.mako')
@view_config(route_name='list_all', renderer='package_list.mako')
def pypi_listing(request):
    """List all available packages including different versions"""

    egg_path = request.registry.settings['egg_path']
    egg_url = request.registry.settings['egg_url']
    packages = glob.glob(os.path.join(egg_path, '*', '*'))
    links = ['..%s%s'%(egg_url, p[len(egg_path):]) for p in packages]
    packages = [os.path.split(p)[1] for p in packages]

    return dict(title="All available eggs", links=links, packages=packages)

@view_config(route_name='list_versions', renderer='package_list.mako')
def list_versions(request):
    """List available versions for :request.matchdict:`package`"""

    egg_path = request.registry.settings['egg_path']
    package = request.matchdict.get('package')
    package_path = os.path.join(egg_path, package)
    if not os.path.isdir(package_path):
        raise HTTPNotFound()
    packages = os.listdir(package_path)
    links = [request.static_url(os.path.join(package_path, p)) for p in packages]

    return dict(title="All versions for {package}".format(package=package),
                links=links, packages=packages)

@view_config(route_name='list_packages', renderer='package_list.mako')
def list_packages(request):
    """List available packages with link to the different versions"""

    egg_path = request.registry.settings['egg_path']
    packages = os.listdir(os.path.join(egg_path))
    links = [request.route_url('list_versions', package=p) for p in packages]

    return dict(title="All packages", links=links, packages=packages)
