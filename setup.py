try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='ckanext-taxonomy',
    version="1.0",
    author='Ross Jones',
    author_email='ross@servercode.co.uk',
    license='Affero General Public License',
    url='http://github.com/datagovuk/ckanext-taxonomy',
    description="Hierarchical 'tags'.",
    keywords="taxonomy hierarchy",
    long_description="",
    zip_safe=False,
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ckanext', 'ckanext.taxonomy'],

    entry_points= {
    'paste.paster_command': [
        'taxonomy = ckanext.taxonomy.commands:TaxonomyCommand',
    ],
    'ckan.plugins': [
        'taxonomy = ckanext.taxonomy.plugin:TaxonomyPlugin',
    ]}
)
