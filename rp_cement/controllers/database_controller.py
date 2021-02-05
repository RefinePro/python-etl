from cement import ex
from .base_controller import BaseController

import peewee as pw
import peeweedbevolve
from pwiz import make_introspector, print_models
from urllib.parse import urlparse
from playhouse.db_url import parseresult_to_dict

class DatabaseController(BaseController):

    class Meta:
        label = 'rp-db'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @ex(
        help='Test the database connexion, show sql server info'
    )
    def db_test(self):
        """Example sub-command."""
        from models.db import db        
        try:
            db.connect()
            connected = db.is_connection_usable()
            self.app.log.debug('Connection is OK')
        except Exception as err:
            self.app.log.fatal(err)

    @ex(
        help='Migrate the database',
    )
    def db_migrate(self):
        # We care only about the tables defined in models
        from models.db import db
        declared_tables = [m._meta.table_name for m in pw.Model.__subclasses__()]
        out_of_scope_tables = [t if t not in declared_tables else None for t in db.get_tables()]
        [self.app.log.warning('Table '+table+' is not a Model and will be ignored') for table in out_of_scope_tables]
        db.evolve(ignore_tables=out_of_scope_tables)


    @ex(
        help='Generate models from an existing database (output to console)',
        arguments=[
            ( [ '--tables' ],
              { 'help' : 'Print models only for the given tables, comma-separated'} ),
            ( [ '--schema' ],
              { 'help' : 'IF using PG, set the schema'} )
        ]
    )
    def db_generate_models(self):
        parsed = urlparse(self.app.config.get('APP', 'database'))
        connect_kwargs = parseresult_to_dict(parsed, False)
        # print(connect_kwargs)
        connect = {'user': connect_kwargs['user'], 'password': connect_kwargs['passwd'] if 'passwd' in connect_kwargs else connect_kwargs['password'], 'host':connect_kwargs['host']}
        if self.app.pargs.schema:
            connect['schema'] = self.app.pargs.schema
            
        database = connect_kwargs['database']
        
        if self.app.pargs.tables:
            tables = self.app.pargs.tables.split(',')
            tables = [table.strip() for table in self.app.pargs.tables.split(',')]
        else:
            tables = None

        self.app.log.debug(tables, 'Generate models only for tables')
        
        
        introspector = make_introspector(parsed.scheme, database, **connect)
        print_models(introspector, tables, None, False, None, False)

        
