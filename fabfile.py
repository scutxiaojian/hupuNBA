from fabric.api import env, sudo, cd, run, local, put  #@UnresolvedImport

# ssh user
env.user = "cxj"
env.hosts = ["127.0.0.1"]

APP_ROOT = '/home/cxj/workspace/hupuNBA/hupunba'


def runcrawl():
    with cd( APP_ROOT ):
        run( 'scrapy crawl hupu' )