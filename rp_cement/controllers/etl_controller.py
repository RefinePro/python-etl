from cement import ex
from .base_controller import BaseController
from playhouse.dataset import DataSet

# import peewee as pw
# import peeweedbevolve
# from pwiz import make_introspector, print_models
# from urllib.parse import urlparse
# from playhouse.db_url import parseresult_to_dict

class ETLController(BaseController):

    class Meta:
        label = 'rp-etl'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @ex(
        help='Insert some data in an arbitrary table, will create or erase the table on the fly',
        arguments=[
            ( [ '--table' ],
              { 'help' : 'Table to insert into', 'required':True} ),
            ( [ '--file' ],
              { 'help' : 'File where to find the data', 'required':True} ),
            ( [ '--format' ],
              { 'help' : 'JSON/CSV, or wathever is supported by peewee/Dataset/Thaw', 'required':True} )
        ]
    )
    def etl_file_to_table(self):
        """Example sub-command."""
        db = DataSet(self.app.config.get('APP', 'database'))
        table = db[self.app.pargs.table]
        table.thaw(filename=self.app.pargs.file, format=self.app.pargs.format)
        self.info('Done !, file has been loaded to', self.app.pargs.table)
    

        
