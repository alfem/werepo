from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Werepo'
settings.subtitle = 'Web Repository'
settings.author = 'Alfonso de Cala'
settings.author_email = 'alfonso.cala@juntadeandalucia.es'
settings.keywords = 'repository, debian, packages'
settings.description = 'Web interface to debian style packages repository'
settings.layout_theme = 'Industrial'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = 'b43aa66b-2cde-458e-88b2-fab9a8adc46b'
settings.email_server = 'mail.juntadeandalucia.es'
settings.email_sender = 'alfonso.cala@juntadeandalucia.es'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
